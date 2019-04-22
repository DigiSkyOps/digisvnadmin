#!/usr/bin/env python
# -*-coding:utf-8-*-
# Create your views here.

from apps.authz.serializers import *
from rest_framework import viewsets


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = SvnProject.objects.all()
    serializer_class = ProjectSerializer


class ProjectPathViewSet(viewsets.ModelViewSet):
    queryset = SvnAuthPath.objects.all()
    serializer_class = ProjectPathSerializer


class UserAuthViewSet(viewsets.ModelViewSet):
    queryset = SvnUserAuth.objects.all()
    serializer_class = UserAuthSerializer


class GroupAuthViewSet(viewsets.ModelViewSet):
    queryset = SvnGroupAuth.objects.all()
    serializer_class = GroupAuthSerializer


from django.contrib.auth.models import User, Group
from apps.authz.models import SvnAuthPath
from apps.svnuser.models import Profile
import configparser

from apps.authz.models import SvnUserAuth, SvnGroupAuth
from digisvn.config import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from apps.authz.libs.encryption import PasswdCrypt
from digisvn.config import ENCRYPT_KEY


def svn_group(file):
    group_list = Group.objects.all()
    user_list = User.objects.all()
    config = configparser.ConfigParser()
    config.add_section('groups')
    for group in group_list:
        user_filter_list = []
        for user in user_list.filter(groups__name=group.name):
            user_filter_list.append(user.username)
        if len(user_filter_list) > 0:
            config.set('groups', group.name, (',').join(user_filter_list))

    with open(file, "w", encoding="utf-8") as groupfile:
        config.write(groupfile)
    groupfile.close()


def svn_authz(file):
    config = configparser.ConfigParser()
    for path in SvnAuthPath.objects.all():
        section = path.project.project_ab + ':' + path.path
        config.add_section(section)
        for authz in SvnUserAuth.objects.filter(svn_auth_path=path):
            op1 = "r" if authz.read else ""
            op2 = "w" if authz.write else ""
            op = op1 + op2
            config.set(section, authz.user.username, op)
        for authz in SvnGroupAuth.objects.filter(svn_auth_path=path):
            op1 = "r" if authz.read else ""
            op2 = "w" if authz.write else ""
            op = op1 + op2
            config.set(section, "@" + authz.group.name, op)

    with open(file, 'w', encoding="utf-8") as authfile:
        config.write(authfile)
    authfile.close()

@login_required
def group_update(request):
    try:
        _f_g_path = SVN_GROUP_AUTHZ_FILE
        svn_group(_f_g_path)
        return HttpResponse(status=200)
    except Exception as e:
        return HttpResponse(e)

@login_required
def authz_update(request):
    try:
        _f_path = SVN_AUTHZ_FILE
        svn_authz(_f_path)
        return HttpResponse(status=200)
    except Exception as e:
        return HttpResponse(e)

def svn_user_passwd(f):
    '更新用户密码文件'
    profile_list = Profile.objects.all()
    config = configparser.ConfigParser()
    config.add_section('users')
    pw = PasswdCrypt(ENCRYPT_KEY)
    for profile in profile_list:
        pw_plaintext = pw.pw_decrypt(profile.password.encode(encoding='utf-8'))
        config.set('users', profile.user.username, pw_plaintext)

    with open(f, 'w') as configfile:
        config.write(configfile)
    configfile.close()

@login_required
def passwd_update(request):
    try:
        f = SVN_PASSWORD_FILE
        svn_user_passwd(f)
        return HttpResponse(status=200)
    except Exception as e:
        return HttpResponse(e)
