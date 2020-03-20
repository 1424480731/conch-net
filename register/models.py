from django.db import models

# Create your models here.
class User(models.Model):

    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50)
    birthday= models.CharField(max_length=50)
    id_card_num = models.CharField(max_length=50)
    habby =  models.TextField(max_length=500)
    real_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    img = models.ImageField()