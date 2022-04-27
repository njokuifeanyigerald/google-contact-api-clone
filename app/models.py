from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin, UserManager
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class MyUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model( email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user( email, password, **extra_fields)


    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user( email, password, **extra_fields)



class  CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.CharField(_('email'),
        unique=True,
        max_length=300,
        help_text=_('email of the individual')
        )
    full_name = models.CharField(
        _('full name '),
        max_length=300,
        help_text=_('full name of the individual')
        
    )
    date_joined = models.DateTimeField(_('date joined'),default=timezone.now)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_("Designates whether the user can log into this admin site.")
    )
    contacts = models.ManyToManyField(_('contacts'),
    'Contact', 
    blank=True,
    help_text=_(' a many to many field of the Contact Model')
    )


    objects = MyUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]


    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

