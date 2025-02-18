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
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PersonalFinances.settings')


schema_view = get_schema_view(
    openapi.Info(
        title='My Personal Finances API',
        default_version='v1',
        description='Personal finances API that helps the user in numerous things.',
        terms_of_service='https://www.google.com/policies/terms/',
        contact=openapi.Contact(email='unai.devel@gmail.com'),
        license=openapi.License(name='BSD License'),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)




urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('finances.urls')), 
    path('api-auth/', include('rest_framework.urls')),
    path('rest-auth/', include(rest_auth_urls)),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    path('dj-rest-auth/facebook', FacebookLogin.as_view(), name='fb_login'),
    path('dj-rest-auth/github/', GitHubLogin.as_view(), name='github_login'),
    path('dj-rest-auth/google/', GoogleLogin.as_view(), name='google_login'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui')
]
