from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

# Docs: https://docs.djangoproject.com/en/4.2/topics/auth/customizing/


class UserManager(BaseUserManager):
    def create_user(self, email, user_name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        if not user_name:
            raise ValueError("Users must have a user name")

        user = self.model(
            email=self.normalize_email(email),
            user_name=user_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, user_name, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            user_name=user_name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    user_name = models.CharField(verbose_name="user name", max_length=60, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "user_name"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.user_name
