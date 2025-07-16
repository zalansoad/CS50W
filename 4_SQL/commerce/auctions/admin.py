from django.contrib import admin
from .models import User, Categories, AuctionL, Bids, Comment

# Register your models here.
class AuctionLAdmin(admin.ModelAdmin):
    filter_horizontal = ('watchlist',)

admin.site.register (User)
admin.site.register (AuctionL, AuctionLAdmin)
admin.site.register (Bids)
admin.site.register (Comment)
admin.site.register (Categories)