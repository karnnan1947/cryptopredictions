from django.shortcuts import render
import requests
import json
# Create your views here.
def newz(request):
    price_request = requests.get("https://min-api.cryptocompare.com/data/pricemultifull?fsyms=BTC,ETH,SOL,XRP,POL,LTC,SHIB,ADA,DOG,TRX&tsyms=USD")
    price = json.loads(price_request.content)
    api_request=requests.get("https://min-api.cryptocompare.com/data/v2/news/?lang=EN")
    api=json.loads(api_request.content)
    return render(request,'newz.html',{'api':api , 'price':price})