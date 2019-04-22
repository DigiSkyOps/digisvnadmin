from django.contrib import admin

# Register your models here.
from apps.svnuser.models import *
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.models import Group

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "password")
    fields = ("user", "password")
    formfield_overrides = {
        models.CharField: {'widget': forms.PasswordInput},
    }
    search_fields = ("user__username",)

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = True
    verbose_name_plural = 'SVN相关属性'
    fk_name = 'user'
    formfield_overrides = {
        models.CharField: {'widget': forms.PasswordInput},
    }

def delete_selected(modeladmin, request, queryset):
    for i in queryset:
        i.delete()
    from apps.authz.views import _svn_passwd_updata
    _svn_passwd_updata(SVN_PASSWORD_FILE)

    from apps.authz.views import _svn_auth_update
    from digisvn.config import SVN_AUTHZ_FILE
    _svn_auth_update(SVN_AUTHZ_FILE)

    from apps.authz.views import _svn_group_auth_update
    from digisvn.config import SVN_GROUP_AUTHZ_FILE
    _svn_group_auth_update(SVN_GROUP_AUTHZ_FILE)

    delete_selected.short_description = '删除已选项'

class SvnUserAdmin(UserAdmin):
    actions = [delete_selected]
    search_fields = ('username',)
    ordering = ('username',)
    filter_horizontal = ()
    inlines = [ ProfileInline, ]

admin.site.unregister(User)
admin.site.register(User, SvnUserAdmin)

class GroupAdminForm(forms.ModelForm):
    class Meta:
        model = Group
        exclude = []

    users = forms.ModelMultipleChoiceField(
         queryset=User.objects.all(),
         required=False,
         widget=FilteredSelectMultiple('users', False)
    )

    def __init__(self, *args, **kwargs):
        # Do the normal form initialisation.
        super(GroupAdminForm, self).__init__(*args, **kwargs)
        # If it is an existing group (saved objects have a pk).
        if self.instance.pk:
            # Populate the users field with the current Group users.
            self.fields['users'].initial = self.instance.user_set.all()

    def save_m2m(self):
        self.instance.user_set.set(self.cleaned_data['users'])

    def save(self, *args, **kwargs):
        # Default save
        instance = super(GroupAdminForm, self).save()
        self.save_m2m()

        from apps.authz.views import _svn_group_auth_update
        from digisvn.config import SVN_GROUP_AUTHZ_FILE
        _svn_group_auth_update(SVN_GROUP_AUTHZ_FILE)

        return instance

class SvnGroupAdmin(admin.ModelAdmin):
    actions = [delete_selected]
    form = GroupAdminForm
    filter_horizontal = ['permissions']

admin.site.unregister(Group)
admin.site.register(Group, SvnGroupAdmin)