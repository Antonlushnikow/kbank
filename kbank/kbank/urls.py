from django.contrib import admin
from django.urls import path, include

from mainapp.views import ArticlesListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ArticlesListView.as_view(), name='index'),
    path('article/', include(('mainapp.urls', 'mainapp'), namespace='articles')),
    path('auth/', include(('authapp.urls', 'authapp'), namespace='auth')),
]
