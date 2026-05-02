from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from core.views import no_permission

urlpatterns = [
    path('no_permission/',no_permission,name='no_permission')
]