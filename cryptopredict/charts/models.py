from django.db import models

# Create your models here.
class chart(models.Model):
    title =models.CharField(max_length=100,null=False)
    description=models.TextField()
    image=models.ImageField(upload_to='media')
    priority=models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.title