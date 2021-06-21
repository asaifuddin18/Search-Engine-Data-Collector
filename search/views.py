from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse
from .forms import QueryForm
from .source.rf import RFCalculator
from googlesearch import search
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
rf = RFCalculator()
current_queries = []
current_object = ""
def home(request):
    context = {'posts': posts}
    print(request.method)
    print(request.body)
    return render(request, 'search/home.html', context)
# Create your views here.
def edit(request, annotation): #this is submitting annotations
    print(annotation)
    if len(current_queries) != 0: #trying to annotate without any input check
        del current_queries[0]
        if len(current_queries) != 0:#ran out of queries check
            return render(request, 'search/home.html', {'links': search(current_queries[0], 10), 'object': current_object})
    return HttpResponseRedirect('/')

def handle_input(request):
    if request.method == 'POST':
        form = QueryForm(request.POST)
        if form.is_valid():
            print("handled input")
            queries = form['your_queries'].value().split('\n')
            for query in queries:
                if query != "":
                    current_queries.append(query)
                    print(query)
            current_object = form['your_object']
            if len(current_queries) != 0:
                return render(request, 'search/home.html', {'links': search(current_queries[0], 10), 'object': current_object})
    
    return render(request, 'search/home.html') #form failed