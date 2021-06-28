from django.conf.urls import url
from django.urls import path
from . import views
from django.views.generic import TemplateView
urlpatterns = [
    path('', views.home, name='search-home'),
    path('edit/<str:annotation>', views.edit, name='edit'),
    path('your-object/your-queries', views.handle_input, name='input'),
    path('test', views.test, name='test'),
    path('url0', views.url0, name='url0'),
    path('url1', views.url1, name='url1'),
    path('url2', views.url2, name='url2'),
    path('url3', views.url3, name='url3'),
    path('url4', views.url4, name='url4'),
    path('url5', views.url5, name='url5'),
    path('url6', views.url6, name='url6'),
    path('url7', views.url7, name='url7'),
    path('url8', views.url8, name='url8'),
    path('url9', views.url9, name='url9'),


]