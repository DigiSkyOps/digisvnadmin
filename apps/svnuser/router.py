#!/usr/bin/env python
# -*-coding:utf-8-*-
# Created by Eric.wu on 2019/3/28 

from rest_framework import routers
from apps.svnuser import views

router = routers.DefaultRouter()
router.register(r'profile', views.ProfileViewSet)