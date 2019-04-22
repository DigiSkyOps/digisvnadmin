#!/usr/bin/env python
# -*-coding:utf-8-*-
# Created by Eric.wu on 2019/3/25

from rest_framework import serializers
from apps.authz.models import *
from django.contrib.auth.models import User, Group

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = SvnProject
        fields = ('id', 'project_name', 'project_ab')

class ProjectPathSerializer(serializers.ModelSerializer):
    class Meta:
        model = SvnAuthPath
        fields = ('id', 'project', 'path')

class UserAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = SvnUserAuth
        fields = ('id', 'user', 'svn_auth_path', 'read', 'write')

class GroupAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = SvnGroupAuth
        fields = ('id', 'group', 'svn_auth_path', 'read', 'write')