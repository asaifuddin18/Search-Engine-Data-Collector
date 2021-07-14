from django.conf.urls import url
from django.urls import path
from . import views
from django.views.generic import TemplateView
urlpatterns = [
    path('', views.home, name='search-home'),
    path('edit/<str:annotation>', views.edit, name='edit'),
    path('your-object/your-queries', views.handle_input, name='input'),
    path('test', views.test, name='test'),
]