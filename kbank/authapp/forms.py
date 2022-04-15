from django.contrib.auth.forms import AuthenticationForm
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
