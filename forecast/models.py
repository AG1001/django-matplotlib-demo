"""Models for the Oil price prediction app."""

from django.db import models


class Region(models.Model):
  def __str__(self):
    return self.name
  name = models.CharField(max_length=128)


class Price(models.Model):
  def __str__(self):
    return '{0}|{1}|{2}'.format(self.region, self.month_str,
                                self.price_per_barrel)
  region = models.ForeignKey(Region)
  month_str = models.CharField(max_length=128)
  price_per_barrel = models.FloatField()
