from django import forms

class PexelsSearchForm(forms.Form):
    query = forms.CharField(label="Search Images", max_length=100)