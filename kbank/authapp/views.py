from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import reverse, get_object_or_404, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView

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
        return HttpResponseRedirect(reverse('authapp:login'))


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
