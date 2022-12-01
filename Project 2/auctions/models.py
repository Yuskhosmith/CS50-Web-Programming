from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    category = models.CharField(max_length=64)
    def __str__(self):
        return f'{self.category}'

class AuctionListing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    starting_bid = models.IntegerField()
    img_link = models.URLField(max_length=1000)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, related_name="bid_category", default=1)
    current_bid = models.IntegerField(default=0)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owned_auction")
    closed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.id}: {self.title} starts at {self.starting_bid} \n Category: {self.category}'

class WatchList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    item = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidding_user")
    item = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)
    user_bid = models.IntegerField()

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comment")
    item = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="comment")
    comment = models.TextField()

    
