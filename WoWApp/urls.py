"""
WoWApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/

Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# Uncomment next two lines to enable admin:
from django.contrib import admin
from django.urls import path, include
from . import views as v
from BoostApp import views

urlpatterns = [
    # Uncomment the next line to enable the admin:
    path('admin/', admin.site.urls),
    path('', v.home, name='home'),
    path('account/', views.account, name='account'),
    path('create_account/', views.create_account, name='create_account'),
    path('book_boost/', views.book_boost, name='book_boost'),
    path('advertiser_boosts/', views.advertiser_boosts, name='advertiser_boosts'),
    path('signup/', views.signup, name='signup'),
    path('booster_boosts/', views.booster_boosts, name='booster_boosts'),
    path('price_list/', views.price_list, name='price_list'),
    path('', include("django.contrib.auth.urls")),
    path('boost_options/', views.boost_options, name='boost_options'),
    path('new_boost_option/', views.add_boost_option, name='add_boost_option'),
    path('accounts/', views.accounts, name='accounts'),
    path('edit_account/', views.edit_account, name='edit_account'),
]