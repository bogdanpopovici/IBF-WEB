#  --- University of Southampton ---
#  --- Group Design Project in collaboration with 'The Big Consulting' ---
#  --- Copyright 2015 ---

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from core.models import *
from core.forms import CustomUserChangeForm, RegistrationForm

admin.site.register(Item)
admin.site.register(PreRegisteredItem)
admin.site.register(Media)
admin.site.register(Notification)

class CustomUserAdmin(UserAdmin):
    # The forms to add and change user instances

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference the removed 'username' field
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('username', 'first_name', 'last_name', 'is_premium','prefered_way_of_contact', 'phone_number' )}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2')}
        ),
    )
    form = CustomUserChangeForm
    add_form = RegistrationForm
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_premium')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)

admin.site.register(CustomUser, CustomUserAdmin)