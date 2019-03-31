from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class SignupForm(UserCreationForm):
    name = forms.CharField(max_length=16)
    number = forms.IntegerField()

    class Meta:
        model = get_user_model()
        fields = ('uuid', 'name', 'number', 'email', 'username', 'password1', 'password2', )
