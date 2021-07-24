from django.conf.urls import url
from django.urls import path
from . import views
from django.views.generic import TemplateView
urlpatterns = [
    path('', views.home, name='search-home'),
    path('edit/<str:annotation>', views.edit, name='edit'),
    path('your-object/q1/q2/q3/q4/q5/q6', views.handle_input, name='input'),
    path('test', views.test, name='test'),
    path('download_dataset', views.download, name='download'),
    path('model/<str:model>/<str:features>', views.change_model, name='change_model'),
]