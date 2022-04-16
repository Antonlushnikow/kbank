from django.http import HttpResponseRedirect
from django.shortcuts import reverse
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView

from .models import KbankUser
from .forms import KbankUserLoginForm, KbankUserRegistrationForm


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


class KbankUserRegisterView(CreateView):
    Model = KbankUser
    form_class = KbankUserRegistrationForm
    template_name = 'authapp/registration.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(KbankUserRegisterView, self).get_context_data()
        context['title'] = 'регистрация'
        return context

    def get_success_url(self):
        return reverse('authapp:login')

    def form_valid(self, form):
        user = form.save()
        return HttpResponseRedirect(reverse('authapp:login'))
