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
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PersonalFinances.settings')



# from drf_yasg.views import get_schema_view
# from drf_yasg import openapi
# schema_view = get_schema_view(
#     openapi.Info(
#         title='My Personal Finances API',
#         default_version='v1',
#         description='Personal finances API that helps the user in numerous things.',
#         terms_of_service='https://www.google.com/policies/terms/',
#         contact=openapi.Contact(email='unai.devel@gmail.com'),
#         license=openapi.License(name='BSD License'),
#     ),
#     public=True,
#     permission_classes=(permissions.AllowAny,),
# )




urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include('finances.urls')), 
    path('api-auth/', include('rest_framework.urls')),
    path('rest-auth/', include(rest_auth_urls)),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
    path('auth/facebook', FacebookLogin.as_view(), name='fb_login'),
    path('auth/github/', GitHubLogin.as_view(), name='github_login'),
    path('auth/google/', GoogleLogin.as_view(), name='google_login'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
