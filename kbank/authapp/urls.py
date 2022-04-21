from django.urls import path

import authapp.views as authapp
from .views import KbankUserLoginView, KbankUserLogoutView, KbankUserRegisterView

urlpatterns = [
    path('login/', KbankUserLoginView.as_view(), name='login'),
    path('logout/', KbankUserLogoutView.as_view(), name='logout'),
    path('register/', KbankUserRegisterView.as_view(), name='register'),
    path('verify/<str:email>/<str:activation_key>/', authapp.KbankUserRegisterView.verify, name='verify')
]
