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

def delete_selected_and_clean_data(modeladmin, request, queryset):
    for i in queryset:
        i.delete()
    from apps.authz.views import svn_user_passwd
    from digisvn.config import SVN_PASSWORD_FILE
    svn_user_passwd(SVN_PASSWORD_FILE)

    from apps.authz.views import svn_authz
    from digisvn.config import SVN_AUTHZ_FILE
    svn_authz(SVN_AUTHZ_FILE)

    from apps.authz.views import svn_group
    from digisvn.config import SVN_GROUP_AUTHZ_FILE
    svn_group(SVN_GROUP_AUTHZ_FILE)

    delete_selected_and_clean_data.short_description = 'delete selected and clean svn config'

class SvnUserAdmin(UserAdmin):
    actions = [delete_selected_and_clean_data]
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)
    filter_horizontal = ()
    inlines = [ ProfileInline, ]
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'last_name', 'email', 'password1', 'password2'),
        }),
    )

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

        from apps.authz.views import svn_group
        from digisvn.config import SVN_GROUP_AUTHZ_FILE
        svn_group(SVN_GROUP_AUTHZ_FILE)

        return instance

class SvnGroupAdmin(admin.ModelAdmin):
    actions = [delete_selected_and_clean_data]
    form = GroupAdminForm
    filter_horizontal = ['permissions']

admin.site.unregister(Group)
admin.site.register(Group, SvnGroupAdmin)
