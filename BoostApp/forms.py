from django.forms import ModelForm
from django import forms
from .models import *
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from crispy_forms.helper import FormHelper

class UserRegister(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'username': _('Character'),}
        help_texts = {
            'username': 'The name and realm of your character. Format: Name-Realm.',}


class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        labels = {
            'username': _('Character'),}
        help_texts = {
            'username': None,}

class AddBoostOption(ModelForm):
    class Meta:
        model = Boost
        fields = ['boostId', 'boostType', 'name', 'level', 'price']
        labels = {
            }
        help_texts = {
            'boostId': 'Use the abbreviated name of the dungeon/raid along with the level. For example; Freehold level 14 would be FH14.',
            'level': 'For dungeons use the keystone level. For raids use the following: LFR = 1 | Normal = 2 | Heroic = 3 | Mythic = 4'}

class DeleteBoostForm(forms.Form):
    boostId = forms.CharField(max_length=6, label='Boost ID', widget=forms.HiddenInput(attrs={'size': 6, 'readonly': 'readonly'}))

class DeleteUserForm(forms.Form):
    userId = forms.CharField(max_length=3, label='User ID', widget=forms.HiddenInput(attrs={'size': 3, 'readonly': 'readonly'}))


class EditUserForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
    class Meta:
        model = User
        fields = ['username', 'email']
        labels = {
            'username': _('Character'),
            'email': _('Email'),}
        help_texts = {
            'username': None,}
        prefix = 'user'

class EditUserRoleForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
    class Meta:
        model = Profile
        fields = ['userRole']
        labels = {
            'userRole': _('Role'),}
        prefix = 'role'

class EditAdvertiserForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
    class Meta:
        model = Advertiser
        fields = ['balance', 'advRank', 'advCommission']
        labels = {
            'advRank': _('Advertiser Rank'),}
        prefix = 'advertiser'

class EditBoosterForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
    class Meta:
        model = Booster 
        fields = ['className', 'role', 'armourType']
        labels = {
            'className': _('Class'),
            'armourType': _('Armour Type'),}
        prefix = 'booster'
