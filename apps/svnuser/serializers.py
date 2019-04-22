#!/usr/bin/env python
# -*-coding:utf-8-*-
# Created by Eric.wu on 2019/3/25 

from django.contrib.auth.models import User, Group
from rest_framework import serializers
from apps.svnuser.models import Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'groups')

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id','name',)

class ProfileSerizlizer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('user', 'password')

