from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings


class UserManager(BaseUserManager):
    """User Manager class for create and update user and superuser"""

    def create_user(self, email, password=None, **extra_field):
        if not email:
            raise ValueError("User Must Have a Email")
        user = self.model(email=self.normalize_email(email), **extra_field)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    UNIVERSITY_ROLE = [
        ("S", "Student"),
        ("T", "Teacher"),
        ("A", "Admin"),
    ]

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    student_id = models.CharField(max_length=50, null=True)
    picture = models.URLField(max_length=255)

    role = models.CharField(max_length=1, choices=UNIVERSITY_ROLE, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    github = models.URLField(max_length=100, null=True)
    linkedIn = models.URLField(max_length=100, null=True)
    facebook = models.URLField(max_length=100, null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
