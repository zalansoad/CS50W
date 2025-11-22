from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
import json
from .models import User, Posts, Follow


def index(request):
    return render(request, "network/index.html",{
        "posts": Posts.objects.all().order_by('-created_at')
    })

def following_page(request):

    followed_users = Follow.objects.filter(follower=request.user).values_list("following", flat=True)

    posts = Posts.objects.filter(creator__in=followed_users).order_by("-created_at")

    return render(request, "network/following.html",{
        "posts": posts
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

        if User.objects.filter(username__iexact=username).exists():
            return render(request, "network/register.html", {
                "message": "Username already taken."
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

@csrf_exempt
def new_post(request):
    # Composing a new email must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # checking the content of the post
    data = json.loads(request.body)
    msg = data.get("msg", "").strip()
    if not msg:
        return JsonResponse({"error": "Empty posts are not allowed."}, status=400)
    else:
        user = request.user

        new_post = Posts(creator=user, message=msg)
        new_post.save()
    
    latest_post = Posts.objects.filter(creator=request.user).order_by('-created_at').first()
    

    return JsonResponse(latest_post.serialize(), status=201)

@csrf_exempt
def post_like(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    data = json.loads(request.body)
    post_id = data.get("post_id")

    user = request.user

    liked_post = Posts.objects.get(id=post_id)
    like_flag = None

    if user in liked_post.likes.all():
        liked_post.likes.remove(request.user)
        like_flag = "dislike"
    else:
        liked_post.likes.add(request.user)
        like_flag = "like"

    liked_post.refresh_from_db()

    data = liked_post.serialize()
    data['like_type'] = like_flag

    return JsonResponse(data, status=201)

@csrf_exempt
def edit_post(request):
    if request.method == "PUT":
        data = json.loads(request.body)
        post_id = data.get("post_id")
        new_message = data.get("message")

        post = Posts.objects.get(pk=post_id)

        if post.creator != request.user:
            return JsonResponse({"error": "Unauthorized"}, status=403)

        post.message = new_message
        post.save()

        # Visszaküldjük a frissített adatot
        return JsonResponse(post.serialize())

    return JsonResponse({"error": "PUT request required."}, status=400)

def profile(request, username):

    if not User.objects.filter(username__iexact=username).exists():
        return redirect("index")
    else:
        user = User.objects.get(username__iexact=username)

        followers = user.followers_rel.count()  
        following = user.following_rel.count() 
        
        posts = Posts.objects.filter(creator__username__iexact=username).order_by('-created_at')
        own_profile = False
        if request.user.username.casefold() == username.casefold():
            own_profile = True

        is_follower = False
        if request.user.is_authenticated:
            is_follower = Follow.objects.filter(follower=request.user, following=user).exists()
        else:
            is_follower = False
        
        return render(request, "network/profile.html",{
            "posts": posts,
            "own_profile": own_profile,
            "profile_name": username.capitalize(),
            "follower": followers,
            "following": following,
            "follow_flag": is_follower, 
        })

@csrf_exempt
def follow(request):
    user = request.user
    if request.method == "PUT":
        data = json.loads(request.body)
        username_to_follow = data.get("Follow")
        username_to_unfollow = data.get("UnFollow")

        if username_to_follow:
            target_user = User.objects.filter(username__iexact=username_to_follow).first()
            if not target_user:
                return JsonResponse({"error": "User not found."}, status=404)
            if not Follow.objects.filter(follower=user, following=target_user).exists():
                Follow.objects.create(follower=user, following=target_user)
            
            follower_count = Follow.objects.filter(following=target_user).count()
            
            return JsonResponse({
                "follower_count": follower_count,
            }, status=201)
        elif username_to_unfollow:
            target_user = User.objects.filter(username__iexact=username_to_unfollow).first()
            if not target_user:
                return JsonResponse({"error": "User not found."}, status=404)
            
            Follow.objects.filter(follower=user, following=target_user).delete()
            
            follower_count = Follow.objects.filter(following=target_user).count()
            
            return JsonResponse({
                "follower_count": follower_count,
            }, status=201)

        else:
            return JsonResponse({"error": "Invalid action"}, status=400)

    return JsonResponse({"error": "PUT request required."}, status=400)


