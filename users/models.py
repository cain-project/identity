from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.db import models

from django.utils.translation import gettext as _
from phonenumber_field.modelfields import PhoneNumberField


class UserManager(BaseUserManager):

    def create_user(self, **user_data):
        user = User.objects.create(**user_data)
        user.set_password(user_data['password'])
        user.save()
        return user

    def create_superuser(self, **user_data):
        user = self.create_user(**user_data)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    The custom user model.
    """

    objects = UserManager()

    REQUIRED_FIELDS = ['given_name', 'family_name', 'full_name',
                       'preferred_name', 'locale']
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'

    given_name = models.CharField(_("Given Name"), max_length=256)
    middle_name = models.CharField(_("Middle Name(s)"), max_length=256, blank=True)
    family_name = models.CharField(_("Family Name"), max_length=256)
    full_name = models.CharField(_("Full Name"), max_length=1024)
    preferred_name = models.CharField(_("Preferred Name"), max_length=256)
    locale = models.CharField(_("Locale"), max_length=256)
    phone_number = PhoneNumberField(_("Phone Number"), blank=True)
    date_of_birth = models.DateField(_("Date of Birth"), blank=True, null=True)
    date_created = models.DateTimeField(_("Created"), auto_now_add=True)
    date_updated = models.DateTimeField(_("Updated"), auto_now=True)
    email = models.EmailField(unique=True, db_index=True)

    is_staff = models.BooleanField(_('Staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(_('Active'), default=True,
                                    help_text=_('Designates whether this user should be treated as active. '
                                                'Unselect this instead of deleting accounts.'))

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_short_name(self):
        """Return the short name for the user."""
        return self.given_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        ordering = ('full_name',)
        indexes = [models.Index(fields=('given_name', 'family_name')),
                   models.Index(fields=('full_name', 'preferred_name'))]

    def __str__(self):
        return self.full_name


class Group(models.Model):
    """
    A group of users, with a name, and admins.
    """

    name = models.CharField(_("Name"), max_length=255)
    short_name = models.CharField(_("Short Name"), max_length=64)
    slug = models.SlugField(_("Slug"), unique=True)

    class Meta:
        verbose_name = _("Group")
        verbose_name_plural = _("Groups")
        ordering = ('short_name',)

    def __str__(self):
        return self.short_name


class Membership(models.Model):
    """
    A user's membership to a group.
    """
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Membership")
        verbose_name_plural = _("Memberships")
        ordering = ('date_created',)
        indexes = [models.Index(fields=('user', 'group'),)]
        unique_together = ('user', 'group')

    def __str__(self):
        return _("%(user)s's membership to %(group)s") % \
               dict(user=self.user, group=self.group)


class Responsibility(models.Model):
    """
    A generic responsibility which can be assigned as a role.
    """
    name = models.CharField(_("Name"), max_length=64)
    description = models.CharField(_("Description"), max_length=255)
    slug = models.SlugField(_("Slug"), unique=True)
    is_available = models.BooleanField(_("Available"), default=True)

    class Meta:
        verbose_name = _("Responsibility")
        verbose_name_plural = _("Responsibilities")
        ordering = ('-is_available', 'name')

    def __str__(self):
        return self.name


class Role(models.Model):
    """
    A responsibility when assigned to a user, in the context of their membership.
    """

    date_created = models.DateTimeField(auto_now_add=True)
    membership = models.ForeignKey(Membership, on_delete=models.CASCADE)
    responsibility = models.ForeignKey(Responsibility, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Role")
        verbose_name_plural = _("Roles")
        ordering = ('date_created',)
        unique_together = ('membership', 'responsibility',)

    def __str__(self):
        return _("%(user)s's role as %(responsibility)s "
                 "at %(group)s") % \
                dict(user=self.membership.user, responsibility=self.responsibility,
                     group=self.membership.group)
