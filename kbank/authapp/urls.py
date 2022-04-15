from django.urls import path
from .views import KbankUserLoginView, KbankUserLogoutView

urlpatterns = [
    path('login/', KbankUserLoginView.as_view(), name='login'),
    path('logout/', KbankUserLogoutView.as_view(), name='logout'),
]
