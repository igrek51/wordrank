import uuid

from django.db import models

from .time import now


def new_uuid() -> str:
    return str(uuid.uuid4())


class Language(models.Model):
    id = models.CharField(max_length=36, primary_key=True, default=new_uuid)
    code = models.CharField(max_length=255)

    def __str__(self):
        return self.code


class Dictionary(models.Model):
    id = models.CharField(max_length=36, primary_key=True, default=new_uuid)
    source_language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='source_language_id')
    target_language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='target_language_id')

    def __str__(self):
        return f'{self.source_language.code} -> {self.target_language.code}'


class User(models.Model):
    id = models.CharField(max_length=36, primary_key=True, default=new_uuid)
    login = models.CharField(max_length=255)
    token = models.CharField(max_length=255)

    def __str__(self):
        return self.login


class Word(models.Model):
    id = models.CharField(max_length=36, primary_key=True, default=new_uuid)
    dictionary = models.ForeignKey(Dictionary, on_delete=models.CASCADE, related_name='dictionary_id')
    name = models.CharField(max_length=255)
    definition = models.CharField(max_length=255)
    create_time = models.DateTimeField(default=now)

    def __str__(self):
        return f'{self.name} - {self.definition}'


class UserWord(models.Model):
    id = models.CharField(max_length=36, primary_key=True, default=new_uuid)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_id')
    word = models.ForeignKey(Word, on_delete=models.CASCADE, related_name='word_id')

    def __str__(self):
        return f'{self.word}'


class Rank(models.Model):
    id = models.CharField(max_length=36, primary_key=True, default=new_uuid)
    reversed_dictionary = models.BooleanField()
    last_use = models.DateTimeField(null=True, blank=True)
    rank_value = models.DecimalField(max_digits=6, decimal_places=3, default=0)
    tries_count = models.IntegerField(default=0)
    user_word = models.ForeignKey(UserWord, on_delete=models.CASCADE, related_name='user_word_id')

    def __str__(self):
        return f'{self.user_word} ({self.rank_value})'
