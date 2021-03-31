from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse

#from django.contrib import messages

from django.contrib.auth.models import User
from .forms import *

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm

from django.shortcuts import get_object_or_404

from stronghold.decorators import public


# Create your views here.

def book_boost(request):
    return render(
        request,
        "BoostApp/book_boost.html",
    )

def advertiser_boosts(request):
    return render(
        request,
        "BoostApp/advertiser_boosts.html",
    )

def signup(request):
    return render(
        request,
        "BoostApp/signup.html",
    )

def booster_boosts(request):
    return render(
        request,
        "BoostApp/booster_boosts.html",
    )

@public
def price_list(request):
    boosts = Boost.objects.all()
    return render(request, "BoostApp/price_list.html", {'boosts':boosts})

@public
def create_account(request):
    if request.method == 'POST':
        form = UserRegister(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")
    else:
        form = UserRegister()
    return render(request, "BoostApp/create_account.html", {'form':form})

def account(request):
    return render(
        request,
        "BoostApp/account.html",
    )

def boost_options(request):
    if request.method == 'POST':
        form = DeleteBoostForm(request.POST)
        if form.is_valid():
            id = form.cleaned_data['boostId']
            Boost.objects.filter(boostId=id).delete()
            return redirect("/boost_options/")
    else:
        form = DeleteBoostForm()
    boosts = Boost.objects.all()
    return render(request, "BoostApp/admin_boost_options.html", {'boosts': boosts, 'form':form})

def add_boost_option(request):
    if request.method == 'POST':
        form = AddBoostOption(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/boost_options/")
    else:
        form = AddBoostOption()
    return render(request, "BoostApp/admin_add_boost_option.html", {'form':form})

def accounts(request):
    if request.method == 'POST':
        if 'delete-account-button' in request.POST:
            form = DeleteUserForm(request.POST)
            if form.is_valid():
                userId = form.cleaned_data['userId']
                User.objects.filter(id=userId).delete()
                return redirect("/accounts/")
        if 'edit-account-button' in request.POST:
            form = DeleteUserForm(request.POST)
            if form.is_valid():
                request.session['userId'] = form.cleaned_data['userId']
                return redirect("/edit_account/")
    else:
        form = DeleteUserForm()
    roles = Profile.objects.all()
    accounts = User.objects.all()
    advertisers = Advertiser.objects.all()
    boosters = Booster.objects.all()
    return render(request, "BoostApp/admin_accounts.html", {'roles':roles, 'accounts':accounts, 'advertisers':advertisers, 'boosters':boosters, 'form':form})


def edit_account(request):
    if request.method == 'POST':
        instance1 = get_object_or_404(User, id=request.session['userId'])
        userForm = EditUserForm(request.POST, instance=instance1, prefix="user")
        instance2 = get_object_or_404(Profile, user_id=request.session['userId'])
        roleForm = EditUserRoleForm(request.POST, instance=instance2, prefix="role")
        prevRole = instance2.userRole
        if request.POST['role-userRole'] == 'Advertiser' or request.POST['role-userRole'] == 'Booster':
            advertiserForm = EditAdvertiserForm(request.POST, prefix="advertiser")
            if prevRole == 'Advertiser' or prevRole == 'Booster':
                instance3 = get_object_or_404(Advertiser, user_id=instance1.id)
                advertiserForm = EditAdvertiserForm(request.POST, instance=instance3, prefix="advertiser")
            if advertiserForm.is_valid():
                if prevRole == 'User':
                    tempAdv = advertiserForm.save(commit=False)
                    tempAdv.user_id = instance1.id
                    tempAdv.save()
                else:
                    advertiserForm.save()
            if request.POST['role-userRole'] == 'Booster':
                boosterForm = EditBoosterForm(request.POST, prefix="booster")
                if prevRole == 'Booster':
                    instance4 = get_object_or_404(Booster, advertiser_id=instance3.user_id)
                    boosterForm = EditBoosterForm(request.POST, instance=instance4, prefix="booster")
                if boosterForm.is_valid():
                    if prevRole == 'User' or prevRole == 'Advertiser':
                        tempBooster = boosterForm.save(commit=False)
                        tempBooster.advertiser_id = instance1.id
                        tempBooster.save()
                    else:
                        boosterForm.save()
        if userForm.is_valid() and roleForm.is_valid():
            userForm.save()
            roleForm.save()
        if prevRole == 'Booster' and request.POST['role-userRole'] == 'Advertiser':
            Booster.objects.filter(advertiser_id=request.session['userId']).delete()
        elif (prevRole == 'Booster' and request.POST['role-userRole'] == 'User') or (prevRole == 'Advertiser' and request.POST['role-userRole'] == 'User'):
            Advertiser.objects.filter(user_id=request.session['userId']).delete()
        return redirect("/accounts/") 
    userData = User.objects.get(id=request.session['userId'])
    roleData = Profile.objects.get(user_id=request.session['userId'])
    userForm = EditUserForm(instance=userData, prefix="user")
    roleForm = EditUserRoleForm(instance=roleData, prefix="role")
    advertiserForm = EditAdvertiserForm(prefix="advertiser")
    boosterForm = EditBoosterForm(prefix="booster")
    if Advertiser.objects.filter(user_id=request.session['userId']).exists():
        advertiserData = Advertiser.objects.get(user_id=request.session['userId'])
        advertiserForm = EditAdvertiserForm(instance=advertiserData, prefix="advertiser")
        if Booster.objects.filter(advertiser_id=advertiserData.user_id):
            boosterData = Booster.objects.get(advertiser_id=advertiserData.user_id)
            boosterForm = EditBoosterForm(instance=boosterData, prefix="booster")
    return render(request, "BoostApp/admin_edit_account.html", {'userForm':userForm, 'roleForm':roleForm, 'advertiserForm':advertiserForm, 'boosterForm':boosterForm, 'userData':userData})
