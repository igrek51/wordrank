from webdict.api.errors import EntityNotFound
from webdict.djangoapp.words import models


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


def find_dictionary_by_code(dict_code: str) -> models.Dictionary:
    lang_codes = dict_code.split('-')
    assert len(lang_codes) == 2 or (len(lang_codes) == 3 and lang_codes[2] == 'r'), 'invalid dictionary code'
    try:
        source_lang = find_language_by_code(lang_codes[0])
        target_lang = find_language_by_code(lang_codes[1])
        return models.Dictionary.objects.get(source_language_id=source_lang.id, target_language_id=target_lang.id)
    except models.Dictionary.DoesNotExist:
        raise EntityNotFound(f'Dictionary with code {dict_code} was not found')
