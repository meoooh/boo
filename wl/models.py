# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin,
                                        BaseUserManager)
from django.conf import settings
from django.core import validators

from gcm.models import AbstractDevice

class MyDevice(AbstractDevice):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

class MyUserManager(BaseUserManager):
    def create(self, deviceId, userId, sex, birthday, password):
        return self.create_user(
            deviceId=deviceId,
            userId=userId,
            sex=sex,
            birthday=birthday,
            password=password,
        )

    def create_user(self, deviceId, userId, sex, birthday, password):
        user = self.model(
            deviceId=deviceId,
            userId=userId,
            birthday=birthday,
            sex=sex,
            is_active=True,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
 
    def create_superuser(self, deviceId, userId, sex, birthday, password):
        user = self.create_user(
            deviceId=deviceId,
            userId=userId,
            sex=sex,
            birthday=birthday,
            password=password,
        )
        user.is_staff=True
        user.is_superuser=True
        user.is_admin=True
        user.save(using=self._db)

        return user

class OwlUser(AbstractBaseUser, PermissionsMixin):
    deviceId = models.CharField(max_length=254, unique=True)
    userId = models.CharField(max_length=254, unique=True)
    sex = models.BooleanField() # 왜 required fals인지 모르겠다...
    birthday = models.DateField()
    ideaTypeAgeMin = models.PositiveSmallIntegerField(
        validators=[
            validators.MaxValueValidator(100),
            validators.MinValueValidator(1),
        ],
        blank=True,
        null=True,
    )
    ideaTypeAgeMax = models.PositiveSmallIntegerField(
        validators=[
            validators.MaxValueValidator(100),
            validators.MinValueValidator(1),
        ],
        blank=True,
        null=True,
    )
    gcmId = models.CharField(max_length=254, unique=True)

    myVoice = models.FileField(upload_to='voice/%Y-%m-%d', blank=True,
                                null=True,)

    creation = models.DateTimeField(auto_now_add=True)
    modification = models.DateTimeField(auto_now=True)

    objects = MyUserManager()

    is_staff = models.BooleanField(default=False, blank=True,)
    is_active = models.BooleanField(default=True, blank=True,)

    def __unicode__(self):
        return self.userId

    def has_perm(self, perm, obj=None):
        return super(OwlUser, self).has_perm(perm, obj)

    def has_module_perms(self, app_label):
        return super(OwlUser, self).has_module_perms(app_label)

    def get_short_name(self):
        return self.userId

    def get_username(self):
        return self.userId

    def get_full_name(self):
        return self.userId

    USERNAME_FIELD = 'userId'
    REQUIRED_FIELDS = ['deviceId', 'birthday', 'sex',]
