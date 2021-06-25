import numpy as np
import pandas as pd
import re
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from urllib.parse import urlparse
from .symmetric_dict import SymmetricDict

class RFCalculator:
    """
    Class used to organize data and make predictions using a Random Forest

    ...

    Attributes
    ----------
    features : list of strings
        A list of features used in the construction of the Random Forest
    labels: list of ints
        List of true values of URL
    df: DataFrame
        Pandas DataFrame that holds all the data
    rf: sklearn.ensemble RandomForestClassifier
        Random Forest Classifier object
    sd: SymmetricDictionary
        A symmetric dictionary so sd[k] = v == sd[v] = k
    idx: int
        The number of unique labels 1-indexed
    
    Methods
    -------

    """
    def __init__(self) -> None:
        self.features = ['length_of_url', 'urlHasName']
        self.labels = []
        self.df = pd.DataFrame(columns=self.features)
        self.rf = None
        self.sd = SymmetricDict()
        self.sd[0] = "not_homepage"
        self.idx = 1

        pass
    
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
        #features = [urlparse(url).netloc.split('.')[-1], len(url)]
        features = [len(url)]
        
        for current in object.split(' '):
            if re.search(current, url, re.IGNORECASE):
                features.append(True)
                break
        else:
            features.append(False)

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
        self.rf = RandomForestClassifier()
        self.rf.fit(train_features, train_labels)

        inferences = self.rf.predict(test_features)

        difference = train_labels - inferences #0 means either TP or TN, 1 means FN, -1 means FP

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
        
        d = {"recall": TP/(TP+FN), "specificity": TN/(TN+FP), "precision": TP/(TP+FP), "accuracy": (TP+TN)/(TP+TN+FP+FN)}
        d["f1"] = 2*(d["precision"] * d["recall"])/(d["precision"] + d["recall"])
        return d


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
        self.rf = RandomForestClassifier()

        self.rf.fit(data_train, self.labels)
        predictions = self.rf.predict(data_test)
        pred_string = []
        for num in predictions:
            if num not in self.sd:
                raise ValueError("Object not in symmetric dictionary on prediction")
            pred_string.append(self.sd[num])
        return pred_string





    