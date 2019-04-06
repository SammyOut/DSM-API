from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class SignupForm(UserCreationForm):
    name = forms.CharField(max_length=16)
    number = forms.IntegerField()

    class Meta:
        model = get_user_model()
        fields = ('uuid', 'name', 'number', 'email', 'username', 'password1', 'password2',)


class LoginForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'password')
