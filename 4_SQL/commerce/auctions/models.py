from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Categories(models.Model):
    title = models.CharField(max_length=64)

    def __str__(self):
        return self.title

class AuctionL(models.Model):
    title = models.CharField(max_length=64)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.DecimalField(max_digits=20, decimal_places = 2)
    image_url = models.URLField()
    created_at = models. DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        CLOSED = 'closed', 'Closed'

    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ACTIVE)
    watchlist = models.ManyToManyField(User, related_name="watchlist", blank=True)
    
    def current_price(self):
        highest_bid = self.bids.order_by('-bid').first()
        if highest_bid:
            return highest_bid.bid
        return self.price

    def highest_bid(self):
        return self.bids.order_by('-bid').first()
    
class Bids(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bid = models.DecimalField(max_digits=20, decimal_places = 2)
    item = models.ForeignKey(AuctionL,on_delete=models.CASCADE, related_name='bids')

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    item = models.ForeignKey(AuctionL,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
