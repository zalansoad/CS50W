from django.contrib import admin
from .models import User, Categories, AuctionL, Bids, Comment

# Register your models here.
class AuctionLAdmin(admin.ModelAdmin):
    filter_horizontal = ('watchlist',)
    list_display = ('title', 'category', 'creator', 'current_price', 'status', 'created_at')
    search_fields = ['title', 'category__title', 'creator__username', 'status']
admin.site.register (AuctionL, AuctionLAdmin)

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')
    search_fields = ['username', 'email']
admin.site.register(User, UserAdmin)

class CategoriesAdmin(admin.ModelAdmin):
    search_fields = ['title']
admin.site.register(Categories, CategoriesAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'comment', 'item', 'created_at')
    ordering = ('item', 'created_at')
    search_fields = ['user__username', 'item__title']
admin.site.register(Comment, CommentAdmin)

class BidsAdmin(admin.ModelAdmin):
    list_display = ('user', 'bid', 'item')
    search_fields = ['user__username', 'item__title']
admin.site.register(Bids, BidsAdmin)