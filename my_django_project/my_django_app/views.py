from django.shortcuts import render, redirect
from django.http import HttpResponse
from my_django_app.models import *
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
import os
from django.conf import settings
from datetime import datetime

# Create your views here.

def home(request):
    return render(request, 'home.html')

def contact(request):
    return render(request, 'contact.html')

def about_us(request):
    return render(request, 'about.html')

def user_options(request):
    is_logged_in = request.user.id
    return render(request, 'user_options.html', {'is_logged_in':is_logged_in} )

def register(request):
    if request.method == "POST":
        user_name = request.POST.get("username")
        user_email = request.POST.get("useremail")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Password does not match!")
            return render(request, 'register.html')
        
        if User.objects.filter(username = user_name).exists():
            messages.error(request, "The username already exists!")
            return render(request, 'register.html')
        
        if User.objects.filter(email = user_email).exists():
            messages.error(request, "The email already exists!")
            return render(request, 'register.html')
        
        user = User.objects.create_user(username = user_name, email = user_email, password = password1)
        user.save()

        login(request, user)

        messages.success(request, "You were registered successfully")

        return redirect('profile')

    else:
        return render(request, 'register.html')
    
def user_login(request):
    if request.method == "POST":
        user_name = request.POST.get("username")
        user_password = request.POST.get("password")
        user = authenticate(request, username = user_name, password = user_password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful.")
            return redirect('profile')
        else:
            messages.error(request, "Either email or password is incorrect")
            return render(request, 'login.html')

    else:
        return render(request, 'login.html')
    

def user_profile(request):
    if request.method == "GET":
        User_Id = request.user.id
        print(User_Id, "my_user_id")
        user_profile_data = users_profile.objects.filter(user_id = User_Id).values()
        if user_profile_data:
            information = list(user_profile_data)[0]

            image_url = os.path.join(settings.MEDIA_URL, "profile_images", information["user_image"])

            user_profile_info = {
            "name": information["user_name"],
            "age":information["user_age"],
            "hobby":information["user_hobby"],
            "city":information["user_city"],
            "profile_image": image_url
            }
            return render(request, 'profile.html', user_profile_info)
        else:
            return render(request, 'profile_questions.html')
    if request.method == "POST":
        U_Id = request.user.id
        u_name = request.POST.get("u_name")
        u_city = request.POST.get("u_city")
        u_age = request.POST.get("u_age")
        u_hobby = request.POST.get("u_hobby")
        u_file = request.FILES["u_image"]


        file_name = u_file.name
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        modified_file_name = f"{file_name.split('.')[0]}_{timestamp}.{file_name.split('.')[-1]}"

        user_profile_image_path = os.path.join(settings.MEDIA_ROOT, "profile_images", modified_file_name)

        with open(user_profile_image_path, "wb+") as destination:
            for chunk in u_file.chunks():
                destination.write(chunk)

        print(modified_file_name)

        profile_information = users_profile(user_id = U_Id,
                                            user_name = u_name,
                                            user_age = u_age,
                                            user_city = u_city,
                                            user_hobby = u_hobby,
                                            user_image = modified_file_name)
        
        profile_information.save()

        image_url = os.path.join(settings.MEDIA_URL, "profile_images", modified_file_name)

        user_profile_info = {
            "name": u_name,
            "age":u_age,
            "hobby":u_hobby,
            "city":u_city,
            "profile_image": image_url
        }

        return render(request, 'profile.html', user_profile_info)
    
def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('my_home')