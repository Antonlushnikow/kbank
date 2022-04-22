from django.contrib import auth
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import reverse, render
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView

from kbank import settings_dev
from .models import KbankUser
from .forms import KbankUserLoginForm, KbankUserRegistrationForm
from kbank.mixins import RedirectToPreviousMixin


class KbankUserLoginView(RedirectToPreviousMixin, LoginView):
    Model = KbankUser
    form_class = KbankUserLoginForm
    template_name = 'authapp/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(KbankUserLoginView, self).get_context_data()
        context['title'] = 'авторизация'
        return context


class KbankUserLogoutView(LogoutView):
    Model = KbankUser


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
        self.send_verify_mail(user)
        context = {}
        context['title'] = 'Активация аккаунта'
        context['user'] = user
        return render(self.request, 'authapp/verification_sent.html', context=context)
        # return HttpResponseRedirect(reverse('authapp:login'))

    def send_verify_mail(self, user):
        verify_link = reverse('auth:verify', args=[user.email, user.activation_key])
        title = f'Подтверждение учетной записи {user.username} на портале KBANK'
        message = f'Для подтверждения учетной записи {user.username} на портале \
        {settings_dev.DOMAIN_NAME} перейдите по ссылке: \n{settings_dev.DOMAIN_NAME}{verify_link}'
        send_mail(title, message, settings_dev.EMAIL_HOST_USER, [user.email], fail_silently=False)

    def verify(self, email, activation_key):
        try:
            user = KbankUser.objects.get(email=email)
            if user.activation_key == activation_key and not user.is_activation_key_expired():
                user.is_active = True
                user.save()
                auth.login(self, user)
                return render(self, 'authapp/verification.html')
            else:
                return render(self, 'authapp/verification.html')
        except Exception as e:
            print(e.with_traceback())
            return HttpResponseRedirect(reverse('index'))
