
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'Enter your name',
        'class' : 'w-full py-3 px-6 rounded-xl mb-2' 
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Enter your password',
        'class' : 'w-full py-3 px-6 rounded-xl mb-2' 
    }))


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'Enter your name',
        'class' : 'w-full py-3 px-6 rounded-xl mb-2' 
    }))

    email = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder':'Enter your email address',
        'class' : 'w-full py-3 px-6 rounded-xl mb-2 ' 
    }))

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Enter your password',
        'class' : 'w-full py-3 px-6 rounded-xl mb-2' 
    }))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Enter your password again',
        'class' : 'w-full py-3 px-6 rounded-xl mb-2' 
    }))