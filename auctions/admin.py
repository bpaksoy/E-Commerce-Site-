from django.contrib import admin
from .models import User, Listing, Watchlist, Category, Comment, Bid


class ListingAdmin(admin.ModelAdmin):
    list_display = ('id')
    list_editable = ('image', 'title', 'status','content', 'category', 'starting_price')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'listing')
    list_editable = ('body')


class BidAdmin(admin.ModelAdmin):
    list_display = ('user', 'listing')
    list_editable = ('bid')


# Register your models here.
admin.site.register(User)
admin.site.register(Listing)
admin.site.register(Watchlist)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Bid)
