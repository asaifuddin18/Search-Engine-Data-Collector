from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse
from .forms import QueryForm, UploadFileForm
from .source.rf import RFCalculator
from .source.ngram_classification import NgramClassification
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup as Soup
import bs4
from .libraries.xgoogle.search import GoogleSearch, SearchError
import re
rf = NgramClassification()
current_links = []
current_title_and_desc = []
current_object = ""
past_data = []
data_x = []
past_accuracy = []
past_recall = []
past_precision = []
past_f1 = []
query = ""
queries = []
dict_t = {
    "Professor": ["First Name", "Last Name", "Institution"],
    "Movie": ["Name", "Year"],
    "Electronic": ["Name", "Model No./Year"],
    "Car": ["Make", "Model", "Year"]
}
'''def prune_divs(links, divs_):
    divs = []
    links_index = 0
    for i in range(len(divs_)):
        if len(divs) == 10:
            break
        for descendant in divs_[i].descendants:
            if descendant != "" and descendant != " " and not isinstance(descendant, bs4.element.NavigableString) and descendant.has_attr('href'):
                if descendant['href'] == links[links_index].url or links[links_index].url in descendant['href']:
                    descendant['href'] = '#'
                    divs.append(descendant)
                    links_index += 1
                    break
                else:
                    print(descendant['href'], links[links_index].url)
        else:
            print("Pruned a div\n")
    return divs'''

def clean_title_and_desc(title, desc):
    title_ = title.lower().strip()
    desc_ = desc.lower().strip()
    title_ = re.sub(r'[^a-zA-Z0-9]', '', title_) #this removes spaces, may need to be changed in the future if using a different feature method
    desc_ = re.sub(r'[^a-zA-Z0-9]', '', desc_)
    return title_, desc_

def set_links_title_desc(results, divs):
    str_divs = []
    global current_links
    global current_title_and_desc
    current_links.clear()
    current_title_and_desc.clear()
    for i in range(len(results)):
        #print(results[i].url)
        if (results[i].url[0] == '/'):
            continue
        current_links.append(results[i].url)
        current_title_and_desc.append(clean_title_and_desc(results[i].title, results[i].desc))
        for descendant in divs[i].descendants:
            if descendant != "" and descendant != " " and not isinstance(descendant, bs4.element.NavigableString) and descendant.has_attr('href'):
                descendant['href'] = current_links[-1]
                descendant['target'] = "_blank"
                descendant['rel'] = 'noopener noreferrer'
                
        str_divs.append(divs[i])
        if len(current_links) >=10:
            break
    return str_divs
                    


'''def download_urls(links):
    for i in range(len(links)):
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        webContent = requests.get(links[i], headers=headers).content.decode()
        soup = Soup(webContent)
        head = soup.find('head')
        base = soup.new_tag('base')
        base_url ='http://'+ urlparse(links[i]).netloc
        base['href'] = base_url
        head.insert(1, base)
        contents = '{% verbatim myblock %}' + str(soup) + '{% endverbatim myblock %}'
        with open('./search/templates/search/url' + str(i) + '.html', 'w') as f:
            f.write(contents)
        print("Downloaded", links[i])'''



def test(request):
    return render(request, 'search/base.html')


def home(request):
    context = {'model': rf.model, 'feature': rf.feature, 'num_datapoints': len(rf.labels), 'class_count': rf.get_class_count()}
    return render(request, 'search/home.html', context=context)
# Create your views here.
def edit(request, annotation): #this is submitting annotations
    truths = []
    for c in annotation:
        if c == '0':
            truths.append("not_homepage")
        else:
            truths.append(current_object + "_homepage")
    
    
    global current_links
    global current_title_and_desc
    global query
    for i in range(len(current_links)):
        rf.add_datapoint(current_links[i], current_title_and_desc[i][1], truths[i], current_object, current_title_and_desc[i][0], i, query)
    data = rf.generate_random_forest()
    past_accuracy.append(data[0])
    past_recall.append(data[1])
    past_precision.append(data[2])
    past_f1.append(data[3])
    data_x.append(len(past_accuracy))
    print(past_accuracy, past_recall, past_precision, past_f1)
    if len(queries) != 0:
        query = queries.pop(0)
        return handle_query(request)
    return render(request, 'search/home.html', {'stats_local': data, 'data_x': data_x, 
    'past_accuracy': past_accuracy, 'past_f1': past_f1, 'past_precision': past_precision, 
    'past_recall': past_recall, 'order': rf.classes, 'model': rf.model, 'feature': rf.feature, 'num_datapoints': len(rf.labels), 'class_count': rf.get_class_count(), 'object': current_object})

