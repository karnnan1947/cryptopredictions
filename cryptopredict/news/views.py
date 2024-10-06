from django.shortcuts import render,redirect
import requests
import json
from django.contrib.auth.decorators import login_required
from users.forms import FeedbackForm

@login_required(login_url='/account')
def newz(request):
    form = FeedbackForm()
    price_request = requests.get("https://min-api.cryptocompare.com/data/pricemultifull?fsyms=BTC,ETH,SOL,XRP,POL,LTC,SHIB,ADA,DOG,TRX&tsyms=USD")
    price = json.loads(price_request.content)
    api_request=requests.get("https://min-api.cryptocompare.com/data/v2/news/?lang=EN")
    api=json.loads(api_request.content)
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)  # Don't save to DB yet
            feedback.user = request.user        # Assign the logged-in user
            feedback.save()
            return redirect('newz')
    return render(request,'newz.html',{'api':api , 'price':price,'form': form})