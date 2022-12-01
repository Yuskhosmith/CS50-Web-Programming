from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Category, AuctionListing, WatchList, Bid, Comment

def activeListing():
    activelisting = []
    listing = AuctionListing.objects.all()
    for item in listing:
        if item.closed == False:
            activelisting.append(item.id)

    return activelisting

def closedListing():
    closedlisting = []
    listing = AuctionListing.objects.all()
    for item in listing:
        if item.closed == True:
            closedlisting.append(item.id)

    return closedlisting
    

def index(request):
    activelisting = []
    listing = AuctionListing.objects.all()
    for item in listing:
        if item.closed == False:
            activelisting.append(item)
    return render(request, "auctions/index.html", {
        'listings': activelisting
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
    return render(request, 'auctions/categories.html', {
        'cats': Category.objects.all()
        })

def category(request, category):
    try:
        category = Category.objects.get(category=category)
        listings = AuctionListing.objects.filter(category=category.id, closed=False).all()
    except Category.DoesNotExist:
        return render(request, 'auctions/error.html', {"message": "Category does not exist"})
    return render(request, 'auctions/category.html', {"category": category.category, "listings": listings})

@login_required(login_url='/login')
def createlisting(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        starting_bid = request.POST["starting_bid"]
        img_link = request.POST["img_link"]
        x = request.POST["category"]
        # returns the object and boolean
        category, created = Category.objects.get_or_create(category = x)
        category = Category.objects.filter(category=x).first()

        try:
            user = User.objects.get(id=request.user.id)
            newlisting = AuctionListing.objects.create(title=title, description=description, starting_bid=starting_bid, img_link=img_link, category=category, owner=user)
            newlisting.save()
        except ValueError:
             return render(request, "auctions/createlisting.html", {
                "message": "Something(value) Went Wrong, Try Again!"
            })
        except IntegrityError:
            return render(request, "auctions/createlisting.html", {
                "message": "Something(integrity) Went Wrong, Try Again!"
            })
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/createlisting.html")

def listing(request, listing_id):
    items_id = activeListing()
    
    ctx = {'listing': AuctionListing.objects.get(pk=listing_id),
            'comments': Comment.objects.filter(item=AuctionListing.objects.get(pk=listing_id)).all()}
    
    # If user isn't logged in, Just show them the page
    try:
        user = User.objects.get(id=request.user.id)
        item = AuctionListing.objects.get(pk=listing_id)

        if not item.current_bid or item.current_bid == 0:
            item.current_bid = item.starting_bid
        
        ctx["min"] = item.current_bid + 1
    except AuctionListing.DoesNotExist:
        return render(request, "auctions/error.html", {
            "message": "Auction does not exist"
            })
    except User.DoesNotExist:
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

        # Bidding - Deciding who's viewing the page
        owner = item.owner
        if user == owner:
            notowner = False
        else:
            notowner = True

        ctx['notowner'] = notowner
        if request.method == "POST":
            try:
                item.closed = True
                item.save()
                return HttpResponseRedirect(reverse("index"))
            except Exception:
                return render(request, "auctions/error.html", {
                    "message": "Exception"
                })
        return render(request, "auctions/listing.html", ctx)

    # Accessing closed bids
    elif listing_id in closedListing():
        # Add closed attribute to ctx for accessing closed bids
        ctx['closed'] = item.closed

        #the user that won that auction
        try:
            final_bid = Bid.objects.filter(item=item).last()
            ctx['winner'] = final_bid.user
            ctx['bid'] = final_bid.user_bid

            # differentiatinfg owner, user and winner
            owner = item.owner
            if user == owner:
                #owner
                notowner = False
            elif user == final_bid.user:
                #winner
                notowner = True
            else:
                #normal user
                notowner = False
            ctx['notowner'] = notowner
        # If the user closed the bid without anybody bidding
        except AttributeError:
            ctx['winner'] = "no one"
            ctx['bid'] = 0
        return render(request, 'auctions/listing.html', ctx)

    else:
        return render(request, 'auctions/index.html', {
            'message': 'Page does not exist',
            'listings': items_id,
            # 'on_watchlist': on_watchlist,
        })

@login_required(login_url='/login')
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

@login_required(login_url='/login')
def bid(request, listing_id):
    try:
        user = User.objects.get(id=request.user.id)
        item = AuctionListing.objects.get(pk=listing_id)
    except AuctionListing.DoesNotExist:
        return render(request, "auctions/error.html", {
            "message": "Auction does not exist"
            })

    if request.method == "POST":
        try:
            user_bid = int(request.POST.get("user_bid"))
            
            if user_bid >= item.current_bid and user_bid >= item.starting_bid:
                item.current_bid = user_bid
                new_bid = Bid(user = user, item = item, user_bid = user_bid)
                new_bid.save()
                item.save()
                return HttpResponseRedirect("/listing/" + str(listing_id))
                
            else:
                return render(request, 'auctions/error.html', {"message": "Weelllll...... 🤡"})
        except ValueError:
                return render(request, "auctions/error.html", {
                    "message": "ValueError.."
                })
    return HttpResponseRedirect("/listing/" + str(listing_id))

@login_required(login_url='/login')
def comment(request, listing_id):
    try:
        user = User.objects.get(id=request.user.id)
        item = AuctionListing.objects.get(pk=listing_id)
    except AuctionListing.DoesNotExist:
        return render(request, "auctions/error.html", {
            "message": "Auction does not exist"
            })


    if request.method == "POST":
        try:
            comment = request.POST.get("comment")
            new_comment = Comment(user=user, item=item, comment=comment)
            new_comment.save()
            return HttpResponseRedirect("/listing/" + str(listing_id))
        # NOT DONE
        except Exception:
            # return HttpResponseRedirect("listing/" + str(listing_id))
            pass
    return HttpResponseRedirect("/listing/" + str(listing_id))

