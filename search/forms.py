from django import forms

class QueryForm(forms.Form):
    your_object = forms.CharField(label='Your Object')
    your_queries = forms.CharField(label='Your Queries')
