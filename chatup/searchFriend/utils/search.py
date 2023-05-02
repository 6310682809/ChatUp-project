from user.models import *
def searchFriendByID(search):
    return UserInfo.objects.filter(chatup_id=search)
def searchFriendByPhone(search):
    phone = search.split(" ")
    if len(phone) != 2:
        return []
    return UserInfo.objects.filter(prefix_phone_number=phone[0], phone_number=phone[1])