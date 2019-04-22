from django.contrib import admin

# Register your models here.

from apps.authz.models import *

@admin.register(SvnUserAuth)
class SvnUserAuth_Admin(admin.ModelAdmin):
    list_display = ('svn_auth_path', 'user', 'read', 'write')
    fields = ('svn_auth_path', 'user', 'read', 'write')
    list_filter = ('svn_auth_path', 'user', 'read', 'write')
    search_fields = ['user__username',]

@admin.register(SvnGroupAuth)
class SvnGroupAuth_Admin(admin.ModelAdmin):
    list_display = ('svn_auth_path', 'group', 'read', 'write')
    fields = ('svn_auth_path', 'group', 'read', 'write')
    list_filter = ('svn_auth_path', 'group', 'read', 'write')

class SvnAdminInline(admin.TabularInline):
    model = SvnAdmin
    extra = 1

@admin.register(SvnProject)
class SvnProject_Admin(admin.ModelAdmin):
    fields = ('project_name', 'project_ab')
    list_filter = ('project_name', 'project_ab')

    inlines = [
        SvnAdminInline,
    ]

class SvnUserAuthPathInline(admin.TabularInline):
    model = SvnUserAuth

class SvnGroupAuthPathInline(admin.TabularInline):
    model = SvnGroupAuth

@admin.register(SvnAuthPath)
class SvnAuthPath_Admin(admin.ModelAdmin):
    list_display = ('project', 'path')
    list_filter = ('project', 'path')
    search_fields = ['project__project_name', 'path']

    inlines = [
        SvnUserAuthPathInline,
        SvnGroupAuthPathInline
    ]

@admin.register(SvnAdmin)
class SvnAdmin_Admin(admin.ModelAdmin):
    fields = ('project', 'admin_user')

