#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/../.."

HOST="${DEPLOY_HOST:-titan}"
REMOTE_DIR="${REMOTE_DIR:-/opt/wordrank}"
IMAGE="${IMAGE:-registry.gitlab.com/igrek51/registry/wordrank:latest}"
REGISTRY="${IMAGE%%/*}"
DB="${HOME}/src/igrekdev-backup/wordrank/wordrank.sqlite"

WITH_DATA=0
[ "${1:-}" = "--with-data" ] && WITH_DATA=1

ENV_FILE="${ENV_FILE:-$HOME/src/igrekdev-backup/wordrank/.env}"
[ -f "$ENV_FILE" ] || ENV_FILE="deploy/.env"
[ -f "$ENV_FILE" ] || { echo "error: missing $ENV_FILE (DJANGO_SECRET_KEY)" >&2; exit 1; }

echo "==> logging in to ${REGISTRY}"
docker login "$REGISTRY"

echo "==> checking ${HOST}"
if ! REMOTE_ARCH=$(ssh "$HOST" 'command -v docker >/dev/null && docker version --format "{{.Server.Arch}}"'); then
    echo "error: Docker Engine + Compose v2 must be installed and usable" >&2
    echo "       without sudo by the ${HOST} SSH user" >&2
    exit 1
fi

LOCAL_ARCH="$(docker version --format '{{.Server.Arch}}')"
PLATFORM="${PLATFORM:-linux/${REMOTE_ARCH}}"
TARGET_ARCH="${PLATFORM#linux/}"
TARGET_ARCH="${TARGET_ARCH%%/*}"

case "$TARGET_ARCH" in
    amd64) BINFMT_ARCH=x86_64 ;;
    arm64) BINFMT_ARCH=aarch64 ;;
    *) BINFMT_ARCH="$TARGET_ARCH" ;;
esac

if [[ "$TARGET_ARCH" != "$LOCAL_ARCH" ]] && ! compgen -G "/proc/sys/fs/binfmt_misc/qemu-${BINFMT_ARCH}*" >/dev/null; then
    echo "error: cannot build ${PLATFORM} on ${LOCAL_ARCH} without binfmt emulation" >&2
    echo "       run once, then retry:" >&2
    echo "       docker run --privileged --rm tonistiigi/binfmt --install ${TARGET_ARCH}" >&2
    exit 1
fi

echo "==> building ${IMAGE} for ${PLATFORM}"
docker build --platform "$PLATFORM" -f backend/Dockerfile -t "$IMAGE" backend

BUILT_ARCH="$(docker image inspect "$IMAGE" --format '{{.Architecture}}')"
if [[ "$BUILT_ARCH" != "$TARGET_ARCH" ]]; then
    echo "error: built image is ${BUILT_ARCH}, expected ${TARGET_ARCH}" >&2
    exit 1
fi

echo "==> pushing ${IMAGE}"
docker push "$IMAGE"

echo "==> preparing ${HOST}:${REMOTE_DIR}"
ssh "$HOST" "sudo mkdir -p '$REMOTE_DIR/volumes/db' \
  && sudo chown -R \$(id -u):\$(id -g) '$REMOTE_DIR'"

echo "==> copying compose and env"
rsync -avh --info=progress2 deploy/docker-compose.yaml "$HOST:$REMOTE_DIR/compose.yaml"
rsync -avh --info=progress2 "$ENV_FILE" "$HOST:$REMOTE_DIR/.env"
ssh "$HOST" "chmod 600 '$REMOTE_DIR/.env'"

if [ "$WITH_DATA" = 1 ]; then
    [ -f "$DB" ] || { echo "error: missing backup $DB" >&2; exit 1; }
    echo "==> restoring wordrank.sqlite from backup"
    ssh "$HOST" "cd '$REMOTE_DIR' && WORD_RANK_IMAGE='$IMAGE' docker compose stop wordrank" || true
    rsync -avh --info=progress2 --no-owner --no-group --rsync-path="sudo rsync" \
        "$DB" "$HOST:$REMOTE_DIR/volumes/db/"
fi

echo "==> data dir -> uid 1000"
ssh "$HOST" "sudo chown -R 1000:1000 '$REMOTE_DIR/volumes/db'"

echo "==> pulling ${IMAGE} on ${HOST}"
if ! ssh "$HOST" "cd '$REMOTE_DIR' && WORD_RANK_IMAGE='$IMAGE' docker compose pull wordrank"; then
    echo "error: pull failed; log in on ${HOST} with:" >&2
    echo "       ssh -t ${HOST} docker login ${REGISTRY}" >&2
    exit 1
fi

echo "==> recreating container"
ssh "$HOST" "cd '$REMOTE_DIR' && WORD_RANK_IMAGE='$IMAGE' docker compose up -d --force-recreate --remove-orphans"

echo "==> container status"
ssh "$HOST" "cd '$REMOTE_DIR' && WORD_RANK_IMAGE='$IMAGE' docker compose ps"

echo "==> done: http://${HOST}:8080/ (nginx: https://wordrank.igrek.dev)"
