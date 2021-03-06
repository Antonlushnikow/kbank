from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from authapp.views import KbankUserPasswordResetView, ProfileView
from kbank.sitemaps import KbankSitemap
from mainapp.views import (
    AboutUsView,
    ArticlesListView,
    CategoryListView,
    NotificationsListView,
    SiteSettingsEditView,
    TagListView,
)

sitemaps = {
    "aricles": KbankSitemap,
}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", ArticlesListView.as_view(), name="index"),
    path("article/", include(("mainapp.urls", "mainapp"), namespace="articles")),
    path("c/<slug:slug>/", CategoryListView.as_view(), name="category"),
    path("tag/<slug:slug>/", TagListView.as_view(), name="tag-list"),
    path("auth/", include(("authapp.urls", "authapp"), namespace="auth")),
    path("profile/<int:pk>", ProfileView.as_view(), name="profile-view"),
    path("accounts/", include("allauth.urls")),
    path("about-us-edit/", SiteSettingsEditView.as_view(), name="about-us-edit"),
    path("about-us/", AboutUsView.as_view(), name="about-us"),
    path(
        "moderation/",
        include(("moderationapp.urls", "moderationapp"), namespace="moderation"),
    ),
    path(
        "forgotpassword/", KbankUserPasswordResetView.as_view(), name="password_reset"
    ),
    path(
        "forgotpasswordsent/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="authapp/forgot-password-sent.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="authapp/reset-password-confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="authapp/reset-password-complete.html"
        ),
        name="password_reset_complete",
    ),
    path("notifications", NotificationsListView.as_view(), name="notifications-view"),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}),
    path("robots.txt", include("robots.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
