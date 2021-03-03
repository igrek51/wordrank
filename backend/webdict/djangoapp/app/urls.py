from django.shortcuts import redirect
from django.conf import settings
from django.urls import include, path
from django.contrib import admin

from webdict.djangoapp.words.staticfiles import staticfiles_urlpatterns

urlpatterns = [
    path('', lambda req: redirect('webdict/')),
    path('webdict/', include('webdict.djangoapp.words.urls')),
    path('admin/', admin.site.urls),
    path('promi/', include('django_prometheus.urls')),
] + staticfiles_urlpatterns()
