from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from mainapp.views import ArticlesListView, CategoryListView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ArticlesListView.as_view(), name='index'),
    path('article/', include(('mainapp.urls', 'mainapp'), namespace='articles')),
    path('<slug:slug>/', CategoryListView.as_view(), name='category'),
    path('auth/', include(('authapp.urls', 'authapp'), namespace='auth')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
