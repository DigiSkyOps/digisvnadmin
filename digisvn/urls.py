"""digisvn URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path

from django.urls import include, path
from rest_framework import routers
from apps.svnuser import views
from apps.authz import router as authz_router
from apps.svnuser import router as svnuser_router
from apps.authz import urls as authz_url

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

urlpatterns = [
    path('', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/svnauth/', include(authz_router.router.urls)),
    path('api/svnuser/', include(svnuser_router.router.urls)),
    path('api/authz/', include(authz_url)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

admin.site.site_header = 'SVN权限管理后台'