def handle_input(request):
    print("triggered")
    if request.method == 'POST':
        print("POST request")
        form = QueryForm(request.POST)
        if form.is_valid():
            global query
            query = str(form['q1'].value()) + " " + str(form['q2'].value()) + " " + str(form['q3'].value()) + " " + str(form['q4'].value()) + " " + str(form['q5'].value()) + " " + str(form['q6'].value())
            query = query.strip()
            global current_object
            current_object = "" + str(form['your_object'].value())
            return handle_query(request)
        else:
            return render(request, 'search/home.html', context={'error': 'Form submission not valid'})
    print(request.method)
    return render(request, 'search/home.html', context={'error': 'POST request was not made'})

def file_upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        
        if form.is_valid():
            global current_object
            current_object = str(form['file_object'].value())
            csv_file = request.FILES['file']
            if not csv_file.name.endswith('.csv'):
                return render(request, 'search/home.html', context={'error': 'File is not a CSV'})
            csv_data = csv_file.read().decode("utf-8")
            
            lines = list(map(str.rstrip, csv_data.split("\n")))
            if current_object not in dict_t: #error
                return render(request, 'search/home.html', context={'error': 'Object not in dict, update dic_t in views.py?'})
            input_names = lines[0].split(',')
            for i in range(len(dict_t[current_object])):
                if dict_t[current_object][i] != input_names[i]:
                    return render(request, 'search/home.html', context={'error': 'File is not formatted properly to the object'})

            for i in range(1, len(lines)):
                if lines[i] != "":
                    fields = []
                    for field in lines[i].split(','):
                        if field != "":
                            fields.append(field)
                    if len(fields) < len(dict_t[current_object]):# less fields than required
                        return render(request, 'search/home.html', context={'error': 'Not enough fields on line ' + str(i) + ' of the uploaded CSV'})
                    temp_query = ""
                    for field in fields:
                        temp_query += field + " "
                    temp_query = temp_query.strip()
                    queries.append(temp_query)
            print(queries)
        else:
            return render(request, 'search/home.html', context={'error': 'Form submission not valid'})
    else:
        return render(request, 'search/home.html', context={'error': 'POST request was not made'})
    if len(queries) == 0:
        print("no queries")
        return render(request, 'search/home.html', context={'error': 'File had no valid queries'})
    global query
    query = queries.pop(0)
    return handle_query(request)

def handle_query(request):
    try:
        gs = GoogleSearch(query)
        gs.results_per_page = 15
        results, divs = gs.get_results()
        str_divs_ = set_links_title_desc(results, divs)
        str_divs = str_divs = [str(x) for x in str_divs_]
    except SearchError:
        return render(request, 'search/home.html', context={'error': 'Error while using Google search engine with query: ' + query})
            
    labels = []
    if current_object + "_homepage" in rf.classes: #create annotations
        predictions = rf.predict(current_links, [x[1] for x in current_title_and_desc], current_object, [x[0] for x in current_title_and_desc], query)
        for current in predictions:
            if current == "not_homepage":
                labels.append(0)
            else:
                labels.append(1)

    return render(request, 'search/iframe_page.html', {'links': current_links,
     'divs': str_divs, 'labels': labels, 'model': rf.model, 'feature': rf.feature,'data_x': data_x, 
    'past_accuracy': past_accuracy, 'past_f1': past_f1, 'past_precision': past_precision, 
    'past_recall': past_recall, 'order': rf.classes, 'class_count': rf.get_class_count()})

def download_dataset(request):
    path = rf.download_dataset()
    response = HttpResponse(open(path, 'rb').read())
    response['Content-Type'] = 'text/plain'
    response['Content-Disposition'] = 'attachment; filename=search_dataset.csv'
    return response


def change_model(request, model):
    if 'ML Models' not in model:
        rf.model = model
    if not rf.is_empty():
        data = rf.generate_random_forest()
        past_accuracy.append(data[0])
        past_recall.append(data[1])
        past_precision.append(data[2])
        past_f1.append(data[3])
        data_x.append(len(past_accuracy))
       
            
    return render(request, 'search/home.html', {'data_x': data_x,
         'past_accuracy': past_accuracy, 'past_f1': past_f1, 'past_precision': past_precision,
          'past_recall': past_recall, 'order': rf.classes, 'num_datapoints': len(rf.labels), 'model': rf.model, 'feature': rf.feature,
          'class_count': rf.get_class_count(), 'object': current_object})

def download_model(request):
    if rf.is_empty():
        return render(request, 'search/home.html')
    path = rf.download_model()
    response = HttpResponse(open(path, 'rb').read())
    response['Content-Type'] = 'text/plain'
    response['Content-Disposition'] = 'attachment; filename=model.pickle'
    return response