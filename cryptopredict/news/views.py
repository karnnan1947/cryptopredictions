from django.shortcuts import render, redirect
import requests
import json
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from users.forms import FeedbackForm

@login_required(login_url='/account')
def newz(request):
    form = FeedbackForm()

    # Fetch cached data if available
    price = cache.get('crypto_prices')
    api = cache.get('crypto_news')

    try:
        # Fetch price data if not cached
        if not price:
            price_request = requests.get("https://min-api.cryptocompare.com/data/pricemultifull?fsyms=BTC,ETH,SOL,XRP,POL,LTC,SHIB,ADA,DOG,TRX&tsyms=USD")
            price = json.loads(price_request.content)
            cache.set('crypto_prices', price, timeout=60)  # Cache the price data for 10 minutes
        
        # Fetch news data if not cached
        if not api:
            api_request = requests.get("https://min-api.cryptocompare.com/data/v2/news/?lang=EN")
            api = json.loads(api_request.content)
            cache.set('crypto_news', api, timeout=60)  # Cache the news data for 10 minutes

        # Handle form submission
        if request.method == 'POST':
            form = FeedbackForm(request.POST)
            if form.is_valid():
                feedback = form.save(commit=False)  # Don't save to DB yet
                feedback.user = request.user        # Assign the logged-in user
                feedback.save()
                return redirect('newz')  # Prevent form resubmission on page reload

    except Exception as e:
        # Log the error and render the page without crashing
        return render(request, 'newz.html', {
            'api': api or {}, 
            'price': price or {}, 
            'form': form, 
            'error_message': 'Failed to fetch data from API. Please try again later.'
        })
        print(api)

    return render(request, 'newz.html', {'api': api, 'price': price, 'form': form})
