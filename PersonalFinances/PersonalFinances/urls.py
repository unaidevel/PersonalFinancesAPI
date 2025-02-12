"""
URL configuration for PersonalFinances project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from dj_rest_auth import urls as rest_auth_urls
from finances.views import FacebookLogin, GitHubLogin, GoogleLogin
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PersonalFinances.settings')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('finances.urls')), 
    path('api-auth/', include('rest_framework.urls')),
    path('rest-auth/', include(rest_auth_urls)),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    path('dj-rest-auth/facebook', FacebookLogin.as_view(), name='fb_login'),
    path('dj-rest-auth/github/', GitHubLogin.as_view(), name='github_login'),
    path('dj-rest-auth/google/', GoogleLogin.as_view(), name='google_login'),
]
