from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse

from .models import Post, Like, Comment, Follow
from .forms import PostForm, CommentForm
from notifications.models import Notification


# ── Auth ──────────────────────────────────────────────────────────────

def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("feed")
    else:
        form = UserCreationForm()
    return render(request, "social/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("feed")
    else:
        form = AuthenticationForm()
    return render(request, "social/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")


# ── Feed ──────────────────────────────────────────────────────────────

@login_required
def feed(request):
    form = PostForm()
    followed = Follow.objects.filter(follower=request.user).values_list("following", flat=True)
    posts = Post.objects.filter(Q(user__in=followed) | Q(user=request.user)).select_related("user").prefetch_related("likes", "comments__user")
    query = request.GET.get("q", "")
    if query:
        posts = posts.filter(Q(text__icontains=query) | Q(user__username__icontains=query))
    return render(request, "social/feed.html", {"posts": posts, "form": form, "query": query})


# ── Posts ─────────────────────────────────────────────────────────────

@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
    return redirect("feed")


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk, user=request.user)
    post.delete()
    return redirect("feed")


# ── Likes ─────────────────────────────────────────────────────────────

@login_required
def like_toggle(request, pk):
    post = get_object_or_404(Post, pk=pk)
    like = Like.objects.filter(user=request.user, post=post).first()
    if like:
        like.delete()
        liked = False
    else:
        Like.objects.create(user=request.user, post=post)
        liked = True
        if post.user != request.user:
            Notification.objects.create(
                recipient=post.user, sender=request.user,
                type="like", text=f"{request.user.username} liked your post",
                link=f"/post/{post.pk}/",
            )
    return JsonResponse({"liked": liked, "count": post.total_likes})


# ── Comments ──────────────────────────────────────────────────────────

@login_required
def comment_create(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            if post.user != request.user:
                Notification.objects.create(
                    recipient=post.user, sender=request.user,
                    type="comment", text=f"{request.user.username} commented: {comment.text[:50]}",
                    link=f"/post/{post.pk}/",
                )
    return redirect("feed")


# ── Follow ────────────────────────────────────────────────────────────

@login_required
def follow_toggle(request, username):
    target = get_object_or_404(User, username=username)
    if target == request.user:
        return redirect("feed")
    follow = Follow.objects.filter(follower=request.user, following=target).first()
    if follow:
        follow.delete()
    else:
        Follow.objects.create(follower=request.user, following=target)
        Notification.objects.create(
            recipient=target, sender=request.user,
            type="follow", text=f"{request.user.username} started following you",
            link=f"/profile/{request.user.username}/",
        )
    return redirect(request.META.get("HTTP_REFERER", "feed"))


# ── Profile ───────────────────────────────────────────────────────────

@login_required
def profile(request, username):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(user=user)
    followers_count = Follow.objects.filter(following=user).count()
    following_count = Follow.objects.filter(follower=user).count()
    is_following = request.user.is_authenticated and Follow.objects.filter(follower=request.user, following=user).exists()
    return render(request, "social/profile.html", {
        "profile_user": user, "posts": posts,
        "followers_count": followers_count, "following_count": following_count,
        "is_following": is_following,
    })


@login_required
def search_users(request):
    q = request.GET.get("q", "")
    from django.contrib.auth import get_user_model
    User = get_user_model()
    users = User.objects.filter(username__icontains=q)[:20] if q else []
    return render(request, "social/search.html", {"users": users, "query": q})


# ── Notifications ─────────────────────────────────────────────────────

@login_required
def notifications(request):
    notifs = Notification.objects.filter(recipient=request.user)
    notifs.update(is_read=True)
    return render(request, "social/notifications.html", {"notifications": notifs})
