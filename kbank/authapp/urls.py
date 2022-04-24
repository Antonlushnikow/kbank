from django.urls import path

from .views import (
    KbankUserLoginView,
    KbankUserLogoutView,
    KbankUserRegisterView,
    KbankUserUpdateView,
    KbankUserPasswordChangeView,
    KbankUserConfirmDeleteView,
)

import authapp.views as authapp


urlpatterns = [
    path('login/', KbankUserLoginView.as_view(), name='login'),
    path('logout/', KbankUserLogoutView.as_view(), name='logout'),
    path('register/', KbankUserRegisterView.as_view(), name='register'),
    path('update/<int:pk>', KbankUserUpdateView.as_view(), name='update-profile'),
    path('changepassword/', KbankUserPasswordChangeView.as_view(), name='change-password'),
    path('confirmdeleteprofile/', KbankUserConfirmDeleteView.as_view(), name='confirm-delete-profile'),
    path('verify/<str:email>/<str:activation_key>/', authapp.KbankUserRegisterView.verify, name='verify')
]
