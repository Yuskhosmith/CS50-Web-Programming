from ast import expr_context
from email import message
from http.client import REQUEST_URI_TOO_LONG
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from sqlalchemy import false, true

from .models import User, AuctionListing, WatchList, Bid


def index(request):
    return render(request, "auctions/index.html", {
        'listings': AuctionListing.objects.all()
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


def categories(request):
    pass


def createlisting(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        starting_bid = request.POST["starting_bid"]
        img_link = request.POST["img_link"]
        category = request.POST["category"]

        try:
            newlisting = AuctionListing.objects.create(title=title, description=description, starting_bid=starting_bid, img_link=img_link, category=category)
            newlisting.save()
        except ValueError:
             return render(request, "auctions/createlisting.html", {
                "message": "Something Went Wrong, Try Again!"
            })
        except IntegrityError:
            return render(request, "auctions/createlisting.html", {
                "message": "Something Went Wrong, Try Again!"
            })
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/createlisting.html")

def listing(request, listing_id):
    items_id = []
    items = AuctionListing.objects.all()
    for item in items:
        y = item.id
        items_id.append(y)
    
    ctx = {'listing': AuctionListing.objects.get(pk=listing_id)}
    # If user isn't logged in, Just show them the page
    try:
        user = User.objects.get(id=request.user.id)
        item = AuctionListing.objects.get(pk=listing_id)
        if not item.current_bid:
            item.current_bid = item.starting_bid
        
    except Exception:
        return render(request, "auctions/listing.html", ctx)
    
    
    # Listing + watchlist + Bidding
    if listing_id in items_id:
        watchlist_item = WatchList.objects.filter(user = user, item = item).first()

        # Add/Remove watchlist
        if watchlist_item is None:
            on_watchlist = False
        else: 
            on_watchlist = True
        
        ctx['on_watchlist'] = on_watchlist

        # Bidding
        owner = item.owner
        # print(owner, user)
        if user == owner:
            notowner = False
        else:
            notowner = True

        ctx['notowner'] = notowner
        if request.method == "POST":
        
            try:
                user_bid = int(request.POST.get("user_bid"))
            
                if user_bid > item.current_bid:
                    item.current_bid = user_bid
                    new_bid = Bid(user = user, item = item, user_bid = user_bid)
                    new_bid.save()
                    item.save()
                    return HttpResponseRedirect("/listing/" + str(listing_id))
                
                else:
                    return render(request, "auctions/error.html", ctx)
            except TypeError:
                
                pass
            except ValueError:
                return render(request, "auctions/error.html", {
                    "message": "ValueError.."
                })
        return render(request, "auctions/listing.html", ctx)
    else:
        return render(request, 'auctions/index.html', {
            'message': 'Page does not exist',
            'listings': AuctionListing.objects.all(),
            # 'on_watchlist': on_watchlist,
        })
    
    


def watchlist(request):
    if request.method == "POST":
        # Collecting id, user and the listing itself
        listing_id = request.POST.get("listing_id")

        try:
            user = User.objects.get(id=request.user.id)
            item = AuctionListing.objects.get(pk=listing_id)

        except AuctionListing.DoesNotExist:
            return render(request, 'auctions/error.html', {
                "message": f"Listing Id ({listing_id}) does not exist"
            })
        
        # If the item is on watchlist, remove it
        if request.POST.get("on_watchlist") == "True":
            watchlist_item_to_be_removed = WatchList.objects.filter(
                user = user,
                item = item
            )
            watchlist_item_to_be_removed.delete()
        # Else Add it to watch list
        else:
            try:
                watchlist_item = WatchList(
                    user = user,
                    item =item
                )
                watchlist_item.save()
            except IntegrityError:
                return render(request, "auctions/error.html", {
                    "message": "Auction is already on watchlist"
                })
    
    else:
        watchlist_items_ids = User.objects.get(id=request.user.id).watchlist.values_list('item_id')
        watchlist_items = AuctionListing.objects.filter(id__in=watchlist_items_ids)
        
        return render(request, "auctions/watchlist.html", {
            'Watchlist': watchlist_items,
            #'ValueList': watchlist_items_ids,
            #'watchlist_items': watchlist_items
        })
    
    return HttpResponseRedirect("/listing/" + listing_id)

def bid(request):
    pass