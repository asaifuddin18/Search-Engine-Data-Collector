from django import forms
'''
Form object for user built query
'''
class QueryForm(forms.Form):
    your_object = forms.CharField(label='Your Object')
    #your_queries = forms.CharField(label='Your Queries')
    q1 = forms.CharField(label='q1', required=False)
    q2 = forms.CharField(label='q2', required=False)
    q3 = forms.CharField(label='q3', required=False)
    q4 = forms.CharField(label='q4', required=False)
    q5 = forms.CharField(label='q5', required=False)
    q6 = forms.CharField(label='q6', required=False)
'''
Form object for user to upload CSV file
'''
class UploadFileForm(forms.Form):
    file_object = forms.CharField(label='Your Object')
    file = forms.FileField()
    
