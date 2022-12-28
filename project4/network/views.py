import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from .models import User, Post, Following, Like

def paginator_handler(request, posts):
    p = Paginator(posts, 10)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)

    return page_obj


def index(request):
    posts = Post.objects.all().order_by('-id')
    print(posts[0].post)
    user_id = request.user.id
    page_obj = paginator_handler(request, posts)
    
    ctx = {'posts': page_obj}
    # print(user_id)
    if user_id is None:
        ctx['notLoggedInPrompt'] = True
    if request.method == 'POST':
        try:
            post = request.POST["post"]
            user = User.objects.get(pk=user_id)
            new_post = Post.objects.create(user=user, post=post)
            new_post.save
            return HttpResponseRedirect(reverse("index"))
        except Exception as e:
            return render(request, "network/index.html", {"message":e})
        
    return render(request, "network/index.html", ctx)

    # converting to API
    # posts = Post.objects.all().order_by('-id')
    # user_id = request.user.id
    # page_obj = paginator_handler(request, posts)
    # if user_id is None:
    #     # ctx['notLoggedInPrompt'] = True
    #     pass
    # if request.method == 'POST':
    #     try:
    #         post = request.POST["post"]
    #         user = User.objects.get(pk=user_id)
    #         new_post = Post.objects.create(user=user, post=post)
    #         new_post.save
    #         return HttpResponseRedirect(reverse("index"))
    #     except Exception as e:
    #         return render(request, "network/index.html", {"message":e})
    
    # return JsonResponse([post.serialize() for post in page_obj], safe=False)

@csrf_exempt
def editPost(request):
    user_id = request.user.id
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            if data.get("post") is not None:
                try:
                    post = data["post"]
                    prevpost = data["prevpost"]
                    user = User.objects.get(pk=user_id)
                    post_tb_updated = Post.objects.get(user=user, post=prevpost)
                    post_tb_updated.post = post
                    post_tb_updated.save()
                    return JsonResponse({"saved": "nothing went wrong."}, status=204)
                except Exception as e:
                    return JsonResponse({"error": f"something is wrong. {e}"}, status=404)
            return HttpResponse(status=204)
            
        except Exception as e:
            return render(request, "network/index.html", {"message":e})
    return HttpResponseRedirect(index)


@login_required
def reProfile(request):
    user = User.objects.get(pk=request.user.id)
    return redirect(reverse('profile', args=[user]))


def profile(request, username):
    user = User.objects.get(pk=request.user.id)
    if user.username == username:
        posts = user.posts.all().order_by('-timestamp')
        page_obj = paginator_handler(request, posts)
        followers = Following.objects.filter(following=user).count()
        following = Following.objects.filter(user=user).count()
        print(followers)
        ctx = {
            "posts": page_obj,
            "followers": followers,
            "following": following,
        }
    else:
        # show the user, the other person's profile
        try:
            some_other_user = User.objects.get(username=username)
            posts = some_other_user.posts.all().order_by('-timestamp')
            page_obj = paginator_handler(request, posts)
            followers = Following.objects.filter(following=some_other_user).count()
            following = Following.objects.filter(user=some_other_user).count()
            ctx = {
                "posts": page_obj,
                "username": username,
                "followers": followers,
                "following": following,
                "other_person": True
            }
        except User.DoesNotExist:
            return render(request, "network/error.html", {"message": f"{username} does not exist."})
    return render(request, "network/profile.html", ctx)

@login_required
def following(request):
    user = User.objects.get(pk=request.user.id)
    user_following = Following.objects.filter(user=user).all()
    posts = Post.objects.all().order_by('-id')

    user_list =[]
    for u in user_following:
        user_list.append(User.objects.get(username=u.following))

    posts_tbd = []
    for post in posts:
        if post.user in user_list:
            posts_tbd.append(post)
    
    page_obj = paginator_handler(request, posts_tbd)
    
    ctx = {
        "posts": page_obj
    }
    return render(request, "network/following.html", ctx)

