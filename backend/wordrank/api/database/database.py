from typing import Iterable
from wordrank.api.errors import EntityNotFound
from wordrank.djangoapp.words import models


def find_user_by_id(id: str) -> models.User:
    try:
        return models.User.objects.get(id=id)
    except models.User.DoesNotExist:
        raise EntityNotFound(f'User with id {id} was not found')


def find_language_by_code(lang: str) -> models.Language:
    try:
        return models.Language.objects.get(code=lang)
    except models.Language.DoesNotExist:
        raise EntityNotFound(f'Language with code {lang} was not found')


def find_word_by_name(name: str, user_id: str, dictionary: models.Dictionary) -> models.Word:
    try:
        return models.UserWord.objects.get(user__id=user_id, word__name=name, word__dictionary=dictionary)
    except models.UserWord.DoesNotExist:
        raise EntityNotFound(f'Word with named {name} was not found')


def word_exists(name: str, user_id: str, dictionary: models.Dictionary) -> bool:
    try:
        find_word_by_name(name, user_id, dictionary)
        return True
    except EntityNotFound:
        return False


def find_rank_by_id(rank_id: str) -> models.Rank:
    try:
        return models.Rank.objects.get(id=rank_id)
    except models.Rank.DoesNotExist:
        raise EntityNotFound(f'Rank with id {rank_id} was not found')


def find_userword_by_id(id: str) -> models.UserWord:
    try:
        return models.UserWord.objects.get(id=id)
    except models.UserWord.DoesNotExist:
        raise EntityNotFound(f'UserWord with id {id} was not found')


def find_dictionary_by_code(dict_code: str) -> models.Dictionary:
    lang_codes = dict_code.split('-')
    assert len(lang_codes) == 2 or (len(lang_codes) == 3 and lang_codes[2] == 'r'), 'invalid dictionary code'
    try:
        source_lang = find_language_by_code(lang_codes[0])
        target_lang = find_language_by_code(lang_codes[1])
        return models.Dictionary.objects.get(source_language_id=source_lang.id, target_language_id=target_lang.id)
    except models.Dictionary.DoesNotExist:
        raise EntityNotFound(f'Dictionary with code {dict_code} was not found')


def generate_all_ranks(
    user: models.User, dictionary: models.Dictionary, reversed: bool,
) -> Iterable[models.Rank]:
    objects = models.Rank.objects.filter(
        reversed_dictionary=reversed,
        user_word__user=user,
        user_word__word__dictionary=dictionary,
    )
    for model in objects:
        yield model


def generate_all_userwords(
    user: models.User, dictionary_id: str,
) -> Iterable[models.UserWord]:
    objects = models.UserWord.objects.filter(
        user=user,
        word__dictionary__id=dictionary_id,
    )
    for model in objects:
        yield model


def generate_all_words(
    dictionary_id: str,
) -> Iterable[models.Word]:
    objects = models.Word.objects.filter(
        dictionary__id=dictionary_id,
    )
    for model in objects:
        yield model


def list_users() -> Iterable[models.User]:
    objects = models.User.objects.all().order_by('login')
    for object in objects:
        yield object


def list_dictionaries() -> Iterable[models.Dictionary]:
    objects = models.Dictionary.objects.all()
    for object in objects:
        yield object
