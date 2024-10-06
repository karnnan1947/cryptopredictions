from django.db import models

# Create your models here.
from django.contrib.auth.models import User


class CryptoWallet(models.Model):
    user = models.ForeignKey(
            User, on_delete=models.CASCADE, null=True, blank=True)
    cryptoName = models.CharField(max_length=30)
    cryptoQuantity = models.FloatField(blank=True, null=True)

    class Meta:
        ordering = ['cryptoName']

    def __str__(self):
        return f'{self.cryptoName}'


class BuyPrice(models.Model):
    user = models.ForeignKey(
            User, on_delete=models.CASCADE, null=True, blank=True)
    day_created = models.DateField()
    time_created = models.TimeField()
    cryptoName = models.CharField(max_length=30)
    cryptoQuantity = models.FloatField()
    price = models.FloatField()

    class Meta:
        ordering = ['cryptoName', 'time_created', 'day_created',]

    def __str__(self):
        return f'{self.cryptoName} buy'
    