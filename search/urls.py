from django.conf.urls import url
from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='search-home'),
    path('edit/<int:annotation>', views.edit, name='edit')
]