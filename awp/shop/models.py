from __future__ import unicode_literals

from django.db import models

# Create your models here.

from django.contrib.auth.models import User
from django.db import models
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
