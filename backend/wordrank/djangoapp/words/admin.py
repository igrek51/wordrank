from django.contrib import admin

from .models import *


class LanguageAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'code',
    )


class DictionaryAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'source_language', 
        'target_language',
    )


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'login',
    )


class WordAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'definition',
        'dictionary',
        'create_time',
    )
    search_fields = [
        'id',
        'name',
        'definition',
    ]
    list_filter = [
        'dictionary',
    ]


class UserWordAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'word',
    )


class RankAdmin(admin.ModelAdmin):
    list_display = (
        'get_user_word_word_name',
        'get_user_word_word_definition',
        'reversed_dictionary',
        'rank_value',
        'tries_count',
        'last_use',
        'get_user_word_user',
    )
    search_fields = [
        'id',
        'user_word__word__name',
        'user_word__word__definition',
    ]
    list_filter = [
        'reversed_dictionary',
    ]

    @admin.display(ordering='user_word__user', description='User')
    def get_user_word_user(self, obj):
        return obj.user_word.user

    @admin.display(ordering='user_word__word__name', description='Word name')
    def get_user_word_word_name(self, obj):
        return obj.user_word.word.name

    @admin.display(ordering='user_word__word__definition', description='Definition')
    def get_user_word_word_definition(self, obj):
        return obj.user_word.word.definition


admin.site.register(Language, LanguageAdmin)
admin.site.register(Dictionary, DictionaryAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Word, WordAdmin)
admin.site.register(UserWord, UserWordAdmin)
admin.site.register(Rank, RankAdmin)
