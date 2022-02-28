from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import User, PermissionsMixin
from django.core.validators import MinLengthValidator
from django.db import models

# Create your models here.
from .validators import validator_only_letters


class PetstagramUserManager(BaseUserManager):
    def _create_user(self, username, password, **extra_fields):
        """
        Create and save a user with the given username, and password.
        """
        if not username:
            raise ValueError('The given username must be set')

        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.

        username = self.model.normalize_username(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, password, **extra_fields)


class PetstagramUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        unique=True,
        max_length=30,

    )

    USERNAME_FIELD = 'username'

    is_staff = models.BooleanField(
        default=False,
    )
    objects = PetstagramUserManager()


class Profile(models.Model):
    FIRST_NAME_MAX_LENGTH = 30
    FIRST_NAME_MIN_LENGTH = 2

    LAST_NAME_MAX_LENGTH = 30
    LAST_NAME_MIN_LENGTH = 2

    MALE = 'Male'
    FEMALE = 'Female'
    DO_NOT_SHOW = 'Do not show'
    GENDER = [(x, x) for x in (MALE, FEMALE, DO_NOT_SHOW)]

    first_name = models.CharField(
        max_length=FIRST_NAME_MAX_LENGTH,
        validators=(
            MinLengthValidator(FIRST_NAME_MIN_LENGTH),
            validator_only_letters,
        )

    )

    last_name = models.CharField(
        max_length=30,
        validators=(
            MinLengthValidator(LAST_NAME_MIN_LENGTH),
            validator_only_letters,
        )
    )

    profile_picture = models.ImageField(
        upload_to='profile_pictures',
        blank=True,


    )

    date_of_birth = models.DateField(
        null=True,
        blank=True,
        validators=(

        )
    )

    description = models.TextField(
        null=True,
        blank=True,
    )

    email = models.EmailField(
        null=True,
        blank=True,
    )

    # GENDER_CHOICE = (
    #     ("Male", "Male"),
    #     ("Female", "Female"),
    #     ("Do not show", "Do not show"),
    # )
    gender = models.CharField(
        max_length=max(len(x) for (x, _) in GENDER),
        choices=GENDER,
        null=True,
        blank=True,
    )
    user = models.OneToOneField(
        PetstagramUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


from .signals import *
