from django.contrib import admin
from .models import User, AuctionListing, WatchList, Category, Bid, Comment
# Register your models here.

admin.site.register(User)
admin.site.register(Category)
admin.site.register(AuctionListing)
admin.site.register(WatchList)
admin.site.register(Bid)
admin.site.register(Comment)