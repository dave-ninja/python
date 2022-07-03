from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import TextInput
from .models import Profile


countries = (
    ('Germany', 'Germany'),
    ('Armenia', 'Armenia'),
    ('Greece', 'Greece')
)

class SignupForm(UserCreationForm):
    # fname = forms.CharField(max_length=200, help_text='Required')
    # country = forms.CharField(max_length=200, help_text='Required')
    # email = forms.EmailField(max_length=200, help_text='Required')
    username = forms.CharField(widget=TextInput(
        attrs={'class': 'form-control'}))

    email = forms.CharField(widget=TextInput(
        attrs={'class': 'form-control'}))

    phone = forms.CharField(widget=TextInput(
        attrs={'class': 'form-control'}))

    last_name = forms.ChoiceField(choices=countries, widget=forms.Select(
        attrs={'class': 'form-control'}))

    password1 = forms.CharField(widget=TextInput(
        attrs={'class': 'form-control', 'type': 'password'}))

    password2 = forms.CharField(widget=TextInput(
        attrs={'class': 'form-control', 'type': 'password'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'phone', 'last_name', 'password1', 'password2')

# Create a UserUpdateForm to update username and email
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    phone = forms.CharField()

    class Meta:
        model = User
        fields = ['username', 'email', 'phone']


# Create a ProfileUpdateForm to update image
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']