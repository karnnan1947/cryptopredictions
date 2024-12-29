from django import forms
from .models import Algorithm,Coin,Duration

class Selectalgorithm(forms.Form):
    algorithm=forms.ModelChoiceField(queryset=Algorithm.objects.all(),label='Algorithm')

class SelectCoin(forms.Form):
    coin=forms.ModelChoiceField(queryset=Coin.objects.all(),label='Coin')

class SelectDuration(forms.Form):
    duration=forms.ModelChoiceField(queryset=Duration.objects.all(),label='Duration')    