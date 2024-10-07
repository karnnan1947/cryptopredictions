from django.contrib import admin

# Register your models here.
from predict.models import Duration, Coin, Algorithm

class AdminDuration(admin.ModelAdmin):
    search_fields=('time',)

admin.site.register(Duration,AdminDuration)

class AdminCoin(admin.ModelAdmin):
    search_fields=('c_name',)

admin.site.register(Coin,AdminCoin)

class AdminAlgorithm(admin.ModelAdmin):
    search_fields=('al_name',)

admin.site.register(Algorithm,AdminAlgorithm)