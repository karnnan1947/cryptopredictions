from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class users(models.Model):
    name=models.CharField(max_length=200)
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='user_profile')
    def __str__(self) -> str:
        return self.name
