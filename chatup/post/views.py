from os import truncate
from django.shortcuts import redirect, render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from sympy import Min
from django.db.models import Q
from chat.models import Notification
from .models import *
from user.models import UserInfo, Friend
from django.utils import timezone
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from datetime import timedelta

def post(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user:signin'))

    user = User.objects.get(username=request.user.username)
    userInfo = UserInfo.objects.get(user_id=user)
    all_friend = Friend.objects.filter(user_id=userInfo, status=True)   
    
    if request.method == 'POST':
        detail = request.POST['detail']
        images = request.FILES.getlist('images')
        
        if detail != "":
            post = Post.objects.create(created_by=userInfo, detail=detail)

            for img in images:
                File.objects.create(file=img, post=post)
                
            for friend in all_friend:
                Notification.objects.create(
                    post = post,
                    detail=f"{user} has public new post",
                    reciever = friend.friend_id.user_id,
                    create_by = user,
                ).save()

    all_post = Post.objects.filter(Q(created_by=userInfo) | Q(created_by__in=all_friend.values('friend_id'))).order_by("-created_at")

    all_post_and_image = {}
    for post in all_post:
        image = File.objects.filter(post=post).first()
        all_comment = Comment.objects.filter(post=post)
        all_like = Like.objects.filter(post=post)
        post.count_comment = len(all_comment)
        post.count_like = len(all_like)
        like = ""
        try:
            like = Like.objects.get(post=post, created_by=userInfo)
        except:
            pass
        if(like != ""):
            post.like = True
        else:
            post.like = False
        all_post_and_image.update({post: image})

    return render(request, 'post/post.html', {
        'userInfo': userInfo,
        'all_post_and_image': all_post_and_image
    })
    
def view_post(request, post_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user:signin'))
    
    user = User.objects.get(username=request.user.username)
    userInfo = UserInfo.objects.get(user_id=user)

    post = Post.objects.get(id=post_id)

    relation = False
    try:
        if userInfo == post.created_by:
            relation = True
        else:
            relation = Friend.objects.get(user_id=userInfo, friend_id=post.created_by, status=True).status
    except:
        pass
    if relation:
        x=""
    else:
        return redirect(request.META.get('HTTP_REFERER', '/'))

    images = File.objects.filter(post=post)
    if request.method == 'POST':
        comment = request.POST['comment']
        if(comment != ""):
            c = Comment.objects.create(created_by=userInfo, post=post, detail=comment)
            if(userInfo != post.created_by):
                Notification.objects.create(
                    post=post,
                    comment=c,
                    detail=f"{request.user} comment on your post",
                    reciever = post.created_by.user_id,
                    create_by = request.user
                )
        return redirect("post:view_post", post_id)

    all_comment = Comment.objects.filter(post=post).order_by("-created_at")
    all_like = Like.objects.filter(post=post)
    post.count_comment = len(all_comment)
    post.count_like = len(all_like)

    like = ""
    try:
        like = Like.objects.get(post=post, created_by=userInfo)
    except:
        pass
    if(like != ""):
        post.like = True
    else:
        post.like = False
        
    return render(request, 'post/view_post.html', {
        'userInfo': userInfo,
        'post': post,
        'images': images,
        'all_comment': all_comment
    })

def delete_post(request, post_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user:signin'))

    post = Post.objects.get(id=post_id)

    if( request.user != post.created_by.user_id):
        return HttpResponseRedirect(reverse('post:post'))
    
    post.delete()
    return HttpResponseRedirect(reverse('post:post'))

def delete_comment(request, post_id, comment_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user:signin'))
    
    post = Post.objects.get(id=post_id)
    comment = Comment.objects.get(post=post, id=comment_id)
    id = comment.post.id
    
    if( request.user != comment.created_by.user_id):
        return HttpResponseRedirect(reverse('post:view_post', args=(id, )))
    
    comment.delete()
    return HttpResponseRedirect(reverse('post:view_post', args=(id, )))

def like_post(request, post_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user:signin'))

    userInfo = UserInfo.objects.get(user_id=request.user)
    post = Post.objects.get(id=post_id)
    like = None
    try:
        like = Like.objects.get(post=post, created_by=userInfo)
    except:
        pass
    if(like != None):
        like.delete()
        return redirect(request.META.get('HTTP_REFERER', '/'))
    
    l = Like.objects.create(created_by=userInfo, post=post)
    if(userInfo != post.created_by):
        Notification.objects.create(
                post=post,
                like=l,
                detail=f"{request.user} like on your post",
                reciever = post.created_by.user_id,
                create_by = request.user
            )
    return redirect(request.META.get('HTTP_REFERER', '/'))

