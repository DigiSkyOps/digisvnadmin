#!/usr/bin/env python
# -*-coding:utf-8-*-
# Created by Eric.wu on 2019/3/28 

from rest_framework import routers
from apps.authz import views as authz_views

from django.conf.urls import url

router = routers.DefaultRouter()

router.register(r'project', authz_views.ProjectViewSet)
router.register(r'svnpath', authz_views.ProjectPathViewSet)
router.register(r'userauth', authz_views.UserAuthViewSet)
router.register(r'groupauth', authz_views.GroupAuthViewSet)