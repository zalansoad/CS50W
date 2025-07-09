from django.contrib import admin
from .models import User, Categories, AuctionL, Bids, Comment

# Register your models here.

admin.site.register (User)
admin.site.register (AuctionL)
admin.site.register (Bids)
admin.site.register (Comment)
admin.site.register (Categories)