from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Categories, AuctionL, Bids, Comment
from datetime import datetime
from decimal import Decimal, InvalidOperation
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, "auctions/index.html", {
        "listing": AuctionL.objects.all()
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
    return HttpResponseRedirect(reverse("index"))


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

@login_required(login_url='/login')
def create_listing(request):
    #check submitted values
    if request.method == "POST":

        if request.POST["title"] == "":
           return render_create_listing(request, "Providing title is mandatory.")
        else:
            title = request.POST["title"]
            print(title)

        
        if not request.POST.get("category"):
            return render_create_listing(request, "Providing category is mandatory.")
        else:
            category = Categories.objects.get(title=request.POST["category"])

        if not request.POST.get("bid_start"):
            return render_create_listing(request, "Provide a valid price.")
        else:    
            try:
                price = Decimal(request.POST["bid_start"])
            except (InvalidOperation, ValueError):
                return render_create_listing(request, "Provide a valid price.")

        if request.POST["image_url"] == "":
            return render_create_listing(request, "Providing image url is mandatory.")
        else:
            image_url = request.POST["image_url"]

        if request.POST["description"] == "":
            return render_create_listing(request, "Providing description is mandatory.")
        else:
            description = request.POST["description"]
        
        user = request.user      

        new_listing = AuctionL(title=title, category=category, price=price, description=description, image_url=image_url, creator=user)
        new_listing.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render_create_listing(request)

def render_create_listing(request, message=None):
    return render(request, "auctions/create.html", {
            "categories": Categories.objects.all(),
            "message": message
        })

def listing_page(request, item_id):

    item = AuctionL.objects.get(id=item_id)
    comments = Comment.objects.filter(item=item)

    if request.method == "POST":
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("login"))

        if "new_bid" in request.POST:
            if item.status == AuctionL.Status.CLOSED:
                return render_listing(request, item, comments, error_msg="The auction is closed.")
            new_bid = request.POST["new_bid"]
            error_msg = "The bid must be at least as large as the starting bid, and must be greater than any other bids that have been placed (if any)."
            try:
                new_bid = Decimal(new_bid)
            except (InvalidOperation, ValueError):
                return render_listing(request, item, comments, error_msg)
            if new_bid <= item.current_price():
                return render_listing(request, item, comments, error_msg)
            else:
                Bids.objects.create(user=request.user, bid=new_bid, item=item)
                return HttpResponseRedirect(reverse('listing_page', args=[item_id]))
        
        elif "comment" in request.POST:
            comment = request.POST["comment"]
            Comment.objects.create(user=request.user, comment=comment, item=item)
            return render_listing(request, item, comments)
        elif "close_auction" in request.POST:
            if item.status == AuctionL.Status.CLOSED:
                return render_listing(request, item, comments, error_msg="The auction is closed already")
            item.status = AuctionL.Status.CLOSED
            item.save()
            return render_listing(request, item, comments)
    else:
        return render_listing(request, item, comments)
        
        
def render_listing(request, item, comment=None, error_msg=None):
    bids = item.bids.all()
    highest_bid = item.highest_bid()

    # checking if the auction is closed and sending the winner data to render
    winbid = None
    if item.status == AuctionL.Status.CLOSED:
        winbid = highest_bid

    return render(request, "auctions/listing.html", {
        "item": item,
        "winbid": winbid,
        "comments":comment,
        "error": error_msg
    })

    
@login_required(login_url='/login')
def watchlist(request, item_id):
    if request.method == "POST":
        item = AuctionL.objects.get(id=item_id)
        if item.watchlist.filter(id=request.user.id).exists():
            item.watchlist.remove(request.user)
        else:
            item.watchlist.add(request.user)

        return HttpResponseRedirect(reverse('listing_page', args=[item_id]))

@login_required(login_url='/login')
def watchlist_view(request):
    watchlist = request.user.watchlist.all()
    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist
    })

def categories_list(request):
    return render(request, "auctions/categories_list.html", {
        "categories": Categories.objects.all()
    })

def category(request, category_title):
        items = AuctionL.objects.filter(category__title=category_title)
        return render(request, "auctions/category.html", {
            "items": items

    })







