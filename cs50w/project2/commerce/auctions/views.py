from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Category, Watchlist, Auction


def index(request):
    auctions = Auction.objects.filter(is_active=True)
    listings = [auction.listing for auction in auctions]
    return render(request, "auctions/index.html", {
        "listings": listings
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
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        starting_bid = request.POST["starting_bid"]
        category = Category.objects.get(name=request.POST["category"])
        image = request.FILES["image"]
        user = request.user
        listing = Listing(
            title=title, description=description, starting_bid=starting_bid,
            image=image, category=category, seller=user)
        listing.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/create_listing.html")
    
def listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    watchlist = None
    winner = None
    if hasattr(listing, 'auction') and listing.auction:
        auction = listing.auction
        if not auction.is_active:
            if auction.winner == request.user:
                winner = True
    if request.user.is_authenticated:
        watchlist = Watchlist.objects.filter(user=request.user, listing=listing).exists()
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "watchlist": watchlist,
        "winner": winner
    })

def add_to_watchlist(request, listing_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    listing = Listing.objects.get(pk=listing_id)
    watchlist = Watchlist(user=request.user, listing=listing)
    watchlist.save()
    request.user.watchlist.add(watchlist)
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

def remove_from_watchlist(request, listing_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    listing = Listing.objects.get(pk=listing_id)
    watchlist = Watchlist.objects.get(user=request.user, listing=listing)
    watchlist.delete()
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

def bid(request, listing_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    listing = Listing.objects.get(pk=listing_id)
    bid = request.POST["bid"]
    if listing.highest_bid is not None and int(bid) <= listing.highest_bid.amount:
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "message": "Your bid must be higher than the current highest bid."
        })
    if int(bid) <= listing.starting_bid:
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "message": "Your bid must be higher than the starting price."
        })

    listing.bids.create(amount=bid, bidder=request.user)
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

def comment(request, listing_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    listing = Listing.objects.get(pk=listing_id)
    content = request.POST["comment"]
    listing.comments.create(content=content, author=request.user)
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

def watchlist(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    user = request.user
    if hasattr(user, 'watchlist'):
        watchlist = user.watchlist.all()
        watchlist = [watch.listing for watch in watchlist]
    else:
        watchlist = None
    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist
    })

def categories(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": categories
    })

def edit_listing(request, listing_id):
    pass

def close_auction(request, listing_id):
    pass

def open_auction(request, listing_id):
    pass
