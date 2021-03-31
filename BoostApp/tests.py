"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import django
import pytest
#from django.test import TestCase
from .models import *
from .forms import *
from django.contrib.auth.models import User

from django import urls

from django_dynamic_fixture import G, P

from bs4 import BeautifulSoup

# TODO: Configure your database in settings.py and sync before running tests.

#class SimpleTest(TestCase):
#    """Tests for the application views."""

#    # Django requires an explicit setup() when running tests in PTVS
#    @classmethod
#    def setUpClass(cls):
#        super(SimpleTest, cls).setUpClass()
#        django.setup()

#    def test_basic_addition(self):
#        """
#        Tests that 1 + 1 always equals 2.
#        """
#        self.assertEqual(1 + 1, 2)

@pytest.fixture
def authenticated_user(client):
    user = G(User, username='Fazzadin-Doomhammer')
    user.set_password('password@12')
    user.save()
    assert client.login(username='Fazzadin-Doomhammer', password='password@12')
    return user

@pytest.fixture
def existing_user(client):
    user = G(User, username='Fazze-Turalyon')
    user.set_password('just@test!123')
    user.save()
    return user

@pytest.fixture
def existing_boost(client):
    boost = G(Boost, boostId='AD16', boostType='Dungeon', name='Atal\' Dazar', level=16, price=160000)
    boost.save()
    return boost

@pytest.fixture
def existing_advertiser(client):
    user = G(User, username='Hwangson-Doomhammer')
    user.set_password('just@test!456')
    user.save()
    id = User.objects.filter(username='Hwangson-Doomhammer')
    advertiser = G(Advertiser, user=id[0].id)
    advertiser.save()
    return user, advertiser

@pytest.fixture
def existing_booster(client):
    user = G(User, username='Desperado-Draenor')
    user.set_password('just@test!789')
    user.save()
    id = User.objects.filter(username='Desperado-Draenor')
    advertiser = G(Advertiser, user=id[0].id)
    advertiser.save()
    booster = G(Booster, advertiser=id[0].id)
    booster.save()
    return user, advertiser, booster

@pytest.mark.parametrize('view_name', ['login', 'create_account', 'price_list'])
@pytest.mark.django_db
def test_public_views(view_name, client):
    url = urls.reverse(view_name)
    resp = client.get(url)
    assert resp.status_code == 200

@pytest.mark.django_db
def test_redirect_to_account_when_logged_in(authenticated_user, client):
    url = urls.reverse('home')
    resp = client.get(url)
    assert resp.status_code == 302
    assert resp.url == urls.reverse('account')

def test_redirect_to_login_when_logged_out(client):
    url = urls.reverse('home')
    resp = client.get(url)
    assert resp.status_code == 302
    assert resp.url == urls.reverse('login')

@pytest.mark.django_db
def test_create_account(client):
    url = urls.reverse('create_account')
    resp = client.get(url)
    assert resp.status_code == 200
    resp = client.post(url, {
        'username': 'TestFazz-Test',
        'email':'testingfazz@gmail.com',
        'password1':'just@test!12',
        'password2':'just@test!12'
    })
    assert resp.status_code == 302
    assert resp.url == urls.reverse('home')
    assert User.objects.filter(username='TestFazz-Test').exists()

@pytest.mark.django_db
def test_delete_account(authenticated_user, existing_user, client):
    url = urls.reverse('accounts')
    resp = client.get(url)
    assert resp.status_code == 200
    id = User.objects.filter(username='Fazze-Turalyon')
    resp = client.post(url, {
        'userId': id[0].id,
        'delete-account-button': 'delete-account-button'  #simulate delete account button being pressed
    })
    assert resp.status_code == 302
    assert resp.url == urls.reverse('accounts')

    ######## TO DO: add assert that boost table has the correct entry removed
    assert not User.objects.filter(username='Fazze-Turalyon').exists()

@pytest.mark.django_db
def test_redirect_to_edit_account(authenticated_user, existing_user, client):
    id = User.objects.filter(username='Fazze-Turalyon')
    url = urls.reverse('accounts')
    resp = client.get(url)
    assert resp.status_code == 200
    resp = client.post(url, {
        'userId': id[0].id,
        'edit-account-button': 'edit-account-button'   #simulate edit account button being pressed
    })

    assert resp.status_code == 302
    assert resp.url == urls.reverse('edit_account')

@pytest.mark.django_db
def test_edit_account_user(authenticated_user, existing_user, client):
    id = User.objects.filter(username='Fazze-Turalyon')
    session = client.session
    session['userId'] = id[0].id
    session.save()
    url = urls.reverse('edit_account')
    resp = client.get(url)
    assert resp.status_code == 200

@pytest.mark.django_db
def test_edit_account_advertiser(authenticated_user, existing_advertiser, client):
    id = User.objects.filter(username='Hwangson-Doomhammer')
    session = client.session
    session['userId'] = id[0].id
    session.save()
    url = urls.reverse('edit_account')
    resp = client.get(url)
    assert resp.status_code == 200

@pytest.mark.django_db
def test_edit_account_booster(authenticated_user, existing_booster, client):
    id = User.objects.filter(username='Desperado-Draenor')
    session = client.session
    session['userId'] = id[0].id
    session.save()
    url = urls.reverse('edit_account')
    resp = client.get(url)
    assert resp.status_code == 200

################################################################################################################### TO DO HERE

## user to advertiser

## user to booster

## advertiser to booster

## booster to advertiser

## booster to user

## advertiser to user

@pytest.mark.django_db
def test_create_boost_option(authenticated_user, client):
    url = urls.reverse('add_boost_option')
    resp = client.get(url)
    assert resp.status_code == 200
    resp = client.post(url, {
        'boostId':'FH12',
        'boostType':'Dungeon',
        'name':'Freehold',
        'level': 12,
        'price': 145000
    })
    assert resp.status_code == 302
    assert resp.url == urls.reverse('boost_options')

    ####### TO DO: add assert that boost table has additional entry
    assert Boost.objects.filter(boostId='FH12').exists()

@pytest.mark.django_db
def test_delete_boost_option(authenticated_user, existing_boost, client):
    url = urls.reverse('boost_options')
    resp = client.get(url)
    assert resp.status_code == 200
    resp = client.post(url, {
        'boostId':'AD16',
        'boostType':'Dungeon',
        'name':'Atal\'Dazar',
        'level': 16,
        'price': 160000
    })
    assert resp.status_code == 302
    assert resp.url == urls.reverse('boost_options')

    ######## TO DO: add assert that boost table has the correct entry removed
    assert not Boost.objects.filter(boostId='AD16').exists()

@pytest.mark.django_db
def test_login_valid_details(existing_user, client):
    url = urls.reverse('login')
    resp = client.get(url)
    assert resp.status_code == 200
    resp = client.post(url, {
        'username':'Fazze-Turalyon',
        'password':'just@test!123'
    })
    assert resp.status_code == 302
    assert resp.url == urls.reverse('account')

# 'edit_account' not included below

@pytest.mark.parametrize('view_name', ['book_boost', 'advertiser_boosts', 'signup', 'booster_boosts', 'boost_options', 'add_boost_option', 'account', 'accounts'])
@pytest.mark.django_db
def test_protected_views(view_name, authenticated_user, client):
    url = urls.reverse(view_name)
    resp = client.get(url)
    assert resp.status_code == 200