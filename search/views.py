from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse
from .forms import QueryForm
from .source.rf import RFCalculator
from .source.ngram_classification import NgramClassification
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup as Soup
import bs4
from .libraries.xgoogle.search import GoogleSearch, SearchError
import re
rf = NgramClassification()
current_queries = []
current_links = []
current_title_and_desc = []
current_object = ""

#def fetch_latest_query():



def clean_title_and_desc(title, desc):
    title_ = title.lower().strip()
    desc_ = desc.lower().strip()
    title_ = re.sub(r'[^a-zA-Z0-9]', '', title_) #this removes spaces, may need to be changed in the future if using a different feature method
    desc_ = re.sub(r'[^a-zA-Z0-9]', '', desc_)
    return title_, desc_


def download_urls(links):
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
        print("Downloaded", links[i])



def test(request):
    return render(request, 'search/base.html')


def home(request):
    context = {'stats_local': ['Total Stats', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A']}
    return render(request, 'search/home.html', context=context)
# Create your views here.
def edit(request, annotation): #this is submitting annotations
    truths = []
    for c in annotation:
        if c == '0':
            truths.append("not_homepage")
        else:
            truths.append(current_object + "_" + "homepage")
    
    #do rf stuff here
    global current_links
    global current_title_and_desc
    for i in range(len(current_links)):
        rf.add_datapoint(current_links[i], current_title_and_desc[i][1], truths[i], current_object, current_title_and_desc[i][0])
    
    if len(current_queries) != 0: #trying to annotate without any input check
        del current_queries[0]
        if len(current_queries) != 0:#ran out of queries
            try:
                gs = GoogleSearch(current_queries[0])
                gs.results_per_page = 15
                results, divs = gs.get_results()
                for i in range(len(divs)):
                    for descendant in divs[i].descendants:
                        if descendant != "" and descendant != " " and not isinstance(descendant, bs4.element.NavigableString) and descendant.has_attr('href'):
                            descendant['href'] = '#'
                    
                str_divs = [str(x) for x in divs]
                current_links.clear()
                current_title_and_desc.clear()
                for result in results:
                    if (result.url[0] == '/'):
                        continue
                    current_links.append(result.url)
                    current_title_and_desc.append(clean_title_and_desc(result.title, result.desc))
                    print("Title:", current_title_and_desc[-1][0])
                    print("Desc:", current_title_and_desc[-1][1])
                    if len(current_links) >=10:
                        break
                    
                print("num results:", len(current_links))
                #download_urls(current_links)
            except SearchError:
                return render(request, 'search/home.html') #probably change this to call edit() again
            
            predictions = rf.predict(current_links, [x[1] for x in current_title_and_desc], current_object, [x[0] for x in current_title_and_desc])
            labels = []
            for current in predictions:
                if current == "not_homepage":
                    labels.append(0)
                else:
                    labels.append(1)
            print("Predictions:", labels)
            data = rf.generate_random_forest()
            data.insert(0, current_object)
            return render(request, 'search/iframe_page.html', {'links': current_links, 'labels': labels, 'stats_local': data, 'divs': str_divs})
    data = rf.generate_random_forest()
    data.insert(0, 'Total Stats')
    return render(request, 'search/home.html', {'stats_local': data})

def handle_input(request):
    if request.method == 'POST':
        form = QueryForm(request.POST)
        if form.is_valid():
            
            queries = form['your_queries'].value().split('\n')
            for query in queries:
                if query != "":
                    current_queries.append(query.lower())
                    print("Query:", query)
            global current_object
            print(form['your_object'])
            current_object = "" + str(form['your_object'].value()).lower()
            if len(current_queries) != 0:
                global current_links
                try:
                    gs = GoogleSearch(current_queries[0])
                    gs.results_per_page = 11
                    results, divs_ = gs.get_results()
                    divs = []
                    for i in range(len(divs_)):
                        if not divs_[i].find('div', class_='H5U6Eb'): #images
                            divs.append(divs_[i])
                        
                        for descendant in divs[-1].descendants:
                            if descendant != "" and descendant != " " and not isinstance(descendant, bs4.element.NavigableString) and descendant.has_attr('href'):
                                descendant['href'] = '#'
                    if len(divs) > 10:
                        del divs[-1]
                        
                    str_divs = [str(x) for x in divs]
                    current_links.clear()
                    current_title_and_desc.clear()
                    for result in results:
                        if (result.url[0] == '/'):
                            continue
                        current_links.append(result.url)
                        current_title_and_desc.append(clean_title_and_desc(result.title, result.desc))
                        print("Title:", current_title_and_desc[-1][0])
                        print("Desc:", current_title_and_desc[-1][1])
                        if len(current_links) >=10:
                            break
                    
                    print("num results:", len(current_links))
                    #download_urls(current_links)
                except SearchError:
                    return render(request, 'search/home.html')
                    

                return render(request, 'search/iframe_page.html', {'links': current_links, 'stats_local': [current_object, 'N/A', 'N/A', 'N/A', 'N/A', 'N/A'], 'divs': str_divs})
    return render(request, 'search/home.html') #form failed

def url0(request):
    return render(request, 'search/url0.html')
def url1(request):
    return render(request, 'search/url1.html')
def url2(request):
    return render(request, 'search/url2.html')
def url3(request):
    return render(request, 'search/url3.html')
def url4(request):
    return render(request, 'search/url4.html')
def url5(request):
    return render(request, 'search/url5.html')
def url6(request):
    return render(request, 'search/url6.html')
def url7(request):
    return render(request, 'search/url7.html')
def url8(request):
    return render(request, 'search/url8.html')
def url9(request):
    return render(request, 'search/url9.html')
