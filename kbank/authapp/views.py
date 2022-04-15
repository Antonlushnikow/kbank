from django.shortcuts import reverse
from django.contrib.auth.views import LoginView, LogoutView

from .models import KbankUser
from .forms import KbankUserLoginForm


class KbankUserLoginView(LoginView):
    Model = KbankUser
    form_class = KbankUserLoginForm
    template_name = 'authapp/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(KbankUserLoginView, self).get_context_data()
        context['title'] = 'авторизация'
        return context

    def get_success_url(self):
        return reverse('index')


class KbankUserLogoutView(LogoutView):
    Model = KbankUser

    def get_next_page(self):
        return reverse('index')
