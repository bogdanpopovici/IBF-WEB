#  --- University of Southampton ---
#  --- Group Design Project in collaboration with 'The Big Consulting' ---
#  --- Copyright 2015 ---

from __future__ import unicode_literals
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin,
                                        UserManager)
from django.core.mail import send_mail
from django.core import validators
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.utils.http import urlquote
from django.contrib.auth.models import BaseUserManager
from stdimage.models import StdImageField
import datetime, re

class CustomUserManager(BaseUserManager):

    def _create_user(self, username, email, password,
                     is_staff, is_superuser, is_active, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(username=username,
        	              email=email,
                          is_staff=is_staff, is_active=is_active,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password=None, **extra_fields):
        return self._create_user(username, email, password, False, False, False,
                                 **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        return self._create_user(username, email, password, True, True, True,
                                 **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):

	username = models.CharField(_('username'), max_length=75, unique=True,
		help_text=_('Required. 30 characters or fewer. Letters, numbers and '
					'@/./+/-/_ characters'),
		validators=[
			validators.RegexValidator(re.compile('^[\w.@+-]+$'),
			_('Enter a valid username.'), 'invalid')
		])

	first_name = models.CharField(_('first name'), max_length=254, blank=True)
	last_name = models.CharField(_('last name'), max_length=254, blank=True)
	email = models.EmailField(_('email address'), max_length=254, unique=True)
	is_staff = models.BooleanField(_('staff status'), default=False,
		help_text=_('Designates whether the user can log into this admin '
					'site.'))
	is_active = models.BooleanField(_('active'), default=True,
		help_text=_('Designates whether this user should be treated as '
					'active. Unselect this instead of deleting accounts.'))
	date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

	CONTACT_METHODS = (
        ('EMAIL', 'Email'),
		('PHONE', 'Phone'),
		('IBF', 'IBF')
    )

	prefered_way_of_contact = models.CharField(max_length=5,
											   choices=CONTACT_METHODS)

	phone_number = models.CharField(max_length=15, null=True, blank=True)
	address = models.CharField(max_length=100, null=True, blank=True)
	is_premium = models.BooleanField(_('premium status'), default=False)

	profile_picture = StdImageField(upload_to='profile_pics', null=True, blank=True, variations={
       'lg': {"width": 1200, "height": 1200, "crop":False},
       'md': {"width": 600, "height": 600, "crop":False},
       'sm': {"width": 100, "height": 100, "crop":False},
       'edit_profile': {"width": 200, "height": 300, "crop":False},
       'show_profile': {"width": 300, "height": 400, "crop":False},
       'navbar_icon': {"width": 50, "height": 50, "crop":True},
    })

	objects = CustomUserManager()

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email']

	class Meta:
	    verbose_name = _('user')
	    verbose_name_plural = _('users')

	def __unicode__(self):
	    return self.username

	def get_absolute_url(self):
	    return "/users/%s/" % urlquote(self.username)

	def get_full_name(self):
	    """
	    Returns the first_name plus the last_name, with a space in between.
	    """
	    if self.first_name or self.last_name:
	    	full_name = full_name = '%s %s' % (self.first_name, self.last_name)
	    else:
	    	full_name = self.username
	    return full_name.strip()

	def get_short_name(self):
	    "Returns the short name for the user."
	    return self.first_name

	def email_user(self, subject, message, from_email=None):
	    """
	    Sends an email to this User.
	    """
	    send_mail(subject, message, from_email, [self.email])

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser)
    activation_key = models.CharField(max_length=40, blank=True)
    key_expires = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural='User profiles'

class AbstractItem(models.Model):
	item_id = models.AutoField(primary_key=True)

class Item(AbstractItem):

	unique_id = models.CharField(_('Unique Identification ID'), blank=True, null=True, max_length=40,
							help_text = "Unique Identification numbers like IMEI,Serial Number,reference number etc (Every item might not have it,so optional)")

	tags = models.CharField(max_length=2000)
	description = models.CharField(max_length=2000)
	found_by_user = models.ForeignKey('CustomUser', related_name='Item_found_by_user', null=True, blank=True, help_text = "The user id of the user who found item")
	lost_by_user = models.ForeignKey('CustomUser', related_name='Item_lost_by_user', null=True, blank=True, help_text = "The user id of the user who lost the item")
	location = models.CharField(max_length=30)
	category = models.CharField(max_length=30)
	date_field = models.DateField(blank=True)
	time_field = models.TimeField(blank=True)

	STATUS_TYPE = (
        ('FOUND', 'found'),
		('CLAIMED', 'claimed'),
		('PREREPATRIATED', 'prerepatriated'),
		('REPATRIATED', 'repatriated')
    )
	status = models.CharField(max_length=15,
								  choices=STATUS_TYPE ,
								  default='FOUND')

	def __unicode__(self):
		return self.tags + self.location

	def __str__(self):
		return self.tags + self.location

	def __repr__(self):
		return str(self)

class PreRegisteredItem(AbstractItem):

	unique_id = models.CharField(_('Unique Identification ID'), blank=True, null=True, max_length=40,
							help_text = "Unique Identification numbers like IMEI,Serial Number,reference number etc (Every item might not have it,so optional)")

	tags = models.CharField(max_length=2000)
	description = models.CharField(max_length=2000)
	owner = models.ForeignKey('CustomUser', related_name='owner', null=True, blank=True, help_text = "The user id of the user who found item")
	category = models.CharField(max_length=30)
	lost = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

	def __unicode__(self):
		return self.tags + self.category

	def __str__(self):
		return self.tags + self.category

	def __repr__(self):
		return str(self.tags)

class Media(models.Model):

	media_id = models.AutoField(primary_key=True)
	MEDIA_TYPES = (
        ('PHOTO', 'photo'),
		('VIDEO', 'video'),
		('AUDIO', 'audio')
    )
	of_item = models.ForeignKey('AbstractItem', blank=True, help_text = "Media recorded for this item")
	media_type = models.CharField(max_length=5,
								  choices=MEDIA_TYPES,
								  default='PHOTO')

	data = StdImageField(upload_to='items_media', null=True, blank=True)

	def __unicode__(self):
		return str(self.media_id)

class Notification(models.Model):

	message = models.CharField(max_length=2000)
	sender = models.ForeignKey('CustomUser', related_name='Notification_from', null=True, blank=True)
	receiver = models.ForeignKey('CustomUser', related_name='Notification_to', null=True, blank=True)
	topic = models.ForeignKey('Item', related_name='Notification_topic',null=True, blank=True)
	match = models.ForeignKey('PreRegisteredItem', related_name='Notification_match',null=True, blank=True)
	seen = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	
	NOTIFICATION_TYPE = (
        ('CLAIM', 'claim'),
		('ACCEPT', 'accept'),
		('REJECT', 'reject'),
		('MESSAGE', 'message'),
		('MATCH', 'match')
    )
	notification_type = models.CharField(max_length=8,
								  choices=NOTIFICATION_TYPE ,
								  default='MESSAGE')

	def __unicode__(self):
		return str(self.message)
