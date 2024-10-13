from rest_framework import serializers
from .models import CryptoWallet, BuyPrice

class CryptoWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = CryptoWallet
        fields = '__all__'  # or specify fields manually

class BuyPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyPrice
        fields = '__all__'