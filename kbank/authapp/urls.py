from django.urls import path

import authapp.views as authapp

from .views import (
    KbankUserConfirmDeleteView,
    KbankUserLoginView,
    KbankUserLogoutView,
    KbankUserPasswordChangeView,
    KbankUserRegisterView,
    KbankUserUpdateView,
    block_user,
)

urlpatterns = [
    path("login/", KbankUserLoginView.as_view(), name="login"),
    path("logout/", KbankUserLogoutView.as_view(), name="logout"),
    path("register/", KbankUserRegisterView.as_view(), name="register"),
    path("update/<int:pk>", KbankUserUpdateView.as_view(), name="update-profile"),
    path(
        "changepassword/", KbankUserPasswordChangeView.as_view(), name="change-password"
    ),
    path(
        "confirmdeleteprofile/",
        KbankUserConfirmDeleteView.as_view(),
        name="confirm-delete-profile",
    ),
    path(
        "verify/<str:email>/<str:activation_key>/",
        authapp.KbankUserRegisterView.verify,
        name="verify",
    ),
    path("block/<int:pk>", block_user, name="block-user"),
]
