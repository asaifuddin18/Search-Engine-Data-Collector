import argparse
import pickle
import pandas as pd
from xgoogle.search import GoogleSearch, SearchError
import numpy as np
from urllib.parse import urlparse
import re
import urllib, sys, bs4
class LoadedModel():
    def __init__(self, path_to_model, queries, labels) -> None:
        self.model = path_to_model
        self.queries = queries
        self.labels = labels
        self.features = ['url_length', 'n_result', 'slash_count', 'dot_count', '.edu', '.com', '.gov', '.net', '.org', '.other', 'alexa_rank', 'keyword_in_netloc', 'keyword_in_path', 'keyword_in_title', 'keyword_in_description', 'first_person_pronoun_count']
        self.first_person_pronouns = ['i', 'we', 'me', 'us', 'my', 'mine', 'our', 'ours']
    
    def clean_links_title_and_desc(self, results, divs):
        '''
        Helper function that extracts the title and description of a list of divs from the Google search result page
        Parameters
        ----------
        results: xgoogle.search.SearchResult
            A search result object from xgoogle contining the title, url, and description
        divs: list(bs4.element)
            A list of bs4 elements representing divs from the Google search result page
        Returns
        -------
        list(bs4.element)
            A list of cleaned and formatted divs
        '''
        links = []
        titles = []
        descs = []
        for i in range(len(results)):
            if (results[i].url[0] == '/'):
                continue
            links.append(results[i].url)
            title_ = results[i].title.lower().strip()
            titles.append(re.sub(r'[^a-zA-Z0-9 ]', '', title_))
            desc_ = results[i].desc.lower().strip()
            descs.append(re.sub(r'[^a-zA-Z0-9 ]', '', desc_))
            if len(links) >=10:
                break
        return links, titles, descs



    def __construct_features(self, query) -> list():
        """
        Helper function that constructs the features required for the Random Forest
        Parameters
        ----------
        query: list(str)
            The query strings as per the search template
        Returns
        -------
        list
            A 2D list of features generated from the search query
        """
        full_query = ""
        for q in query:
            full_query += q.lower() + " "
        full_query = full_query.strip()
        gs = GoogleSearch(full_query)
        gs.results_per_page = 15
        results, divs = gs.get_results()
        urls, titles, descs = self.clean_links_title_and_desc(results, divs)
        feature_array = []
        for i in range(len(urls)):
            features = np.zeros((len(self.features),))
            formatted_url = "" + urls[i]
            cleaned = formatted_url.replace("http://www.","")
            cleaned = formatted_url.replace("https://www.","")
            slash_count = cleaned.count("/")
            dot_count = cleaned.count('.')
        
            formatted_url = formatted_url.lower()
        
            domain = str(urlparse(urls[i]).netloc)
            path = str(urlparse(urls[i]).path)
            for word in query:
                word_l = word.lower()
                if word_l in domain:
                    features[self.features.index("keyword_in_netloc")] += 1
                if word_l in path:
                    features[self.features.index("keyword_in_path")] += 1
                if word_l in titles[i]:
                    features[self.features.index("keyword_in_title")] += 1
                if word_l in descs[i]:
                    features[self.features.index("keyword_in_description")] += 1
        
            tld = urlparse(urls[i]).netloc.split('.')[-1]
            features[0] = len(formatted_url)
            features[1] = i
            features[2] = slash_count
            features[3] = dot_count
            try:
                features[self.features.index('alexa_rank')] = int(bs4.BeautifulSoup(urllib.request.urlopen("http://data.alexa.com/data?cli=10&dat=s&url="+ str(urls[i])).read(), "xml").find("REACH")['RANK'])
            except: #not in alexa rankings 
                features[self.features.index('alexa_rank')] = sys.maxsize
        
            if "."+tld in self.features:
                features[self.features.index("."+tld)] = 1
            else:
                features[self.features.index(".other")] = 1
        
            for word in descs[i].split(' '):
                if word in self.first_person_pronouns:
                    features[self.features.index("first_person_pronoun_count")] += 1
            feature_array.append(features)
        return feature_array

    def predict(self):
        full_data = []
        for i in range(len(self.queries)):
            feature_array = self.__construct_features(self.queries[i])
            for j in range(len(feature_array)):
                full_data.append(feature_array[j])
        return self.model.predict(full_data)

def main():
    parser = argparse.ArgumentParser(description="Loads a previously saved model & creates inferences based on ")
    parser.add_argument('--model_path', '-m', help="Path to downloaded ML pickle ", required=True)
    parser.add_argument('--test_data', '-t', help='Path to test data CSV file containing URLs & ground truths', required=True)
    args = parser.parse_args()
    model_path = args.model_path
    test_data = args.test_data
    file = open(model_path, 'rb')
    file.seek(0)
    df = pd.read_csv(test_data).replace(np.nan, '', regex=True)
    labels = []
    if 'labels' in df.columns:
        labels = list(df['labels'])
    q1, q2, q3, q4, q5, q6 = df['q1'], df['q2'], df['q3'], df['q4'], df['q5'], df['q6']
    queries = []
    for i in range(len(q1)):
        queries.append([q1[i], q2[i], q3[i], q4[i], q5[i], q6[i]])
    print(queries)
    loaded_model = LoadedModel(pickle.load(file), queries, labels)
    print(loaded_model.predict())

if __name__ == "__main__":
    main()
