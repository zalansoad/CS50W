from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Categories, AuctionL
from datetime import datetime


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

def create_listing(request):
 
    if request.method == "POST":
        title = request.POST["title"]
        category = Categories.objects.get(title=request.POST["category"])
        price = Deciaml(request.POST["price"])
        description = request.POST["description"]
        image_url = request.POST["image_url"]
        user = request.user

        new_listing = AuctionL(title=title, category=category, price=price, description=description, image_url=image_url, creator=user)
        new_listing.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/create.html", {
            "categories": Categories.objects.all()
        })

def listing_page(request, item_id):

    item = AuctionL.objects.get(id=item_id)
    return render(request, "auctions/listing.html", {
        "item": item
    })

    #if bid.user == request.user
    #itt kiszedni a legmagasabb bidet es annak useret, ha ez ugyanaz mindt a request.user, akkor o nyert es kiirni
    #bids = Bids.objects.filter(item=item)