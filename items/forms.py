from django import forms
from django.contrib.auth.models import User

class UserRegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [ 'username', 'first_name', 'last_name', 'password']

class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    fields = ['username', 'password']



