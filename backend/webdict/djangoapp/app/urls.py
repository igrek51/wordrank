from django.shortcuts import redirect
from django.urls import include, path
from django.contrib import admin

from wordrank.djangoapp.words.dump import dump_database
from wordrank.djangoapp.words.staticfiles import staticfiles_urlpatterns

urlpatterns = [
    path('', lambda req: redirect('wordrank/')),
    path('wordrank/', include('wordrank.djangoapp.words.urls')),
    path('admin/', admin.site.urls),
    path('dump/', dump_database),
] + staticfiles_urlpatterns()
