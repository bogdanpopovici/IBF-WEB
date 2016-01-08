#  --- University of Southampton ---
#  --- Group Design Project in collaboration with 'The Big Consulting' ---
#  --- Copyright 2015 ---

from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from core.models import CustomUser

class RegistrationForm(UserCreationForm):

    def __init__(self, *args, **kargs):
        super(RegistrationForm, self).__init__(*args, **kargs)

    class Meta:
        model = CustomUser
        fields = ['username', 'phone_number', 'first_name', 'last_name', 'email', 'prefered_way_of_contact', 'is_premium', 'password1', 'password2']

class CustomUserChangeForm(UserChangeForm):

    def __init__(self, *args, **kargs):
        super(CustomUserChangeForm, self).__init__(*args, **kargs)

    class Meta:
        model = CustomUser
        fields= '__all__'