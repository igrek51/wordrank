from django.contrib import admin

from .models import *


class LanguageAdmin(admin.ModelAdmin):
    list_display = ('id', 'code')


class DictionaryAdmin(admin.ModelAdmin):
    list_display = ('id', 'source_language', 'target_language')


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'login')


class WordAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'definition', 'dictionary')


class UserWordAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'word')


class RankAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'user_word', 
        'rank_value', 
        'reversed_dictionary', 
        'tries_count',
        'last_use', 
    )


admin.site.register(Language, LanguageAdmin)
admin.site.register(Dictionary, DictionaryAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Word, WordAdmin)
admin.site.register(UserWord, UserWordAdmin)
admin.site.register(Rank, RankAdmin)
