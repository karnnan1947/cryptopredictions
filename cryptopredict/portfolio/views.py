from django.core.cache import cache
from django.shortcuts import render, redirect
from django.contrib import messages
from pycoingecko import CoinGeckoAPI
from datetime import date, datetime
from .models import CryptoWallet, BuyPrice
from django.contrib.auth.decorators import login_required
from users.forms import FeedbackForm

coingecko = CoinGeckoAPI()
today = date.today()

def get_coin_price(coin):
    """ Fetch cryptocurrency price with caching & error handling """
    cache_key = f"coin_price_{coin.lower()}"
    cached_price = cache.get(cache_key)

    if cached_price is not None:
        return cached_price  # Return cached price if available

    try:
        response = coingecko.get_price(ids=coin.lower(), vs_currencies='usd')

        if coin.lower() not in response:
            return None  # Invalid coin name

        coin_price = response[coin.lower()]['usd']
        cache.set(cache_key, float(coin_price), timeout=60)  # Cache for 1 minute
        return float(coin_price)

    except Exception as e:
        print(f"Error fetching price for {coin}: {e}")
        return None  # API error

def collect_buy_prices(user, day, time, crypto, quantity, price):
    """ Store buy price history """
    b_price = BuyPrice(user=user, day_created=day, time_created=time, cryptoName=crypto, cryptoQuantity=quantity, price=price)
    b_price.save()

def delete_buy_prices(user, crypto_name, quantity):
    """ Remove buy price records after selling """
    buy_prices = BuyPrice.objects.filter(user=user, cryptoName=crypto_name).order_by("day_created", "time_created")

    for entry in buy_prices:
        if quantity >= entry.cryptoQuantity:
            quantity -= entry.cryptoQuantity
            entry.delete()
        else:
            entry.cryptoQuantity -= quantity
            entry.save()
            break

@login_required(login_url='/account')
def portfolio(request):
    today = date.today()
    form = FeedbackForm()


    if request.method == 'POST':
        # Handle Buy Request
        if request.POST.get('cryptoNameBuy') and request.POST.get('quantityDollarsBuy'):
            buying_coin = request.POST.get('cryptoNameBuy')
            quantity_bought = float(request.POST.get('quantityDollarsBuy'))

            # Fetch coin price (cached)
            buying_coin_exchange = get_coin_price(buying_coin)

            if buying_coin_exchange is None:
                messages.error(request, f"Failed to fetch price for '{buying_coin}'. Please enter a valid cryptocurrency.")
                return redirect('portfolio')

            crypto_quantity_bought = quantity_bought / buying_coin_exchange
            user_cryptos = CryptoWallet.objects.filter(user=request.user)

            user_cryptos_list = [str(i.cryptoName) for i in user_cryptos]
            if buying_coin in user_cryptos_list:
                y = user_cryptos.get(cryptoName=buying_coin)
                y.cryptoQuantity += crypto_quantity_bought
                y.save()
            else:
                new_crypto = CryptoWallet(user=request.user, cryptoName=buying_coin, cryptoQuantity=crypto_quantity_bought)
                new_crypto.save()

            curr_time = datetime.now().time()
            collect_buy_prices(request.user, today, curr_time, buying_coin, crypto_quantity_bought, buying_coin_exchange)

            messages.success(request, f"Successfully bought {crypto_quantity_bought:.5f} {buying_coin}.")
            cache.delete(f"user_portfolio_{request.user.id}")  # Clear cache after update
            return redirect('portfolio')

        # Handle Sell Request
        if request.POST.get('cryptoNameSell') and request.POST.get('cryptoQuantitySell'):
            selling_coin = request.POST.get('cryptoNameSell')
            selling_quantity = float(request.POST.get('cryptoQuantitySell'))

            try:
                user_crypto = CryptoWallet.objects.get(user=request.user, cryptoName=selling_coin)
            except CryptoWallet.DoesNotExist:
                messages.error(request, f"You don't own any {selling_coin}.")
                return redirect('portfolio')

            if user_crypto.cryptoQuantity < selling_quantity:
                messages.error(request, f"You don't have enough {selling_coin} to sell.")
                return redirect('portfolio')

            user_crypto.cryptoQuantity -= selling_quantity
            user_crypto.save()
            if user_crypto.cryptoQuantity <= 0:
                user_crypto.delete()

            curr_time = datetime.now().time()
            delete_buy_prices(request.user, selling_coin, selling_quantity)

            messages.success(request, f"Successfully sold {selling_quantity} {selling_coin}.")
            cache.delete(f"user_portfolio_{request.user.id}")  # Clear cache after update
            return redirect('portfolio')

        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.save()
            messages.success(request, "Feedback submitted successfully!")

    # 🔹 **Check Cached User Portfolio**
    cache_key = f"user_portfolio_{request.user.id}"
    cached_data = cache.get(cache_key)

    if cached_data:
        return render(request, "portfolio.html", cached_data)

    # Get user's cryptos & buy history (efficient query)
    user_cryptos = CryptoWallet.objects.filter(user=request.user)
    user_prices = BuyPrice.objects.filter(user=request.user)

    # Compute portfolio details
    current_crypto_values = []
    profit_loss_all = {}

    for crypto in user_cryptos:
        coin_price = get_coin_price(crypto.cryptoName)
        if coin_price is None:
            messages.error(request, f"Could not retrieve current price for {crypto.cryptoName}.")
            continue

        # Get all buy prices for this coin
        user_crypto_prices = user_prices.filter(cryptoName=crypto.cryptoName)

        total_quantity = sum(b.cryptoQuantity for b in user_crypto_prices)
        total_cost = sum(b.cryptoQuantity * b.price for b in user_crypto_prices)

        avg_buy_price = (total_cost / total_quantity) if total_quantity > 0 else 0

        # Profit or Loss calculation
        profit_loss = (coin_price - avg_buy_price) * crypto.cryptoQuantity
        profit_loss_all[crypto.cryptoName] = round(profit_loss, 2)

        # Calculate current value
        current_value = round(coin_price * crypto.cryptoQuantity, 5)
        current_crypto_values.append(current_value)

    # Prepare final table
    names = [i.cryptoName for i in user_cryptos]
    quantities = [i.cryptoQuantity for i in user_cryptos]
    values_list = list(profit_loss_all.values())
    portfolio_summary = sum(current_crypto_values)

    final_table = zip(names, quantities, current_crypto_values, values_list)

    context = {
    'final_table': list(final_table),  # Convert zip object to list
    'values_summary': round(portfolio_summary, 2),
    }

    cache.set(cache_key, context, timeout=30)  # Cache for 30 seconds
 # Cache for 30 seconds
    return render(request, "portfolio.html", {**context, 'form': form})
