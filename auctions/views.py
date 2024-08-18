from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *
from .forms import *


def get_listings():
    return Listing.objects.order_by("-created_at")


def get_listing(listing_id):
    return Listing.objects.get(id=listing_id)


def get_active_listings():
    status = True
    return Listing.objects.filter(status=status).order_by("-created_at")


def index(request):
    listings = get_listings()
    if not request.user.is_authenticated:
        return render(request, "auctions/index.html", {
            "listings": listings
        })
    else:
        try:
            user_list = Watchlist.objects.get(user=request.user)
        except:
            user_list = None
        if not user_list:
            return render(request, "auctions/index.html", {
                "listings": listings
            })
        else:
            watchlist = user_list.listings.all()
            count = watchlist.count
            return render(request, "auctions/index.html", {
                "listings": listings,
                "count": count
            })


def active_listings(request):
    listings = get_active_listings()
    if not request.user.is_authenticated:
        return render(request, "auctions/index.html", {
            "listings": listings
        })
    else:
        try:
            user_list = Watchlist.objects.get(user=request.user)
        except:
            user_list = None
        if not user_list:
            return render(request, "auctions/active.html", {
                "listings": listings
            })
        else:
            watchlist = user_list.listings.all()
            count = watchlist.count
            return render(request, "auctions/active.html", {
                "listings": listings,
                "count": count
            })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return render(request, "auctions/login.html", {
        "message": "You have successfully logged out."
    })


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


# Add a new listing
def add_listing(request):
    if request.method == "POST":
        form = NewListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.author = request.user
            listing.save()
        try:
            print("Successfully saved!!")
            return HttpResponseRedirect(reverse("index"))
        except:
            messages.error(
                request, "This listing was not saved in the system.")
            return render(request, "auctions/add.html", {
                "form": form
            })
    else:
        form = NewListingForm()
        return render(request, "auctions/add.html", {
            "form": form
        })

# Show a list of watched items
@ login_required
def watchlist(request):
    try:
        user_list = Watchlist.objects.get(user=request.user)
    except:
        user_list = None

    if not user_list:
        return render(request, "auctions/watchlist.html", {
            "watchlist": []
        })
    else:
        user_list = Watchlist.objects.get(user=request.user)
        watchlist = user_list.listings.all()
        count = watchlist.count
        return render(request, "auctions/watchlist.html", {
            "watchlist": watchlist,
            "count": count
        })

# Add an item to watchlist


@ login_required
def add_to_watchlist(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    user_list, created = Watchlist.objects.get_or_create(user=request.user)
    user_list.listings.add(listing)
    watchlist = user_list.listings.all()
    count = watchlist.count
    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist,
        "count": count
    })

# Remove an item from watchlist


@ login_required
def remove_from_watchlist(request, listing_id):
    user_list = Watchlist.objects.get(user=request.user)
    user_list.listings.remove(listing_id)
    watchlist = user_list.listings.all()
    count = watchlist.count
    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist,
        "count": count
    })


# Show listing detail
def listing(request, listing_id):
    listing = get_listing(listing_id)
    if request.user.is_authenticated:
        user = request.user
        if not listing.status:
            bid_list = Bid.objects.get(listing_id=listing_id, win=True)
            winner = bid_list.user
            if winner == user:
                messages.success(
                    request, "Congratulations! You have won this auction.")
                return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "user": user
                })

            else:
                messages.success(
                    request, "This auction has been closed by the seller.")
                return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "user": user
                })
        else:
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "user": user
            })
    else:
        return render(request, "auctions/listing.html", {
            "listing": listing
        })


def categories(request):
    listings = get_active_listings()
    if not request.user.is_authenticated:
        return render(request, "auctions/categories.html", {
            "listings": listings
        })
    else:
        user_list, created = Watchlist.objects.get_or_create(user=request.user)
        watchlist = user_list.listings.all()
        count = watchlist.count
        return render(request, "auctions/categories.html", {
            "listings": listings,
            "count": count
        })


def show_categories(request, category):
    category = Category.objects.filter(category=category)
    listings = get_active_listings()
    listings = listings.filter(
        category__in=category)
    if not request.user.is_authenticated:
        return render(request, "auctions/categories.html", {
            "listings": listings,
            "category": category
        })
    else:
        user_list, created = Watchlist.objects.get_or_create(user=request.user)
        watchlist = user_list.listings.all()
        count = watchlist.count
        return render(request, "auctions/categories.html", {
            "listings": listings,
            "count": count,
            "category": category
        })


@ login_required
def add_comment(request, listing_id):
    listing = get_listing(listing_id)
    if request.method == "POST":
        form = NewCommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.listing = listing
            comment.user = request.user
            comment.save()
        try:
            print("Successfully saved!!")
            return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
        except:
            messages.error(
                request, "This comment was not saved in the system.")
            return render(request, "auctions/add_comment.html", {
                "form": form,
                "listing": listing
            })
    else:
        form = NewCommentForm()
        return render(request, "auctions/add_comment.html", {
            "form": form,
            "listing": listing
        })


@ login_required
def place_bid(request, listing_id):
    listing = get_listing(listing_id)
    bid_list = Bid.objects.filter(listing_id=listing_id)
    if request.method == "POST":
        form = NewBidForm(request.POST, request.FILES)
        if form.is_valid():
            bid = form.save(commit=False)
            bid.listing = listing
            bid.user = request.user
            if len(bid_list):
                max = bid_list.order_by('-bid')[0]
                if bid.bid <= max.bid:
                    messages.error(
                        request, f"The bid needs to be more than the highest bid of ${max.bid}")
                    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

            if bid.bid < listing.starting_price:
                messages.error(
                    request, "The bid needs to be equal to or more than the listing price")
                return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
            else:
                bid.save()
        try:
            print("Successfully placed the bid!!")
            return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
        except:
            messages.error(
                request, "This bid was not saved in the system.")
            return render(request, "auctions/place_bid.html", {
                "form": form,
                "listing": listing
            })
    else:
        form = NewBidForm()
        return render(request, "auctions/place_bid.html", {
            "form": form,
            "listing": listing
        })


@ login_required
def close_auction(request, listing_id):
    listing = get_listing(listing_id)
    bid_list = Bid.objects.filter(listing_id=listing_id)
    if len(bid_list):
        max = bid_list.order_by('-bid')[0]
        max.win = True
        max.save()
        listing.status = False
        listing.save()

        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
    else:
        messages.error(
            request, "The listing has not received an offer yet! Closing not allowed.")
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
