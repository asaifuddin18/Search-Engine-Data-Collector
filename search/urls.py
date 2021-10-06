from django.conf.urls import url
from django.urls import path
from . import views
from django.views.generic import TemplateView
'''
URL: '', home page of the website
URL: 'edit/<str:annotaion>', url to be entered upon annotation submission where str: annotation is a string of 0s and 1s
URL: 'download_dataset/', url to be entered when user clicks download dataset button
URL: 'model/<str:model>/, url to be entered when user attemps to change the current ML model
URL: 'download_model/', url to be entered when user clicks download model button
URL: 'file-object/file', url to be entered when user uploads and submits a CSV file via POST request
'''
urlpatterns = [
    path('', views.home, name='search-home'),
    path('edit/<str:annotation>/<str:words>', views.edit, name='edit'),
    path('your-object/q1/q2/q3/q4/q5/q6', views.handle_input, name='input'),
    path('download_dataset/', views.download_dataset, name='download_dataset'),
    path('model/<str:model>/', views.change_model, name='change_model'),
    path('download_model/', views.download_model, name='download_model'),
    path('file-object/file', views.file_upload, name='file_upload')
]