from django.urls import reverse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from user.models import *
from django.http import HttpResponse, HttpResponseRedirect
from chat.models import Notification
# Create your views here.


@login_required(redirect_field_name="", login_url="/signin")
def addFriend(request, id):
    friend = User.objects.get(id=id)
    friendInfo = UserInfo.objects.get(user_id=friend.id)
    userInfo = UserInfo.objects.get(user_id=request.user.id)
    if (Friend.objects.filter(user_id=userInfo, friend_id=friendInfo, status=True)):
        return HttpResponse("This guy is already your friend")

    if (friendInfo == userInfo):
        return HttpResponse("Can't add yourself to be your friend")
    # if not Friend.objects.filter(user_id=userInfo, friend_id=friendInfo):
    #     Friend.objects.create(
    #         user_id=userInfo,
    #         friend_id=friendInfo,
    #     ).save()
    
    # f = Friend.objects.get(user_id=userInfo, friend_id=friendInfo)
    # f.status = False
    # f.save()
    if (not Friend.objects.filter(user_id=friendInfo, friend_id=userInfo)):
        Friend.objects.create(
            user_id=friendInfo,
            friend_id=userInfo,
            status=False,
        ).save()
        f = Friend.objects.get(user_id=friendInfo, friend_id=userInfo)
        Notification.objects.create(
            add_friend=f,
            detail=f"{request.user} sent you a friend request",
            reciever=friend,
            create_by = request.user
        ).save()
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required(redirect_field_name="", login_url="/signin")
def deleteFriend(request, id):
    userInfo = UserInfo.objects.get(user_id=request.user.id)
    friend = User.objects.get(id=id)
    friendInfo = UserInfo.objects.get(user_id=friend)
    relation = Friend.objects.get(user_id = userInfo, friend_id = friendInfo)
    relation.delete()
    relation = Friend.objects.get(user_id = friendInfo, friend_id = userInfo)
    relation.delete()
    # if not relation:
    #     relation = Friend.objects.create(
    #         user_id = userInfo,
    #         friend_id = friendInfo,
    #         status = False
    #     )
    
    # relation.status = False
    # relation.save()
    # return HttpResponse(f"delete {friendInfo} from friend success")

    
    return HttpResponseRedirect(reverse('searchFriend:friend', args=(friendInfo.user_id.username, )))

@login_required(redirect_field_name="", login_url="/signin")
def acceptFriend(request, id):
    friend = User.objects.get(id=id)
    friendInfo = UserInfo.objects.get(user_id=friend.id)
    userInfo = UserInfo.objects.get(user_id=request.user.id)

    f = Friend.objects.get(user_id=userInfo, friend_id=friendInfo)
    f.status = True
    f.save()

    ff = Friend.objects.create(
            user_id=friendInfo,
            friend_id=userInfo,
            status=True,
        )

    Notification.objects.create(
            add_friend=ff,
            detail=f"{request.user} is accepted your friend request",
            reciever=friend,
            create_by = request.user
        )
    
    return HttpResponseRedirect(reverse('searchFriend:friend', args=(friendInfo.user_id.username, )))

@login_required(redirect_field_name="", login_url="/signin")
def rejectFriend(request, id):
    friend = User.objects.get(id=id)
    friendInfo = UserInfo.objects.get(user_id=friend)
    userInfo = UserInfo.objects.get(user_id=request.user)
    f = Friend.objects.get(user_id=userInfo, friend_id=friendInfo)

    f.delete()
    
    return HttpResponseRedirect(reverse('searchFriend:friend', args=(friendInfo.user_id.username, )))
