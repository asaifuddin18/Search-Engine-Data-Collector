import numpy as np
from numpy.lib import tracemalloc_domain
import pandas as pd
import re
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from urllib.parse import urlparse
from .symmetric_dict import SymmetricDict
from string import ascii_lowercase

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
    
    Methods
    -------

    """
    def __init__(self) -> None:
        self.features = []
        self.labels = []
        self.sd = SymmetricDict()
        self.sd[0] = "not_homepage"
        self.idx = 1
        for c1 in ascii_lowercase:
            for c2 in ascii_lowercase:
                for c3 in ascii_lowercase:
                    self.features.append(c1+c2+c3)

        self.df = pd.DataFrame(columns=self.features)
        pass

    def __generate_trigrams(self, formatted_url) -> list():
        """
        Helper function that constructs the tri-grams required for feature generation

        Parameters
        ----------
        formatted_url: str
            The new string of the url, lowercase and containing only letters

        Returns
        list
            A list of strings of the tri-grams generated from the url
        """
        tri_grams = []
        for i in range(2, len(formatted_url)):
            tri_grams.append(formatted_url[i-2] + formatted_url[i-1] + formatted_url[i])
        
        return tri_grams
    
    def __construct_features(self, url, snippet, object) -> list():
        """
        Helper function that constructs the features required for the Random Forest

        Parameters
        ----------
        url: str
            The URL of the datapoint
        snippet: str
            The text snippet that google provides under the URL in a google search

        Returns
        -------
        list
            A list of features generated from the URL and the snippet
        """
        features = np.zeros((17576,))
        formatted_url = "" + url
        formatted_url = re.sub(r'[^a-zA-Z]', '', formatted_url)
        formatted_url = formatted_url.lower()
        tri_grams = self.__generate_trigrams(formatted_url)
        for tri_gram in tri_grams:
            features[self.features.index(tri_gram)] += 1


        return features

    def add_datapoint(self, url, snippet, label, object) -> None:
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
        
        self.df.loc[len(self.df.index)] = self.__construct_features(url, snippet, object)
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

        data = pd.get_dummies(self.df) #probably have to do the same with labels
        features = np.array(data)
        train_features, test_features, train_labels, test_labels = train_test_split(features, self.labels, test_size = .2) #Is this too expensive?
        rf = RandomForestClassifier()
        rf.fit(train_features, train_labels)

        inferences = rf.predict(test_features)

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
        if precision == 'N/A' or recall == 'N/A':
            f1 = 'N/A'
        else:
            f1 = round(2*(precision * recall)/(precision + recall), 2)

        #to_return = [(TP+TN)/(TP+TN+FP+FN), TP/(TP+FN), TN/(TN+FP), TP/(TP+FP)]
        #to_return.append(2*(to_return[3] * to_return[1])/(to_return[3] + to_return[1]))
        return [accuracy, recall, specificity, precision, f1]


    def predict(self, urls, snippets, object) -> list():
        """
        Creates predictions based on input URLs

        Parameters
        ----------
        urls: list
            A list of URLs to cast predictions on
        snippets: list
            A list of strings that re the snippets google returns alongside URLs on search queries

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
            data_test.append(self.__construct_features(urls[i], "", object))
        data_test = np.array(data_test)
        data_train = np.asarray(self.df)
        rf = RandomForestClassifier()

        rf.fit(data_train, self.labels)
        predictions = rf.predict(data_test)
        pred_string = []
        for num in predictions:
            if num not in self.sd:
                raise ValueError("Object not in symmetric dictionary on prediction")
            pred_string.append(self.sd[num])
        return pred_string





    