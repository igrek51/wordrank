FROM node:9 AS frontend-builder
RUN npm install -g @angular/cli@6
COPY angular.json \
    package.json \
    package-lock.json \
    proxy.conf.json \
    tsconfig.json \
    tslint.json \
    /build/
WORKDIR /build
RUN npm install

COPY src /build/src
RUN npm install
RUN ng build --prod --output-path=static --deploy-url=/webdict/ --base-href=/webdict/
