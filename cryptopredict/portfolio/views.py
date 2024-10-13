from django.shortcuts import render, redirect
from pycoingecko import CoinGeckoAPI
from datetime import date, datetime
from .models import CryptoWallet, BuyPrice
from django.contrib.auth.decorators import login_required
from users.forms import FeedbackForm
from django.contrib import messages  # For error messages
from django.core.cache import cache

coingecko = CoinGeckoAPI()
today = date.today()


def get_multiple_coin_prices(coins):
    """Fetch prices for multiple coins in one API call."""
    try:
        prices = coingecko.get_price(ids=','.join(coins).lower(), vs_currencies='usd')
        return {coin.lower(): prices[coin.lower()]['usd'] for coin in coins if coin.lower() in prices}
    except Exception as e:
        print(f"Error fetching multiple coin prices: {e}")
        return {}


def CollectBuyPrices(user, day, time, crypto, cq, price):
    """Collect buy price details."""
    bPrice = BuyPrice(
        user=user, 
        day_created=day, 
        time_created=time, 
        cryptoName=crypto, 
        cryptoQuantity=cq, 
        price=price
    )
    bPrice.save()


def DeleteBuyPrices(buyprices, quantity, user, cryptoname, day, time):
    """Delete or update buy prices as necessary."""
    for price_record in buyprices:
        if quantity > price_record.cryptoQuantity:
            quantity -= price_record.cryptoQuantity
            price_record.delete()
        else:
            price_record.cryptoQuantity -= quantity
            price_record.save()
            break

    # Check for buyprices to avoid wallet bug
    if not BuyPrice.objects.filter(user=user, cryptoName=cryptoname).exists():
        CollectBuyPrices(user, day, time, cryptoname, 0, 0)


@login_required(login_url='/account')
def portfolio(request):
    try:
        form = FeedbackForm()
        user_cryptos = CryptoWallet.objects.filter(user=request.user)
        user_prices = BuyPrice.objects.filter(user=request.user)

        # Prepare a list of crypto names for batch fetching
        crypto_names = [price.cryptoName for price in user_prices] + [crypto.cryptoName for crypto in user_cryptos]
        unique_crypto_names = list(set(crypto_names))  # Remove duplicates

        # Get prices for all cryptocurrencies in one go
        prices = get_multiple_coin_prices(unique_crypto_names)

        # Calculate current values and profit/loss
        current_crypto_values = []
        profit_loss_all = {}

        for price_record in user_prices:
            coin_price = prices.get(price_record.cryptoName.lower())
            if coin_price is None:
                messages.error(request, f"Could not fetch the price for {price_record.cryptoName}. Please try again later.")
                continue
            profit_loss = (price_record.cryptoQuantity * coin_price) - (price_record.cryptoQuantity * price_record.price)
            profit_loss_all[price_record.cryptoName] = profit_loss

        for crypto in user_cryptos:
            coin_price = prices.get(crypto.cryptoName.lower())
            if coin_price is None:
                continue  # Skip if we couldn't fetch the price
            current_value = round(coin_price * crypto.cryptoQuantity, 5)
            current_crypto_values.append(current_value)

        # Prepare the final table for display
        names = [crypto.cryptoName for crypto in user_cryptos]
        quantities = [crypto.cryptoQuantity for crypto in user_cryptos]
        values_list = list(profit_loss_all.values())
        portfolio_summary = sum(current_crypto_values)

        final_table = zip(names, quantities, current_crypto_values, values_list)

        if request.method == 'POST':
            # Handle Buy Request
            if request.POST.get('cryptoNameBuy') and request.POST.get('quantityDollarsBuy'):
                buying_coin = request.POST.get('cryptoNameBuy')
                quantity_bought = request.POST.get('quantityDollarsBuy')

                # Get the coin's current exchange price
                buying_coin_exchange = prices.get(buying_coin.lower())
                if buying_coin_exchange is None:
                    messages.error(request, f"Could not fetch the price for {buying_coin}. Please try again later.")
                    return redirect('portfolio')

                # Calculate how much of the crypto was bought
                cryptoQuantityBought = float(quantity_bought) / float(buying_coin_exchange)
                user_cryptos_list = [str(crypto.cryptoName) for crypto in user_cryptos]

                if buying_coin in user_cryptos_list:
                    # If the coin exists, update its quantity
                    existing_crypto = user_cryptos.get(cryptoName=buying_coin)
                    existing_crypto.cryptoQuantity += cryptoQuantityBought
                    existing_crypto.save()
                else:
                    # If the coin doesn't exist, create a new wallet entry
                    new_cryp = CryptoWallet(user=request.user, cryptoName=buying_coin, cryptoQuantity=cryptoQuantityBought)
                    new_cryp.save()

                # Save the buy price history
                curr_time = datetime.now().time()
                CollectBuyPrices(request.user, today, curr_time, buying_coin, cryptoQuantityBought, buying_coin_exchange)

                return redirect('portfolio')

            # Handle Sell Request
            elif request.POST.get('cryptoNameSell') and request.POST.get('cryptoQuantitySell'):
                selling_coin = request.POST.get('cryptoNameSell')
                selling_quantity = float(request.POST.get('cryptoQuantitySell'))

                try:
                    user_crypto = CryptoWallet.objects.get(user=request.user, cryptoName=selling_coin)
                except CryptoWallet.DoesNotExist:
                    messages.error(request, f"You do not own any {selling_coin}.")
                    return redirect('portfolio')

                # Subtract the sold quantity
                user_crypto.cryptoQuantity -= selling_quantity
                if user_crypto.cryptoQuantity <= 0:
                    # Delete the crypto if the quantity becomes zero
                    user_crypto.delete()
                else:
                    user_crypto.save()

                # Remove buy price records
                user_prices = BuyPrice.objects.filter(user=request.user, cryptoName=selling_coin)
                curr_time = datetime.now().time()
                DeleteBuyPrices(user_prices, selling_quantity, request.user, selling_coin, today, curr_time)

                return redirect('portfolio')

            # Handle Feedback form
            form = FeedbackForm(request.POST)
            if form.is_valid():
                feedback = form.save(commit=False)
                feedback.user = request.user  # Automatically assign the logged-in user
                feedback.save()
                return redirect('portfolio')

        return render(request, "portfolio.html", {
            'user': request.user,
            'final_table': final_table,
            'values_summary': round(portfolio_summary, 2), 'form' : form ,
        })

    except Exception as e:
        messages.error(request, f"An error occurred: {e}")
        return render(request, "portfolio.html", {
            'user': request.user,
            'final_table': [],
            'values_summary': 0,
        })
