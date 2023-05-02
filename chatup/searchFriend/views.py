from django.shortcuts import render
from post.models import *
from user.models import *
from .utils.search import *
from django.urls import reverse
from django.http import HttpResponseRedirect

def searchFriend(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user:signin'))
    
    search = request.GET.get('search', "")
    friends = []
    friends += searchFriendByID(search)
    friends += searchFriendByPhone(search)
    if len(friends) == 0:
        friends = UserInfo.objects.all()
    context = {
        'friends': friends,
        }

    template = 'searchFriend/searchFriend.html'
    return render(request, template, context)

def friend(request, username):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user:signin'))
    
    userInfo = UserInfo.objects.get(user_id=request.user)
    friend = User.objects.get(username=username)
    friendInfo = UserInfo.objects.get(user_id=friend)
    if userInfo == friendInfo:
        return HttpResponseRedirect(reverse('user:profile'))
    friend_status = "notyetAppfriend"
    try:
        friend_status = Friend.objects.get(user_id=userInfo, friend_id=friendInfo)
    except:
        pass
    relation = False
    try:
        relation = Friend.objects.get(user_id=userInfo, friend_id=friendInfo).status
    except:
        pass
    
    all_post_and_image = {}

    if relation: 
        all_post = Post.objects.filter(created_by=friendInfo).order_by("-created_at")
    else:
        all_post = []

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
        
    if friend == request.user:
        return HttpResponseRedirect(reverse('user:index'))
    else:
        return render(request, 'searchFriend/friend.html', {
            'friendInfo': friendInfo,
            'friend_status': friend_status,
            'all_post_and_image': all_post_and_image
        })