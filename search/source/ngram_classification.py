import numpy as np
from numpy.lib import tracemalloc_domain
import pandas as pd
import re
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from urllib.parse import urlparse
from .symmetric_dict import SymmetricDict
from string import ascii_lowercase
import math

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
        self.sd = SymmetricDict()
        self.sd[0] = "not_homepage"
        self.idx = 1
        self.model = "Random Forest"
        self.feature = "Term Frequency * Mutual Information"
        for c1 in ascii_lowercase:
            for c2 in ascii_lowercase:
                for c3 in ascii_lowercase:
                    self.features.append(c1+c2+c3+'_u')
                    self.features.append(c1+c2+c3+'_d')
                    self.features.append(c1+c2+c3+'_t')

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
    
    def __construct_features(self, url, description, object, title) -> list():
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
        features = np.zeros((17576*3,))
        formatted_url = "" + url
        formatted_url = re.sub(r'[^a-zA-Z]', '', formatted_url)
        formatted_url = formatted_url.lower()

        formatted_title = "" + title
        formatted_title = re.sub(r'[^a-zA-Z]', '', formatted_title)
        formatted_title = formatted_title.lower()

        formatted_desc = "" + description
        formatted_desc = re.sub(r'[^a-zA-Z]', '', formatted_desc)
        formatted_desc = formatted_desc.lower()

        tri_grams = self.__generate_trigrams(formatted_url, formatted_desc, formatted_title)
        for tri_gram in tri_grams:
            features[self.features.index(tri_gram)] += 1


        return features

    def add_datapoint(self, url, description, label, object, title) -> None:
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
        
        self.df.loc[len(self.df.index)] = self.__construct_features(url, description, object, title)
        if label not in self.sd:
            self.sd[label] = self.idx
            self.idx += 1
        self.labels.append(self.sd[label])

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
        train_features, test_features, train_labels, test_labels = train_test_split(features, self.labels, test_size = .2) #Is this too expensive?
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

        difference = test_labels - inferences #0 means either TP or TN, 1 means FN, -1 means FP

        TP = 0
        TN = 0
        FP = 0
        FN = 0
        for i in range(len(difference)):
            if difference[i] == 1:
                FN += 1
            elif difference[i] == -1:
                FP += 1
            else:
                if train_labels[i] == 1:
                    TP += 1
                else:
                    TN += 1
        
        #d = {"recall": TP/(TP+FN), "specificity": TN/(TN+FP), "precision": TP/(TP+FP), "accuracy": (TP+TN)/(TP+TN+FP+FN)}
        #d["f1"] = 2*(d["precision"] * d["recall"])/(d["precision"] + d["recall"])
        #return d
        accuracy = 0
        recall = 0
        specificity = 0
        precision = 0
        f1 = 0
        if TP + TN + FP + FN == 0:
            accuracy = 'N/A'
        else:
            accuracy = round((TP+TN)/(TP+TN+FP+FN), 2)
        if TP + FN == 0:
            recall = 'N/A'
        else:
            recall = round(TP/(TP+FN),2)
        if TN + FP == 0:
            specificity = 'N/A'
        else:
            specificity = round(TN/(TN+FP), 2)
        if TP + FP == 0:
            precision = 'N/A'
        else:
            precision = round(TP/(TP+FP), 2)
        if precision == 'N/A' or recall == 'N/A' or (precision == 0 and recall == 0):
            f1 = 'N/A'
        else:
            f1 = round(2*(precision * recall)/(precision + recall), 2)

        #to_return = [(TP+TN)/(TP+TN+FP+FN), TP/(TP+FN), TN/(TN+FP), TP/(TP+FP)]
        #to_return.append(2*(to_return[3] * to_return[1])/(to_return[3] + to_return[1]))
        return [accuracy, recall, specificity, precision, f1]


    def predict(self, urls, snippets, object, titles) -> list():
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
            data_test.append(self.__construct_features(urls[i], snippets[i], object, titles[i]))
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
            if num not in self.sd:
                raise ValueError("Object not in symmetric dictionary on prediction")
            pred_string.append(self.sd[num])
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
        

        freq_array = np.zeros((self.idx, 17576*3, 4)) #0th dim = class, 1st dim = tri-gram, 2nd dim = a,b,c,d

        for i in range(len(arr)):
            for j in range(len(arr[i])):
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
        for label in self.labels:
            num_class[label] += 1
        

        freq_array = np.zeros((self.idx, 17576*3, 4)) #0th dim = class, 1st dim = tri-gram, 2nd dim = a,b,c,d

        for i in range(len(arr)):
            for j in range(len(arr[i])):
                if arr[i][j] != 0:
                    freq_array[self.labels[i]][j][0] += 1 #a
                    temp = np.arange(self.idx)
                    temp = np.delete(temp, self.labels[i])
                    freq_array[temp,j,2] += 1 #c

        tf_idf_arr = np.zeros((len(arr), len(arr[0])))
        for i in range(len(arr)):
            for j in range(len(arr[i])):
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
        self.df.to_csv(path)
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

                

