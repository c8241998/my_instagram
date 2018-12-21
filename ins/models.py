import datetime

from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, username, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not username:
            raise ValueError('Users must have username')

        user = self.model(
            username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            username=username,
            password=password
        )

        user.is_admin = True
        user.save(using=self._db)
        return user


def profile_path(instance, filename):
    return '{}/{}'.format(instance.id, filename)


class UserProfile(AbstractBaseUser):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        max_length=150,
        unique=True,
        blank=False,
        validators=[username_validator],
    )
    email = models.EmailField(
        verbose_name='email address',
        max_length=150,
        unique=True,
    )
    created_at = models.DateTimeField()
    photo = models.ImageField(upload_to=profile_path, default='default_photo.jpg')
    posts = models.IntegerField(default=0)

    website = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    phone = models.CharField(max_length=25)
    sex = models.CharField(max_length=25, default='unknown')

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'created_at']

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


def post_path(instance, filename):
    path = '{}/{}'.format(instance.user.id, 'post')
    filename = '{}.{}'.format(instance.create_at, 'jpg')
    return '{}/{}'.format(path, filename)


class Post(models.Model):
    user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE
    )
    create_at = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=150)
    photo = models.ImageField(upload_to=post_path)
    likes = models.IntegerField(default=0)


class Like(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE
    )
    create_at = models.DateTimeField(auto_now_add=True)
