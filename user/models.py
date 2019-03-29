from django.db import models
import json
import re
from django.utils.encoding import python_2_unicode_compatible
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core import validators
from django.utils.translation import ugettext, ugettext_lazy as _
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group as DjangoGroup, Permission as DjangoPermission


def validate_json(value):
    try:
        json.loads(value)
    except:
        raise ValidationError(_('Ivalid JSON syntax'))


class User(AbstractBaseUser, PermissionsMixin):
    """A custom User model with timezone and language support.
    """
    username = models.CharField(
        max_length=30,
        unique=True,
        help_text=_('Required. 30 characters or fewer. Letters, numbers and '
                    '@/./+/-/_ characters'),
        validators=[
            validators.RegexValidator(re.compile(
                '^[\w.@+-]+$'), _('Enter a valid username.'), 'invalid')
        ],
        verbose_name=_('username')
    )
    email = models.EmailField(max_length=254, verbose_name=_('email'))
    is_staff = models.BooleanField(default=False, help_text=_(
        'Designates whether the user can log into this admin site.'), verbose_name=_('staff'))
    is_active = models.BooleanField(default=True, help_text=_(
        'Designates whether this user should be treated as active. Unselect this instead of deleting accounts.'), verbose_name=_('active'))
    date_joined = models.DateTimeField(
        default=timezone.now, verbose_name=_('date joined'))
    language = models.CharField(max_length=5, null=True, choices=settings.LANGUAGES,
                                default=settings.LANGUAGE_CODE, verbose_name=_("language"))
    TimeZone = models.CharField(max_length=20, null=True,
                                #choices=settings.TIME_ZONES,
                                default=settings.TIME_ZONE, verbose_name=_("timezone"))

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    # objects = UserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self._meta.get_field('is_superuser').verbose_name = _('admin')

    def get_short_name(self):
        return self.username

    def get_full_name(self):
        return self.get_short_name()

    #@models.permalink
    def get_absolute_url(self):
        return ('user_detail', (), {"pk": self.pk})

    def email_user(self, subject, message, from_email=None):
        send_mail(subject, message, from_email, [self.email])


@python_2_unicode_compatible
class Group(DjangoGroup):
    """A proxy for Group model which customize its string representation.
    """
    class Meta:
        proxy = True

    def __str__(self):
        """In this proxy class the name is returned already translated.
        """
        return ugettext(self.name)


class Permission(DjangoPermission):
    """A proxy for Permission model which uses a custom manager.
    """
    # objects = PermissionManager()

    class Meta:
        proxy = True

    @property
    def uid(self):
        return "%s.%s" % (self.content_type.app_label, self.codename)


@python_2_unicode_compatible
class ObjectPermission(models.Model):
    """A generic object/row-level permission.
    """
    object_id = models.PositiveIntegerField()
    perm = models.ForeignKey(Permission, verbose_name=_("permission"), on_delete=models.CASCADE)
    users = models.ManyToManyField(
        User, blank=True, related_name='objectpermissions', verbose_name=_("users"))
    groups = models.ManyToManyField(
        Group, blank=True, related_name='objectpermissions', verbose_name=_("groups"))

    # objects = ObjectPermissionManager()

    class Meta:
        verbose_name = _('object permission')
        verbose_name_plural = _('object permissions')

    @property
    def uid(self):
        return "%s.%s" % (self.perm.uid, self.object_id)

    def __str__(self):
        return "%s | %d" % (self.perm, self.object_id)
