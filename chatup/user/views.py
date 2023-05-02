from django.shortcuts import render, redirect
from chat.models import Notification
from post.models import Post
from user.models import *
from post.models import *
from django.http import HttpResponseRedirect, HttpResponse
from twilio.rest import Client
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

account_sid = "AC3607d951e9f16551ff392e66a5086414"
auth_token = "4d251cb5cbb2b470be11874ace98e0f5"
verify_sid = "VAc62028483f915539917bf2ee4e83b839"


def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user:signin'))

    # user = User.objects.get(username=request.user.username)
    # userInfo = UserInfo.objects.get(user_id=user)

    # all_post = Post.objects.all()
    # return render(request, 'post/post.html', {
    #     'userInfo': userInfo,
    #     'all_post': all_post
    # })  # change to post/..
    return HttpResponseRedirect(reverse('post:post'))



def verify_otp(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user:index'))
    
    if request.method == 'POST':
        otp_code = request.POST['otp']
        client = Client(account_sid, auth_token)
        verification_check = client.verify.v2.services(verify_sid) \
            .verification_checks \
            .create(to=request.session['prefixPhoneNumber']+request.session['phonenumber'][1:], code=otp_code)

        if verification_check.status == "approved":
            user = User.objects.create_user(
                request.session['username'], request.session['email'], request.session['password'])
            user.first_name = request.session['firstname']
            user.last_name = request.session['lastname']
            user.save()

            UserInfo.objects.create(user_id=user, prefix_phone_number=request.session['prefixPhoneNumber'], phone_number=request.session[
                                    'phonenumber'], chatup_id=request.session['chatupid'], profile_image='./static/assets/default_profile_image/default.jpg', 
                                    last_logout=timezone.now())

            return redirect('user:signin')
        else:
            return render(request, 'user/verify_otp.html', {
                'message': 'Invalid OTP. Please try again.'
            })
    return render(request, 'user/verify_otp.html')


def signin(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user:index'))
    
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('post:post'))
        else:
            return render(request, 'user/signin.html', {
                'message': 'Invalid credentials.'
            })
    return render(request, 'user/signin.html')


def signup(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user:index'))
    
    if request.method == "POST":
        umessage = ''
        pmessage = ''
        phmessage = ''
        idmessage = ''

        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        username = request.POST["username"]
        email = request.POST["email"]
        prefixPhoneNumber = request.POST["prefixPhoneNumber"]
        phonenumber = request.POST["phonenumber"]
        chatupid = request.POST["chatupid"]
        password = request.POST["password"]
        confirmpassword = request.POST["confirmpassword"]

        # check phonenumber
        if phonenumber == '':
            phmessage = 'Please Enter Phone Number.'
        elif (prefixPhoneNumber == '+66' and len(phonenumber) == 9):
            phonenumber = '0' + phonenumber
        elif (len(phonenumber) < 7):
            phmessage = 'Invalid Phone Number.'

        phone = UserInfo.objects.filter(phone_number=phonenumber).count()
        if phone != 0:
            phmessage = 'This Phone Number is already taken.'
        # check chatup id
        if chatupid == '':
            idmessage = 'Please Enter ChatUp Id.'
        else:
            userinfo = UserInfo.objects.filter(chatup_id=chatupid).count()
            if userinfo != 0:
                idmessage = 'This ChatUp Id is already taken.'

        # check username
        if username == '':
            umessage = 'Please Enter Username.'
        else:
            user = User.objects.filter(username=username).count()
            if user != 0:
                umessage = 'This Username is already taken.'

        # check password
        if password == '':
            pmessage = 'Please Enter Password.'
        if password != confirmpassword:
            pmessage = 'Confirm Password is not same as password.'

        if umessage == '' and pmessage == '' and phmessage == '' and idmessage == '':
            request.session['firstname'] = firstname
            request.session['lastname'] = lastname
            request.session['username'] = username
            request.session['email'] = email
            request.session['prefixPhoneNumber'] = prefixPhoneNumber
            request.session['phonenumber'] = phonenumber
            request.session['chatupid'] = chatupid
            request.session['password'] = password

            client = Client(account_sid, auth_token)
            verification = client.verify.v2.services(verify_sid) \
                .verifications \
                .create(to=prefixPhoneNumber + phonenumber[1:], channel="sms")
            return redirect('user:verify_otp')
        else:
            return render(request, 'user/signup.html', {
                'phmessage': phmessage,
                'idmessage': idmessage,
                'usermessage': umessage,
                'passwordmessage': pmessage,
                'firstname': firstname,
                'lastname': lastname,
                'username': username,
                'email': email,
                'phonenumber': phonenumber,
                'chatupid': chatupid,
                'password': password,
                'confirmpassword': confirmpassword,
            })

    return render(request, 'user/signup.html')


def signout(request):
    logout(request)
    return render(request, 'user/signin.html', {
        'message': 'Logged out'
    })


def edit_profile(request):
    if not request.user.is_authenticated:
        return render(request, 'users/signin.html', status=403)

    user = User.objects.get(username=request.user.username)
    user_info = UserInfo.objects.get(user_id=user)

    if request.method == "POST":
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        try:
            profile_image = request.FILES.getlist('images')[0]
            user_info.profile_image = profile_image
            user_info.save()
        except:
            pass

        User.objects.filter(pk=request.user.id).update(
            first_name=firstname,
            last_name=lastname,
        )

        return redirect('/')

    return render(request, 'user/editprofile.html', {
        "user_info": user_info,
    })


def change_password(request):
    if not request.user.is_authenticated:
        return render(request, 'user/signin.html', status=403)

    user = User.objects.get(pk=request.user.id)
    user_info = UserInfo.objects.get(user_id=user)

    if request.method == "POST":
        old_password = request.POST['current_password']
        new_password = request.POST['new_password']
        con_password = request.POST['con_password']

        if (new_password == old_password) or (new_password != con_password) or (not user.check_password(old_password)):
            return render(request, "user/password.html", {
                'user_info': user_info,
                'message': 'Invalid password'
            })

        user.set_password(new_password)
        user.save()

        return redirect(reverse('user:signin'))
    else:
        return render(request, "user/password.html", {
            'user_info': user_info
        })
    
    
def profile(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user:signin'))

    userInfo = UserInfo.objects.get(user_id=request.user)

    if request.method == 'POST':
        detail = request.POST['detail']
        images = request.FILES.getlist('images')

        if detail != "":
            post = Post.objects.create(created_by=userInfo, detail=detail)

            for img in images:
                File.objects.create(file=img, post=post)

    all_post_and_image = {}
    all_post = Post.objects.filter(created_by=userInfo).order_by("-created_at")
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
        
    return render(request, 'user/user_profile.html', {
        'userInfo':userInfo,
        'all_post_and_image': all_post_and_image
    })


def change_phonenumber(request):
    pass
    # user = User.objects.get(pk=request.user)
    # subject = 'welcome to GFG world'
    # message = f'Hi {user.username}, thank you for registering in geeksforgeeks.'
    # email_from = settings.EMAIL_HOST_USER
    # recipient_list = [user.email, ]
    # send_mail( subject, message, email_from, recipient_list )


def noti(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user:signin'))
    
    user = User.objects.get(id=request.user.id)
    notifications = Notification.objects.filter(reciever=user).order_by('-created_at')[:30]
    context = {
        "notifications": notifications
    }
    return render(request, 'user/notification.html', context=context)


def get_profile_picture(request, id):
    try:
        with open(f'{UserInfo.objects.get(user_id=User.objects.get(id=id)).profile_image.path}', 'rb') as picture:
            return HttpResponse(picture.read(), content_type="image/jpeg")
    except:
        with open(f'user/static/user/images/d09bZgy.png', 'rb') as picture:
            return HttpResponse(picture.read(), content_type="image/jpeg")

def friend_list(request, user_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user:signin'))
    
    user = User.objects.get(id=user_id)
    userInfo = UserInfo.objects.get(user_id=user)
    all_friend = Friend.objects.filter(user_id=userInfo, status=True)

    return render(request, 'user/friendlist.html', {
        'all_friend': all_friend,
    })
