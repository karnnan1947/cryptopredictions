from django import forms
from .models import Algorithm,Coin,Duration

class Selectalgorithm(forms.Form):
    item=forms.ModelChoiceField(queryset=Algorithm.objects.all(),label='Algorithm')

class SelectCoin(forms.Form):
    item=forms.ModelChoiceField(queryset=Coin.objects.all(),label='Coin')

class SelectDuration(forms.Form):
    item=forms.ModelChoiceField(queryset=Duration.objects.all(),label='Duration')    