import numpy as np
from numpy.lib import tracemalloc_domain
from numpy.lib.function_base import average
import pandas as pd
import re
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
import sklearn
from urllib.parse import urlparse
import urllib, sys, bs4
from string import ascii_lowercase
import math
import pickle
from os.path import exists
class MLModel:
    """
    Class used to organize data and make predictions using a selected Machine Learning model
    ...
    Attributes
    ----------
    features : list of strings
        The feature space of the model: all possible 3-grams starting with aaa, aab, ..., zzz
    labels: list of ints
        List of true values of URL
    df: DataFrame
        Pandas DataFrame that holds all the data
    model: str
        The current type of model being used
    first_person_pronouns
        A list of predefined first person pronouns to detect in a given Google search result description
    urls: list of strings
        The list of URLs from the Google Search Page
    Methods
    -------
    """
    def __init__(self) -> None:
        self.labels = []
        self.model = "Random Forest"
        self.words = []
        self.features = ['url_length', 'n_result', 'slash_count', 'dot_count', '.edu', '.com', '.gov', '.net', '.org', '.other', 'alexa_rank', 'keyword_in_netloc', 'keyword_in_path', 'keyword_in_title', 'keyword_in_description', 'first_person_pronoun_count']
        self.first_person_pronouns = ['i', 'we', 'me', 'us', 'my', 'mine', 'our', 'ours']
        self.info = []
        self.urls = []
        if exists("search/data/dataset.csv"): #this only allows 1 type of entity to be searched, change it, perhaps create file on first search & pass entity through
            self.df = pd.from_csv("search/data/dataset.csv")
            self.labels = list(self.df['labels'])
            self.urls = list(self.df['urls'])
            del self.df['urls']
            del self.df['labels']
            self.features = list(self.df.columns)
        else:
            self.df = pd.DataFrame(columns=self.features)
        if exists("search/data/info.pickle"):
            with open("search/data/info.pickle") as f:
                f.seek(0)
                self.info = pickle.load(f)
        pass
    
    def add_word(self, word):
        if word.lower() not in self.words:
            self.words.append(word.lower())
            self.features.append(word.lower())
            self.df[word.lower()] = 0
        for i in range(len(self.data)):
            for val in self.data[i]:
                self.df.at[i, word] = val.count(word)

    def __generate_trigrams(self, formatted_url, description, title) -> list():
        """
        DEPRECATED
        Helper function that constructs the tri-grams required for feature generation
        Parameters
        ----------
        formatted_url: str
            The new string of the url, lowercase and containing only letters
        description: str
            The text snippet that google provides under the URL in a google search
        title: str
            The text that appears hyperlinked
        Returns
        -------
        list
            A list of strings of the tri-grams generated from the url
        """
        tri_grams = []
        for i in range(2, len(formatted_url)):
            tri_grams.append(formatted_url[i-2] + formatted_url[i-1] + formatted_url[i] + '_u')
        for i in range(2, len(description)):
            tri_grams.append(description[i-2] + description[i-1] + description[i] + '_d')
        for i in range(2, len(title)):
            tri_grams.append(title[i-2] + title[i-1] + title[i] + '_t')
        
        return tri_grams
    
    def __construct_features(self, url, description, title, n, query) -> list():
        """
        Helper function that constructs the features required for the Random Forest
        Parameters
        ----------
        url: str
            The URL of the datapoint
        description: str
            The text snippet that google provides under the URL in a google search
        title: str
            The text that appears hyperlinked
        n: int
            The index that the Google search result is within the page
        query: string
            The original query that the user inputted
        Returns
        -------
        list
            A list of features generated from the URL and the snippet
        """
        features = np.zeros((len(self.features),))
        formatted_url = "" + url
        cleaned = formatted_url.replace("http://www.","")
        cleaned = formatted_url.replace("https://www.","")
        slash_count = cleaned.count("/")
        dot_count = cleaned.count('.')
        
        formatted_url = formatted_url.lower()
        
        domain = str(urlparse(url).netloc)
        path = str(urlparse(url).path)
        query_words = query.split()
        for word in query_words:
            word_l = word.lower()
            if word_l in domain:
                features[self.features.index("keyword_in_netloc")] += 1
            if word_l in path:
                features[self.features.index("keyword_in_path")] += 1
            if word_l in title:
                features[self.features.index("keyword_in_title")] += 1
            if word_l in description:
                features[self.features.index("keyword_in_description")] += 1
        for word in self.words:
            features[self.features.index(word)] += domain.count(word) + path.count(word) + title.count(word) + description.count(word)
            
        tld = urlparse(url).netloc.split('.')[-1]
        features[0] = len(formatted_url)
        features[1] = n
        features[2] = slash_count
        features[3] = dot_count
        self.info.append([url, title, description])
        try:
            features[self.features.index('alexa_rank')] = int(bs4.BeautifulSoup(urllib.request.urlopen("http://data.alexa.com/data?cli=10&dat=s&url="+ str(url)).read(), "xml").find("REACH")['RANK'])
        except: #not in alexa rankings 
            features[self.features.index('alexa_rank')] = sys.maxsize
        
        if "."+tld in self.features:
            features[self.features.index("."+tld)] = 1
        else:
            features[self.features.index(".other")] = 1
        
        for word in description.split(' '):
            if word in self.first_person_pronouns:
                features[self.features.index("first_person_pronoun_count")] += 1


        return features

    def add_datapoint(self, url, description, label, title, n, query) -> None:
        """
        Parameters
        ----------
        url: str
            The URL of the datapoint
        description: str
            The text description that google provides under the URL in a google search
        label: string
            The ground-truth provided by the user
        title: str
            The title of the Google search result
        n: The index the Google search result within the page
        query: str
            The query inputted by the user
        """
        
        self.df.loc[len(self.df.index)] = self.__construct_features(url, description, title, n, query)
        self.labels.append(label)
        self.urls.append(url)
        self.df.to_csv("search/data/dataset.csv")
        pickle.dump(self.info, open("search/data/info.pickle", 'wb'))


    def generate_random_forest(self) -> dict:
        """
        Function that trains and tests Random Forest
        Returns
        -------
        dict
            A dictionary containing the following keys: recall, specificity, precision, accuracy, f1
        """

        #data = pd.get_dummies(self.df) #probably have to do the same with labels
        features = np.array(self.df)
        
        train_features, test_features, train_labels, test_labels = train_test_split(features, self.labels, test_size = .3) #Is this too expensive?
        inferences = []
        if self.model == 'Random Forest':
            print('rf')
            rf = RandomForestClassifier()
            rf.fit(train_features, train_labels)
            inferences = rf.predict(test_features)
        elif self.model == 'SVM':
            print('svm')
            svm = make_pipeline(StandardScaler(), SVC(gamma='auto'))
            svm.fit(train_features, train_labels)
            inferences = svm.predict(test_features)

        f1 = sklearn.metrics.f1_score(test_labels, inferences, zero_division=0)
        recall = sklearn.metrics.recall_score(test_labels, inferences, zero_division=0)
        precision = sklearn.metrics.precision_score(test_labels, inferences, zero_division=0)
        accuracy = sklearn.metrics.accuracy_score(test_labels, inferences)
        return [accuracy, recall, precision, f1]


    def predict(self, urls, snippets, titles, query) -> list():
        """
        Creates predictions based on input URLs
        Parameters
        ----------
        urls: list
            A list of URLs to cast predictions on
        snippets: list
            A list of strings that are the descriptions google returns alongside URLs on search queries
        titles: list
            A list of titles that are hyperlinked to the URL returned upon search queries
        query: str
            The query inputted by the user
        Returns
        -------
        list:
            A list of predictions with the same length as the list of URLs
        """

        data_test = []
        for i in range(len(urls)):
            data_test.append(self.__construct_features(urls[i], snippets[i], titles[i], i, query))
        data_test = np.array(data_test)
        data_train = np.array(self.df)
        inferences = []
        if self.model == 'Random Forest':
            print('rf')
            rf = RandomForestClassifier()
            rf.fit(data_train, self.labels)
            inferences = rf.predict(data_test)
        elif self.model == 'SVM':
            print('svm')
            svm = make_pipeline(StandardScaler(), SVC(gamma='auto'))
            svm.fit(data_train, self.labels)
            inferences = svm.predict(data_test)
        return inferences.tolist()

    def tf_mi_array(self, arr) -> np.array:
        """
        DEPRECATED
        Creates tf.mi array
        Parameters
        ----------
        arr: np.array
            The numpy array given when converting the pandas term-frequency dataframe into a numpy array
        Returns
        -------
        np.array:
            A numpy array of same dimensions of the input array except with tf.mi values filled in
        """
        num_class = [0, 0]
        for label in self.labels:
            num_class[label] += 1
        

        freq_array = np.zeros((self.idx, len(self.features), 4)) #0th dim = class, 1st dim = tri-gram, 2nd dim = a,b,c,d

        for i in range(len(arr)):
            for j in range(len(self.engineer_features), len(arr[i])):
                if arr[i][j] != 0:
                    freq_array[self.labels[i]][j][0] += 1 #a
                    temp = np.arange(self.idx)
                    temp = np.delete(temp, self.labels[i])
                    #freq_array[temp][j][2] += 1 #c
                    freq_array[temp,j,2] += 1 #c
                #else:
                    #freq_array[self.labels[i]][j][1] += 1 #b
                    #temp = np.arange(self.idx)
                    #temp = np.delete(temp, self.labels[i])
                    #freq_array[temp,j,3] += 1 #d

        tf_mi_arr = np.zeros((len(arr), len(arr[0])))
        for i in range(len(arr)):
            for j in range(len(arr[i])):
                if j < len(self.engineer_features):
                    tf_mi_arr[i][j] = arr[i][j]
                    continue
                a = freq_array[self.labels[i]][j][0]
                c = freq_array[self.labels[i]][j][2]
                n1 = self.labels.count(self.labels[i])
                n2 = len(self.labels) - n1
                n = len(self.labels)
                if a + c == 0 or (n1 == 0 and n2 == 0):
                    tf_mi_arr[i][j] = 0
                    continue
                v1 = (a*n)/((a+c)*n1)
                v2 = (c*n)/((a+c)*n2)
                tf_mi_arr[i][j] = math.log2(max(v1, v2))*arr[i][j]
        return tf_mi_arr


    def tf_idf_array(self, arr) -> np.array:
        """
        DEPRECATED
        Creates tf.idf array
        Parameters
        ----------
        arr: np.array
            The numpy array given when converting the pandas term-frequency dataframe into a numpy array
        Returns
        -------
        np.array:
            A numpy array of same dimensions of the input array except with tf.mi values filled in
        """
        num_class = [0]*self.idx
        for label in self.labels: #raw number of datapoints per class
            num_class[label] += 1
        

        freq_array = np.zeros((self.idx, len(self.features), 4)) #0th dim = class, 1st dim = tri-gram, 2nd dim = a,b,c,d

        for i in range(len(arr)): #datapoint
            for j in range(len(self.engineer_features), len(arr[i])): #features
                if arr[i][j] != 0:
                    freq_array[self.labels[i]][j][0] += 1 #a
                    temp = np.arange(self.idx)
                    temp = np.delete(temp, self.labels[i])
                    freq_array[temp,j,2] += 1 #c

        tf_idf_arr = np.zeros((len(arr), len(arr[0])))
        for i in range(len(arr)):
            for j in range(len(arr[i])):
                if j < len(self.engineer_features):
                    tf_idf_arr[i][j] = arr[i][j]
                    continue
                
                a = freq_array[self.labels[i]][j][0]
                c = freq_array[self.labels[i]][j][2]
                n = len(self.labels)
                if a + c == 0:
                    tf_idf_arr[i][j] = 0
                    continue
                tf_idf_arr[i][j] = math.log2(n/(a+c))*arr[i][j]
        return tf_idf_arr

    def download_dataset(self) -> str:
        """
        Downloads data to a CSV file (term frequency features)
        Returns
        -------
        str:
            A string to the path of the newly created file
        """
        path = "search/data/dataset.csv"
        df_copy = self.df.copy()
        df_copy['labels'] = self.labels
        df_copy['urls'] = self.urls
        df_copy.to_csv(path)
        return path

    def is_empty(self) -> bool:
        """
        Checks to see if the classifier has no data
        Returns
        -------
        bool:
            True if there is no data, false otherwise
        """
        return len(self.labels) == 0

    def get_class_count(self):
        '''
        Gets the frequency of not_hompage and homepage
        Returns
        -------
        list:
            List of size 2, index 0 = frequency of not_homepage, index 1 = frequency of homepage
        '''
        #num_class = [0, 0]
        #for label in self.labels:
        #    num_class[label] += 1
        #return num_class
        s = sum(self.labels)
        return [len(self.labels) - s, s]
    def download_model(self) -> str:
        '''
        Converts the Scikit-learn model into a pickle file
        Returns
        -------
        str:
            A string of the path to the created pickle file
        '''
        path = "search/temp/temp_model.pickle"
        data_train = np.array(self.df)
        model = ""
        if self.model == 'Random Forest':
            print('rf')
            model = RandomForestClassifier()
            model.fit(data_train, self.labels)
        elif self.model == 'SVM':
            print('svm')
            model = make_pipeline(StandardScaler(), SVC(gamma='auto'))
            model.fit(data_train, self.labels)
        pickle.dump(model, open(path, 'wb'))
        return path

    def get_url_and_labels(self) -> tuple(str, int):
        '''
        Retrieves URL and labels as tuple
        Returns
        -------
        tuple(str, int):
            A tuple of the URL and label of datapoint
        '''
        return (self.urls, self.labels)
