from __future__ import unicode_literals

from django.db import models

# Create your models here.

from django.contrib.auth.models import User
from django.db import models
import datetime
from django.urls import reverse


class Product(models.Model):

  category = models.CharField(max_length=200)
  product_name = models.CharField(max_length=200 )
  description = models.CharField(max_length=200)
  price = models.FloatField()
  stock_number=models.FloatField()
  unit = models.CharField(max_length=5, default='Units')
  def __unicode__(self):
    return 'Name {}, Category {}, Description {}, Price {}, Stock_number {}'.format(self.product_name, self.category, self.description, self.price, self.stock_number)

class Client(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birthday = models.DateField(null=True)
    address = models.CharField(max_length=150)
    avatar = models.ImageField(null=True, upload_to='images')
    user = models.OneToOneField(User, primary_key=True, related_name='profile')

class MyShoppingCart(models.Model):
  client= models.OneToOneField(Client , primary_key=True, related_name='clients_cart')

class ShoppingCartItem(models.Model):
  cart= models.ForeignKey(MyShoppingCart)
  product= models.ForeignKey(Product)
