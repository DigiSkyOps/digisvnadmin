from django.db import models

# Create your models here.

from django.contrib.auth.models import User, Group


class SvnProject(models.Model):
    project_name = models.CharField(max_length=30, unique=True, verbose_name="项目名称")
    project_ab = models.CharField(max_length=30, unique=True, verbose_name="项目英文缩写")

    def __str__(self):
        return u"%s - %s" % (self.project_name, self.project_ab)

    class Meta:
        verbose_name = u"SVN项目"
        verbose_name_plural = verbose_name


class SvnAuthPath(models.Model):
    project = models.ForeignKey(SvnProject, on_delete=models.CASCADE)
    path = models.CharField(max_length=150, verbose_name="权限路径")

    def __str__(self):
        return u"%s - %s" % (self.project, self.path)

    class Meta:
        unique_together = (('project', 'path'),)
        verbose_name = u"权限路径定义"
        verbose_name_plural = verbose_name


class SvnUserAuth(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="权限成员", null=True)
    svn_auth_path = models.ForeignKey(SvnAuthPath, on_delete=models.CASCADE)
    read = models.BooleanField(default=False)
    write = models.BooleanField(default=False)

    def __str__(self):
        return u"%s - %s - %s - %s" % (self.svn_auth_path, self.user, self.read, self.write)

    def save(self, *args, **kwargs):
        super(SvnUserAuth, self).save(*args, **kwargs)
        from apps.authz.views import svn_authz
        from digisvn.config import SVN_AUTHZ_FILE
        svn_authz(SVN_AUTHZ_FILE)

    class Meta:
        unique_together = (('user', 'svn_auth_path'),)
        verbose_name = u"用户权限设定"
        verbose_name_plural = verbose_name

class SvnGroupAuth(models.Model):
    svn_auth_path = models.ForeignKey(SvnAuthPath, on_delete=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name="权限组", null=True)
    read = models.BooleanField(default=False)
    write = models.BooleanField(default=False)

    def __str__(self):
        return u"%s - %s - %s - %s" % (self.svn_auth_path, self.group, self.read, self.write)

    def save(self, *args, **kwargs):
        super(SvnGroupAuth, self).save(*args, **kwargs)
        from apps.authz.views import svn_authz
        from digisvn.config import SVN_AUTHZ_FILE
        svn_authz(SVN_AUTHZ_FILE)

    class Meta:
        unique_together = (('group', 'svn_auth_path'),)
        verbose_name = u"组权限设定"
        verbose_name_plural = verbose_name


class SvnAdmin(models.Model):
    project = models.ForeignKey(SvnProject, on_delete=models.CASCADE, verbose_name="SVN 项目")
    admin_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="项目管理者")

    def __str__(self):
        return u"%s - %s" % (self.project, self.admin_user)

    class Meta:
        unique_together = (('project', 'admin_user'),)
        verbose_name = u"项目管理"
        verbose_name_plural = verbose_name
