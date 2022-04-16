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
