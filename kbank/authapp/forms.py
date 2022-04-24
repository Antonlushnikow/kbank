from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm, PasswordChangeForm
from django import forms
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


class KbankUserUpdateForm(UserChangeForm):
    password = None
    avatar = forms.FileField(label='Аватар', widget=forms.FileInput())

    class Meta:
        model = KbankUser
        fields = ('first_name', 'last_name', 'info', 'avatar')

    def __init__(self, *args, **kwargs):
        super(KbankUserUpdateForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''


class KbankUserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label='Старый пароль', widget=forms.PasswordInput())
    new_password1 = forms.CharField(label='Новый пароль', widget=forms.PasswordInput())
    new_password2 = forms.CharField(label='Еще раз новый пароль', widget=forms.PasswordInput())

    class Meta:
        model = KbankUser
        fields = ('old_password', 'new_password1', 'new_password2')

    def __init__(self, *args, **kwargs):
        super(KbankUserPasswordChangeForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''


class KbankUserConfirmDeleteForm(forms.Form):
    password = forms.CharField(label='Введите пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
