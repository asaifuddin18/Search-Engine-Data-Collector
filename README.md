# Search-Engine-Data-Collector

  

## Introduction

This repository contains code that launches a website allowing users to annotate Google Search results to find **source pages**

A **source page** is defined to be a website that holds specific information about an object. In the case of an professor, it could be their personal website or faculty website. In the case of a politician, it could be their official government website. The goal is to find the page that holds information specific to that object to prepare for data extraction.

## How to use

First, download the dependencies from requirements.txt. This can be accomplished by running the following command: pip install -r requirements.txt. Then, the website can be launched via the command: python manage.py runserver.
The website can be navigated a number of ways. Firstly, select the search template you want to use. Only 1 template may be used per website instance.
### Annotate 1 search query at a time
To annotate 1 search query at a time, input the search values in the input boxes displayed. The input boxes will tell you what types of values to input. Click submit when finished to go to the annotation page.
### Annotate 1 or more queries at a time
To annotate 1 or more queries at a time, the user must upload a properly formatted CSV file containing 1 or more queries. A properly formatted CSV file has the first line representing the search template as displayed by the website. Then, each search query value thereafter must follow that template declared in the CSV. Click submit when the CSV file has been uploaded.
### Annotation page
The annotation page will have the first 10 search results listed. The user can then click 'Not Hompage' or 'Homepage' buttons to assign a value to each search result. If this is not the first annotations, the model will attempt to classify the search results. The user can then annotate normally, opting to accept the model's inferences or override them. Click submit when finished annotating.
### Graphs
There are graphs on both the home page and the annotation page. These are to aid the user in how the model is training with the cumulative dataset. The metrics tracked on the line graph are accuracy, recall, precision, and f1 score. Each time the user annotates a set of websites, the models metrics are recorded and added to the graph. In addition, there is a pie chart displaying the number of hompage and non homepage URLs.
### Change Models
The user can change models whenever they are on the homepage. To change models, click the ML models dropdown and select the new model. The current models available are Random Forest and SVM.
### Download Dataset
The user can download the dataset generated so far by clicking the 'Download Dataset' button on the homepage. This will download the dataset in a CSV file with all the generated features as well as their corresponding labels & URLs.
### Download Model
The user can download the currently selected model by clicking the 'Download Model' button on the homepage. This will download the model to a pickle file.
  

## About

The website uses the Django framework along with Bootstrap for frontend. The graphs generated utilize Chart.js. The backend uses Scikit-learn to train and get inferences from ML generated models. Currently, the 2 models available for training are Random Forest and SVM.

## TODO

1. Implement more ML models (ME)

2. Collect lots of data

3. Make tab open in the same place (maybe as a pop-up?)

4. Add WHOIS data to features

5. Create wrapper for model & make it into python package

6. Add URLs to download dataset CSV