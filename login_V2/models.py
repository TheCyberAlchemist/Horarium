from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
# from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver


class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, email, password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name']
    def __str__(self):
        return self.first_name + " " + self.last_name
    objects = CustomUserManager()


class AuditEntry(models.Model):
    action = models.CharField(max_length=64)
    forwarded_ip = models.TextField(null=True)
    ip = models.GenericIPAddressField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True,null=True)
    email_used = models.CharField(max_length=256, null=True)
    password_used = models.TextField(null=True)
    user_agent = models.TextField(null=True)
    user_id = models.ForeignKey(CustomUser,default=None,null=True,on_delete = models.SET_NULL)

    # def __unicode__(self):
    #     return '{0} - {1} - {2}'.format(self.action, self.email, self.ip)

    def __str__(self):
        return '{0} - {1} - {2}'.format(self.action, self.email_used, self.ip)


@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):  
    forwarded_ip = request.META.get('HTTP_X_FORWARDED_FOR')
    ip = request.META.get('REMOTE_ADDR')
    AuditEntry.objects.create(
        action='user_logged_in',
        forwarded_ip=forwarded_ip,
        ip=ip,
        email_used=user.email,
        user_agent= type(request.META['HTTP_USER_AGENT']),
        user_id = user
    )



@receiver(user_logged_out)
def user_logged_out_callback(sender, request, user, **kwargs):  
    forwarded_ip = request.META.get('HTTP_X_FORWARDED_FOR')
    ip = request.META.get('REMOTE_ADDR')
    # print(ip,user.email)
    AuditEntry.objects.create(
        action='user_logged_out',
        forwarded_ip=forwarded_ip,
        ip=ip,
        user_agent= type(request.META['HTTP_USER_AGENT']),
        user_id = user
    )


# @receiver(user_login_failed)
# def user_login_failed_callback(sender, credentials, **kwargs):
#     pass
    # forwarded_ip = request.META.get('HTTP_X_FORWARDED_FOR')
    # ip = request.META.get('REMOTE_ADDR')
    # print(ip,credentials['password'])
    # AuditEntry.objects.create(
    #     action='user_logged_in',
    #     forwarded_ip=forwarded_ip,
    #     ip=ip,
    #     email_used=user.email,
    #     user_agent= type(request.META['HTTP_USER_AGENT']),
    #     user_id = user
    # )
    # AuditEntry.objects.create(action='user_login_failed', email=credentials.get('email', None))