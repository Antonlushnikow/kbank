from django.contrib import admin
from django.urls import path

from mainapp.views import ArticlesListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ArticlesListView.as_view()),

]
