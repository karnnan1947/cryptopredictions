from django.shortcuts import render
import requests
import json
# Create your views here.
def newz(request):
    api_request=requests.get("https://min-api.cryptocompare.com/data/v2/news/?lang=EN")
    api=json.loads(api_request.content)
    return render(request,'newz.html',{'api':api})