def check_following(request, username):
    user = User.objects.get(pk=request.user.id)
    user_following = Following.objects.filter(user=user)
    # print(user_following)
    # user_following = user.following_details.all()

    x = [uf.serialize() for uf in user_following]
    # print(x)
    y = []
    for i in x:
        y.append(i['following'])

    # print(username, y)
    if username in y:
        return JsonResponse(True, safe=False)
    else:
        return JsonResponse(False, safe=False)


@csrf_exempt
@login_required
def like(request):
    user_id = request.user.id

    # instead of stressing over payloads of GEt request, We can use :Drum Roll: Get or Create method 
    # if request.method == 'GET':
    #     try:
    #         data = json.load(request.body)
    #         if data.get("post") is not None and data.get("username") is not None:
    #             # Check if user has liked the post
    #             user = User.objects.get(pk=user_id)
    #             post = data["post"]
    #             username = data["username"]
    #             poster = User.objects.get(username=username)
    #             post = Post.objects.get(user=poster, post=post)
    #             post_liked_or_not = Like.objects.get(user=user, post=post)
    #             if post_liked_or_not is not None:
    #                 return JsonResponse(True, safe=False)
    #             else:
    #                 return JsonResponse(False, safe=False)
    #     except Exception as e:
    #         return JsonResponse({"error": f"something is wrong. {e}"}, status=404)


    
    if request.method == 'PUT':
        # like or dislike
        try:
            data = json.loads(request.body)
            
            if data.get("post") is not None:
                try:
                    post_id = data["post"]
                    print("pass 1")
                    user = User.objects.get(pk=user_id)
                    print("pass 2")
                    # username = User.objects.get(username=data["username"])
                    print("pass 3")
                    # owner = User.objects.get(username=username)
                    # print(post_id, owner)
                    print("pass 4")
                    post = Post.objects.get(id=post_id)
                    print("pass 5")
                    likeObj, liked = Like.objects.get_or_create(user=user, post=post)
                    if not liked:
                        likeObj.delete()
                    return JsonResponse({"saved": "nothing went wrong."}, status=204)
                except Exception as e:
                    return JsonResponse({"error": f"something is wrong. {e}"}, status=404)
            # elif data.get("unlike") is not None:
            #     try:
            #         post = data["post"]
            #         user = User.objects.get(pk=user_id)
            #         username = User.objects.get(username=data["username"])
            #         owner = User.objects.get(username=username)
            #         post = Post.objects.get(user=owner, post=post)
            #         like_post = Like.objects.get(user=user, post=post)
            #         like_post.delete()
            #         return JsonResponse({"saved": "nothing went wrong."}, status=204)
            #     except Exception as e:
            #         return JsonResponse({"error": f"something is wrong. {e}"}, status=404)
            # return HttpResponse(status=204)
            return JsonResponse({"saved": "2- nothing went wrong."}, status=204)
        except Exception as e:
            return render(request, "network/index.html", {"message":e})
    return HttpResponseRedirect(index)

@csrf_exempt
@login_required
def follow(request):
    user = User.objects.get(pk=request.user.id)
    if request.method == 'PUT':
        data = json.loads(request.body)
        if data.get("follow") is not None:
            try:
                user_to_be_followed = User.objects.get(username=data["follow"])
            except Exception as e:
                return JsonResponse({"error": f"user not found. {e}"}, status=404)
            follow_action = Following.objects.create(user=user, following=user_to_be_followed)
            follow_action.save()

        return HttpResponse(status=204)
    else:
        return redirect(reverse('profile', args=[user]))
        
@csrf_exempt
@login_required
def unfollow(request): 
    user = User.objects.get(pk=request.user.id)
    if request.method == 'PUT':
        data = json.loads(request.body)
        if data.get("unfollow") is not None:
            try:
                user_to_be_unfollowed = User.objects.get(username=data["unfollow"])
            except Exception as e:
                return JsonResponse({"error": f"user not found. {e}"}, status=404)
            follow_action = Following.objects.get(user=user, following=user_to_be_unfollowed)
            follow_action.delete()
        return HttpResponse(status=204)
    else:
        return redirect(reverse('profile', args=[user]))

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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
