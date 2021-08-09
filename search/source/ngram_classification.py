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

class NgramClassification:
    """
    Class used to organize data and make predictions using a Random Forest
    ...
    Attributes
    ----------
    features : list of strings
        The feature space of the model: all possible 3-grams starting with aaa, aab, ..., zzz
    labels: list of ints
        List of true values of URL
    df: DataFrame
        Pandas DataFrame that holds all the data
    sd: SymmetricDictionary
        A symmetric dictionary so sd[k] = v == sd[v] = k
    idx: int
        The number of unique labels 1-indexed
    model: str
        The current type of model being used
    feature: str
        The current feature extraction method
    
    Methods
    -------
    """
    def __init__(self) -> None:
        self.features = []
        self.labels = []
        self.classes = ['not_homepage']
        self.idx = 1 #remove in future (same as len(self.classes))
        self.model = "Random Forest"
        self.feature = "Term Frequency"
        self.engineer_features = ['url_length', 'n_result', 'slash_count', 'dot_count', '.edu', '.com', '.gov', '.net', '.org', '.other', 'alexa_rank', 'keyword_in_netloc', 'keyword_in_path', 'keyword_in_title', 'keyword_in_description']
        for f in self.engineer_features:
            self.features.append(f)
        #for c1 in ascii_lowercase:
        #    for c2 in ascii_lowercase:
        #        for c3 in ascii_lowercase:
        #            self.features.append(c1+c2+c3+'_u')
        #            self.features.append(c1+c2+c3+'_d')
        #            self.features.append(c1+c2+c3+'_t')

        self.df = pd.DataFrame(columns=self.features)
        pass

    def __generate_trigrams(self, formatted_url, description, title) -> list():
        """
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
    
    def __construct_features(self, url, description, object, title, n, query) -> list():
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
        formatted_url = re.sub(r'[^a-zA-Z]', '', formatted_url)
        formatted_url = formatted_url.lower()

        formatted_title = "" + title
        formatted_title = re.sub(r'[^a-zA-Z]', '', formatted_title)
        formatted_title = formatted_title.lower()

        formatted_desc = "" + description
        formatted_desc = re.sub(r'[^a-zA-Z]', '', formatted_desc)
        formatted_desc = formatted_desc.lower()

        #tri_grams = self.__generate_trigrams(formatted_url, formatted_desc, formatted_title)
        #for tri_gram in tri_grams:
        #    features[self.features.index(tri_gram)] += 1
        
        domain = str(urlparse(url).netloc)
        path = str(urlparse(url).path)
        query_words = query.split()
        for word in query_words:
            word_l = word.lower()
            if word_l in domain:
                features[self.features.index("keyword_in_netloc")] += 1
            if word_l in path:
                features[self.features.index("keyword_in_path")] += 1
            if word_l in formatted_title:
                features[self.features.index("keyword_in_title")] += 1
            if word_l in formatted_desc:
                features[self.features.index("keyword_in_description")] += 1
        
        tld = urlparse(url).netloc.split('.')[-1]
        features[0] = len(formatted_url)
        features[1] = n
        features[2] = slash_count
        features[3] = dot_count
        try:
            features[self.features.index('alexa_rank')] = int(bs4.BeautifulSoup(urllib.request.urlopen("http://data.alexa.com/data?cli=10&dat=s&url="+ str(url)).read(), "xml").find("REACH")['RANK'])
        except: #not in alexa rankings 
            features[self.features.index('alexa_rank')] = sys.maxsize
        print(features[self.features.index('alexa_rank')], "alexa rank")
        if "."+tld in self.features:
            features[self.features.index("."+tld)] = 1
        else:
            features[self.features.index(".other")] = 1


        return features

    def add_datapoint(self, url, description, label, object, title, n, query) -> None:
        """
        Parameters
        ----------
        url: str
            The URL of the datapoint
        snippet: str
            The text snippet that google provides under the URL in a google search
        label: string
            The ground-truth provided by the user
        object: string
            The name of the object
        """
        
        self.df.loc[len(self.df.index)] = self.__construct_features(url, description, object, title, n, query)
        if label not in self.classes:
            self.classes.append(label)
            self.idx += 1
        self.labels.append(self.classes.index(label))

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
        if self.feature == 'Term Frequency':
            print('tf')
            pass
        elif self.feature == 'Term Frequency * Mutual Information':
            features = self.tf_mi_array(features)
            print('tf_mi')
        elif self.feature == 'Term Frequency * Inverse Doc. Freq.':
            print('tf_idf')
            features = self.tf_mi_array(features)
        
        #tf_mi_features = self.tf_mi_array(features)
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


    def predict(self, urls, snippets, object, titles, query) -> list():
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
        Returns
        -------
        list:
            A list of predictions with the same length as the list of URLs
        """

        #generate features
        feature_list = []
        #df_t = pd.DataFrame(columns=self.features)
        #print(self.df)
        #data_test = np.array((len(urls), len(self.features)))
        data_test = []
        for i in range(len(urls)):
            data_test.append(self.__construct_features(urls[i], snippets[i], object, titles[i], i, query))
        data_test = np.array(data_test)
        data_train = np.array(self.df)
        if self.feature == 'Term Frequency':
            print('tf')
            pass
        elif self.feature == 'Term Frequency * Mutual Information':
            print('tf_mi')
            data_test = self.tf_mi_array(data_test)
            data_train = self.tf_mi_array(data_train)
        elif self.feature == 'Term Frequency * Inverse Doc. Freq.':
            print('tf_idf')
            data_test = self.tf_idf_array(data_test)
            data_train = self.tf_idf_array(data_train)
        #data_test_tf_mi = self.tf_mi_array(data_test)
        #data_train_tf_mi = self.tf_mi_array(data_train)
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
        #rf = RandomForestClassifier()

        #rf.fit(data_train, self.labels)
        #predictions = rf.predict(data_test)
        pred_string = []
        for num in inferences:
            if num >= len(self.classes):
                raise ValueError("Object not in symmetric dictionary on prediction")
            pred_string.append(self.classes[num])
        return pred_string

    def tf_mi_array(self, arr) -> np.array:
        """
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
        num_class = [0]*self.idx
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
        path = "search/temp/temp.csv"
        df_copy = self.df.copy()
        df_copy['labels'] = self.labels
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
        num_class = [0]*5
        for label in self.labels:
            num_class[label] += 1
        return num_class
    def download_model(self) -> str:
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

                

