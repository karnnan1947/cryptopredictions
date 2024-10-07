from django.db import models

# Create your models here.
class Algorithm(models.Model):
    al_name=models.CharField(max_length=10)

    def __str__(self):
        return self.al_name
    
class Coin(models.Model):
    c_name=models.CharField(max_length=20)    

    def __str__(self):
        return self.c_name

class Duration(models.Model):
    time=models.IntegerField()

    def __str__(self):
        return self.time    