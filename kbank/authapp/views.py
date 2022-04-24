from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import reverse, get_object_or_404, redirect, render
from django.contrib import auth
from django.core.mail import send_mail
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView

from kbank import settings
from .models import KbankUser
from .forms import (
    KbankUserLoginForm,
    KbankUserRegistrationForm,
    KbankUserUpdateForm,
    KbankUserPasswordChangeForm,
    KbankUserConfirmDeleteForm,
)
from kbank.mixins import RedirectToPreviousMixin


class KbankUserLoginView(RedirectToPreviousMixin, LoginView):
    Model = KbankUser
    form_class = KbankUserLoginForm
    template_name = 'authapp/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(KbankUserLoginView, self).get_context_data()
        context['title'] = 'авторизация'
        return context

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('/')
        return super(KbankUserLoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = get_object_or_404(KbankUser, username=form['username'].value())
        # print('dsfsdf' + form['username'].value())
        print(user.is_deleted)
        if user.is_deleted:
            return HttpResponseNotFound('Пользователь удален')
        return super(KbankUserLoginView, self).form_valid(form)


class KbankUserLogoutView(LoginRequiredMixin, LogoutView):
    model = KbankUser
    login_url = reverse_lazy('auth:login')


class KbankUserRegisterView(CreateView):
    Model = KbankUser
    form_class = KbankUserRegistrationForm
    template_name = 'authapp/registration.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('/')
        return super(KbankUserRegisterView, self).dispatch(request, *args, **kwargs)

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
      
    def send_verify_mail(self, user):
        verify_link = reverse('auth:verify', args=[user.email, user.activation_key])
        title = f'Подтверждение учетной записи {user.username} на портале KBANK'
        message = f'Для подтверждения учетной записи {user.username} на портале \
        {settings.DOMAIN_NAME} перейдите по ссылке: \n{settings.DOMAIN_NAME}{verify_link}'
        send_mail(title, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)

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


class KbankUserUpdateView(LoginRequiredMixin, UpdateView):
    model = KbankUser
    template_name = 'authapp/update.html'
    form_class = KbankUserUpdateForm
    login_url = reverse_lazy('auth:login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(KbankUserUpdateView, self).get_context_data()
        context['title'] = 'изменить профиль'
        return context

    def dispatch(self, request, *args, **kwargs):
        if KbankUser.objects.get(pk=kwargs['pk']).id == request.user.id or request.user.is_superuser:
            return super(KbankUserUpdateView, self).dispatch(request, *args, **kwargs)
        return redirect('/')

    def get_success_url(self):
        return reverse('profile-view', kwargs={'pk': self.request.user.pk})


class KbankUserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = KbankUserPasswordChangeForm
    template_name = 'authapp/change-password.html'
    login_url = reverse_lazy('auth:login')

    def get_success_url(self):
        return reverse('profile-view', kwargs={'pk': self.request.user.pk})


class ProfileView(DetailView):
    model = KbankUser
    template_name = 'authapp/profile.html'
    context_object_name = 'profile'

    def get_object(self):
        return get_object_or_404(KbankUser, pk=self.kwargs['pk'])


class KbankUserConfirmDeleteView(LoginRequiredMixin, FormView):
    model = KbankUser
    template_name = 'authapp/confirm-delete.html'
    form_class = KbankUserConfirmDeleteForm
    success_url = reverse_lazy('auth:confirm-delete-profile')
    login_url = reverse_lazy('auth:login')

    def get_object(self):
        return get_object_or_404(KbankUser, pk=self.kwargs['pk'])

    def form_valid(self, form):
        password = form['password'].value()

        if self.request.user.check_password(password):
            self.request.user.is_deleted = True
            self.success_url = reverse_lazy('auth:logout')
            self.request.user.save()
        return super(KbankUserConfirmDeleteView, self).form_valid(form)
