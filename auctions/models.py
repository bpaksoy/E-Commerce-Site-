from urllib import response
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError


class User(AbstractUser):
    pass


class Category(models.Model):
    CHOICES = [('Fashion', 'Fashion'), ('Home', 'Home'),
               ('Toys', 'Toys'), ('Electronics', 'Electronics')]

    category = models.CharField(max_length=100, choices=CHOICES)

    def __str__(self):
        return f"{self.category}"


class Listing(models.Model):
    image = models.ImageField(
        'image', upload_to='auctions/static/auctions/images', default='image')
    status = models.BooleanField(default=True)
    title = models.CharField(max_length=64)
    content = models.TextField()
    starting_price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.DO_NOTHING)
    category = models.ForeignKey(
        Category, null=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.id}, {self.image}, {self.title}, {self.status}, {self.content}, {self.starting_price}, {self.created_at}, {self.category}"


class Watchlist(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.RESTRICT)
    listings = models.ManyToManyField(
        Listing,  blank=True, related_name="listings")

    def __str__(self):
        return f"User: {self.user}, Listings: {self.listings}"


class Comment(models.Model):
    user = models.ForeignKey(
        User, null=True, related_name="user", on_delete=models.RESTRICT)
    listing = models.ForeignKey(
        Listing,  blank=True, related_name="comments", on_delete=models.CASCADE)
    body = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"User: {self.user}, Comment: {self.listing}, {self.date_created}"


class Bid(models.Model):
    user = models.ForeignKey(
        User, null=True, related_name="bidder", on_delete=models.RESTRICT)
    listing = models.ForeignKey(
        Listing, null=True, blank=True, related_name="bids", on_delete=models.RESTRICT)
    bid = models.FloatField()
    date_of_bid = models.DateTimeField(auto_now_add=True)
    win = models.BooleanField(default=False)

    def __str__(self):
        return f"Bidder: {self.user}, bid: {self.bid}, win: {self.win}"
