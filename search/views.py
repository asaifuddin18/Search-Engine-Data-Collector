from django.shortcuts import render
from django.http import HttpResponse

posts = [{
    'author': 'CoreyMS',
    'title': 'Search result 1',
    'content': 'First search content',
    'date_posted': 'August 27, 2018'},
{'author': 'Jane Doe',
'title': 'Search result 2',
'content': 'second search content',
'date_posted': 'August 28, 2018'},
{'author': 'Aziz S',
'title': 'Search result 3',
'content': 'third search content',
'date_posted': 'August 29, 2018'}]

def home(request):
    context = {'posts': posts, 'title': 'This is the title'}
    return render(request, 'search/home.html', context)
# Create your views here.
