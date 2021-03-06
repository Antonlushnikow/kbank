import hashlib
from random import random

from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
    UserChangeForm,
    UserCreationForm,
)

from .models import KbankUser


class KbankUserLoginForm(AuthenticationForm):
    """
    Форма аутентификации
    """
    captcha = ReCaptchaField(
        widget=ReCaptchaV2Checkbox, label="Подтвердите, что вы не робот!"
    )

    class Meta:
        model = KbankUser
        fields = ("username", "password")

    def __init__(self, *args, **kwargs):
        super(KbankUserLoginForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control mb-2"
            field.help_text = ""


class KbankUserRegistrationForm(UserCreationForm):
    """
    Форма регистрации
    """
    captcha = ReCaptchaField(
        widget=ReCaptchaV2Checkbox, label="Подтвердите что вы не робот!"
    )

    class Meta:
        model = KbankUser
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "info",
            "avatar",
            "password1",
            "password2",
        )

    def __init__(self, *args, **kwargs):
        super(KbankUserRegistrationForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control mb-2"
            if field.required:
                field.label_suffix = " (обязательное)"
            field.help_text = ""

    def save(self, commit=True):
        user = super(KbankUserRegistrationForm, self).save()
        user.is_active = False
        salt = hashlib.sha1(str(random()).encode("utf8")).hexdigest()[:6]
        user.activation_key = hashlib.sha1(
            (user.email + salt).encode("utf8")
        ).hexdigest()
        user.save()
        return user


class KbankUserUpdateForm(UserChangeForm):
    """
    Форма изменения данных пользователя
    """
    password = None
    avatar = forms.FileField(label="Аватар", widget=forms.FileInput())

    class Meta:
        model = KbankUser
        fields = ("first_name", "last_name", "info", "avatar")

    def __init__(self, *args, **kwargs):
        super(KbankUserUpdateForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
            field.help_text = ""


class KbankUserPasswordChangeForm(PasswordChangeForm):
    """
    Форма смены пароля
    """
    old_password = forms.CharField(label="Старый пароль", widget=forms.PasswordInput())
    new_password1 = forms.CharField(label="Новый пароль", widget=forms.PasswordInput())
    new_password2 = forms.CharField(
        label="Еще раз новый пароль", widget=forms.PasswordInput()
    )

    class Meta:
        model = KbankUser
        fields = ("old_password", "new_password1", "new_password2")

    def __init__(self, *args, **kwargs):
        super(KbankUserPasswordChangeForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
            field.help_text = ""


class KbankUserConfirmDeleteForm(forms.Form):
    """
    Форма подтверждения удаления пользователя
    """
    password = forms.CharField(
        label="Введите пароль",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )


class KbankUserPasswordResetForm(PasswordResetForm):
    """
    Форма сброса пароля
    """
    def __init__(self, *args, **kwargs):
        super(KbankUserPasswordResetForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
            field.help_text = ""
