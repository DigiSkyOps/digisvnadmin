from django.db import models
from django.contrib.auth.models import User
from digisvn.config import *
# Create your models here.

from apps.authz.libs.encryption import PasswdCrypt
from digisvn.config import ENCRYPT_KEY
from datetime import datetime

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    password = models.CharField(max_length=30, blank=False, verbose_name="SVN密码")
    update_time = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        obj = PasswdCrypt(ENCRYPT_KEY)
        if self.password:
            self.password = obj.pw_encrypt(self.password).decode()
            self.update_time = datetime.now()
            super(Profile, self).save(*args, **kwargs)

            from apps.authz.views import svn_user_passwd
            svn_user_passwd(SVN_PASSWORD_FILE)


    class Meta:
        verbose_name = u"SVN用户密码"
        verbose_name_plural = verbose_name