from django.shortcuts import render, redirect
from pycoingecko import CoinGeckoAPI
from datetime import date, datetime
from .models import CryptoWallet, BuyPrice
from django.contrib.auth.decorators import login_required
from users.forms import FeedbackForm


coingecko = CoinGeckoAPI()
today = date.today()


def get_coin_price(coin):
    coin_price = coingecko.get_price(ids=str(coin).lower(), vs_currencies='usd')[str(coin).lower()]['usd']
    return float(coin_price)

def CollectBuyPrices(user, day, time, crypto, cq, price):
    bPrice = BuyPrice()
    bPrice.user = user
    bPrice.day_created = day
    bPrice.time_created = time
    bPrice.cryptoName = crypto
    bPrice.cryptoQuantity = cq
    bPrice.price = price
    bPrice.save()


def CollectBuyPrices(user, day, time, crypto, cq, price):
    bPrice = BuyPrice()
    bPrice.user = user
    bPrice.day_created = day
    bPrice.time_created = time
    bPrice.cryptoName = crypto
    bPrice.cryptoQuantity = cq
    bPrice.price = price
    bPrice.save()

def DeleteBuyPrices(buyprices, quantity, user, cryptoname, day, time):
    for i in range(0, len(buyprices)):
        if quantity > buyprices[i].cryptoQuantity:
            quantity -= buyprices[i].cryptoQuantity
            buyprices[i].delete()
        else:
            buyprices[i].cryptoQuantity -= quantity
            buyprices[i].save()
            break
    # checks for buyprices to avoid wallet bug
    try:
        check = BuyPrice.objects.get(user=user, cryptoName=cryptoname)
    except:
        check = False

    if check is False:
        CollectBuyPrices(user, day, time, cryptoname, 0, 0)



@login_required(login_url='/account')
def portfolio(request):
    today = date.today()  # Define today's date
    user_cryptos = CryptoWallet.objects.filter(user=request.user)
    user_prices = BuyPrice.objects.filter(user=request.user)
        # Calculate current values and profit/loss
    current_crypto_values = []
    profit_loss_all = {}

    for i in user_prices:
        profit_loss = (i.cryptoQuantity * get_coin_price(i.cryptoName)) - (i.cryptoQuantity * i.price)
        profit_loss_all[i.cryptoName] = profit_loss

    for i in user_cryptos:
        current_value = round(get_coin_price(i.cryptoName) * i.cryptoQuantity, 5)
        current_crypto_values.append(current_value)

        # Prepare the final table for display
    names = [i.cryptoName for i in user_cryptos]
    quantities = [i.cryptoQuantity for i in user_cryptos]
    values_list = list(profit_loss_all.values())
    portfolio_summary = sum(current_crypto_values)

    final_table = zip(names, quantities, current_crypto_values, values_list)
    
    if request.method == 'POST':
        # Handle Buy Request
        if request.POST.get('cryptoNameBuy') and request.POST.get('quantityDollarsBuy'):
            buying_coin = request.POST.get('cryptoNameBuy')
            quantity_bought = request.POST.get('quantityDollarsBuy')

            # Get the coin's current exchange price
            buying_coin_exchange = get_coin_price(buying_coin)

            # Calculate how much of the crypto was bought
            cryptoQuantityBought = float(quantity_bought) / float(buying_coin_exchange)
            user_cryptos = CryptoWallet.objects.filter(user=request.user)

            # List of the user's current cryptos
            user_cryptos_list = [str(i.cryptoName) for i in user_cryptos]

            if buying_coin in user_cryptos_list:
                # If the coin exists, update its quantity
                y = user_cryptos.get(cryptoName=buying_coin)
                y.cryptoQuantity += cryptoQuantityBought
                y.save()

            else:
                # If the coin doesn't exist, create a new wallet entry
                new_cryp = CryptoWallet(
                    user=request.user,
                    cryptoName=buying_coin,
                    cryptoQuantity=cryptoQuantityBought
                )
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
                user_crypto = None

            if user_crypto:
                # Subtract the sold quantity
                user_crypto.cryptoQuantity -= selling_quantity
                user_crypto.save()

                if user_crypto.cryptoQuantity <= 0:
                    # Delete the crypto if the quantity becomes zero
                    user_crypto.delete()

                # Remove buy price records
                user_prices = BuyPrice.objects.filter(user=request.user, cryptoName=selling_coin)
                curr_time = datetime.now().time()
                DeleteBuyPrices(user_prices, selling_quantity, request.user, selling_coin, today, curr_time)

                return redirect('portfolio')  
        else:
            form = FeedbackForm(request.POST)
            if form.is_valid():
                feedback = form.save(commit=False)
                feedback.user = request.user  # Automatically assign the logged-in user
                feedback.save()     

    # Get the user's portfolio dat


    return render(request, "portfolio.html", {
        'user': request.user,
        'final_table': final_table,
        'values_summary': round(portfolio_summary, 2),
    })
