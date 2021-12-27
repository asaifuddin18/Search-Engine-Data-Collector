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
    #The main page of the website, asks for search query
    path('', views.home, name='search-home'),
    #URL to submit annotations if user adds custom words to model
    path('edit/<str:annotation>/<str:words>', views.edit, name='edit'),
    #URL to submit annotations if user does not add custom words to model
    path('edit/<str:annotation>/', views.no_words, name='no_words'),
    #URL to send search query to model
    path('your-object/q1/q2/q3/q4/q5/q6', views.handle_input, name='input'),
    #URL to request dataset download
    path('download_dataset/', views.download_dataset, name='download_dataset'),
    #URL to change model type
    path('model/<str:model>/', views.change_model, name='change_model'),
    #URL to request model download as pickle file
    path('download_model/', views.download_model, name='download_model'),
    #URL to upload a CSV for multiple search queries
    path('file-object/file', views.file_upload, name='file_upload')
]