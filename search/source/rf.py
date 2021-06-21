import numpy as np
import pandas as pd
import re
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from urllib.parse import urlparse

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
    
    Methods
    -------

    """
    def __init__(self) -> None:
        self.features = ['extension', 'length_of_url', 'urlHasName']
        self.labels = []
        self.df = pd.DataFrame(columns=self.features)

        pass
    
    def __construct_features(self, url, snippet) -> list():
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
        features = [urlparse(url).netloc.split('.')[-1], len(url)]
        
        for current in self.object.split(' '):
            if re.search(current, url, re.IGNORECASE):
                features.append(True)
                break
        else:
            features.append(False)



        return features

    def add_datapoint(self, url, snippet, label) -> None:
        """
        Parameters
        ----------
        url: str
            The URL of the datapoint
        snippet: str
            The text snippet that google provides under the URL in a google search
        label: The ground-truth provided by the user
        """

        self.df.loc[len(self.df.index)] = self.__construct_features(url, snippet)
        self.labels.append(label)

    def generate_random_forest(self) -> dict:
        """
        Function that trains and tests Random Forest

        Returns
        -------
        dict
            A dictionary containing the following keys: recall, specificity, precision, accuracy, f1
        """

        data = pd.get_dummies(self.df)
        features = np.array(data)
        train_features, test_features, train_labels, test_labels = train_test_split(features, self.labels, test_size = .2) #Is this too expensive?
        clf = RandomForestClassifier()
        clf.fit(train_features, train_labels)

        inferences = clf.predict(test_features)

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





    