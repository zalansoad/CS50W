from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class AuctionL(models.Model):
    title = models.CharField
    description = models.TextField
    bid_start = models.DecimalField(max_digits=20, decimal_places = 3)
    image_url = models.URLField
    created_at = models. DateTimeField(auto_now_add=True)

class Bids(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bid = models.DecimalField(max_digits=20, decimal_places = 3)
    item = models.ForeignKey(AuctionL,on_delete=models.CASCADE)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField
    item = models.ForeignKey(AuctionL,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
