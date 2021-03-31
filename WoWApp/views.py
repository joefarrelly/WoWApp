from django.shortcuts import render, redirect
from stronghold.decorators import public

@public
def home(request):
    if request.user.is_authenticated:
        return redirect("account")
    else:
        return redirect("login") # redirect to your page
