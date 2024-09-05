from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.views.generic import ListView

from mailapp.forms import StyleFormMixin
from users.models import User


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'name', 'password1', 'password2',)


class UserProfileForm(StyleFormMixin, UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'name', 'first_name', 'last_name', 'description', 'phone_number', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password'].widget = forms.HiddenInput()


class UserList(StyleFormMixin, ListView):
    class Meta:
        model = User
        fields = ('email', 'name', 'first_name', 'last_name', 'description', 'phone_number', 'avatar')

