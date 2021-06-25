from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse
from .forms import QueryForm
from .source.rf import RFCalculator
from googlesearch import search
rf = RFCalculator()
current_queries = []
current_links = []
current_object = ""

def test(request):
    return render(request, 'search/base.html')


def home(request):
    print(request.method)
    print(request.body)
    return render(request, 'search/home.html')
# Create your views here.
def edit(request, annotation): #this is submitting annotations
    print(annotation)
    truths = []
    for c in annotation:
        if c == '0':
            truths.append("not_homepage")
        else:
            truths.append(current_object + "_" + "homepage")
    
    #do rf stuff here
    global current_links
    for i in range(len(current_links)):
        rf.add_datapoint(current_links[i], "", truths[i], current_object)
    
    if len(current_queries) != 0: #trying to annotate without any input check
        del current_queries[0]
        if len(current_queries) != 0:#ran out of queries
            current_links = search(current_queries[0], 10)
            predictions = rf.predict(current_links, [], current_object)
            print(predictions)
            labels = []
            for current in predictions:
                if current == "not_homepage":
                    labels.append(0)
                else:
                    labels.append(1)
            print(labels)
            return render(request, 'search/iframe_page.html', {'links': current_links, 'object': current_object, 'labels': labels})
    return render(request, 'search/home.html')

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
                global current_links
                current_links = search(current_queries[0], 10)
                print(current_links)
                return render(request, 'search/iframe_page.html', {'links': current_links, 'object': current_object})
    return render(request, 'search/home.html') #form failed