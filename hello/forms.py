from django import forms

class NutritionForm(forms.Form):
    serving_size = forms.CharField(max_length=100)
    food = forms.CharField(max_length=100)
