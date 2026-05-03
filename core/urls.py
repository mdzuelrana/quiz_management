from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from core.views import no_permission,base

urlpatterns = [
    path('no_permission/',no_permission,name='no_permission'),
    path('landing_page/',base,name='landing_page'),
]