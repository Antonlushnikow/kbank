import hashlib
from random import random

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import KbankUser


class KbankUserLoginForm(AuthenticationForm):
    class Meta:
        model = KbankUser
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super(KbankUserLoginForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''


class KbankUserRegistrationForm(UserCreationForm):
    class Meta:
        model = KbankUser
        fields = ('username', 'first_name', 'last_name', 'email', 'info', 'avatar', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(KbankUserRegistrationForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''

    def save(self, commit=True):
        user = super(KbankUserRegistrationForm, self).save()
        user.is_active = False
        salt = hashlib.sha1(str(random()).encode('utf8')).hexdigest()[:6]
        user.activation_key = hashlib.sha1((user.email + salt).encode('utf8')).hexdigest()
        user.save()
        return user
