#!/usr/bin/env python
# -*-coding:utf-8-*-
# Created by Eric.wu on 2019/3/28

from django.urls import include, path
from apps.authz.views import authz_update, passwd_update, group_update

urlpatterns = [
    path('passwordUpdate/', passwd_update),
    path('authUpdate/', authz_update),
    path('groupUpdate/', group_update),
]