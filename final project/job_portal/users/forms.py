from django import forms
from mainsite import models
from django.contrib.auth.forms import UserCreationForm


class UserRegistrationForm(UserCreationForm):
    role = forms.ChoiceField(choices=models.User.Role.choices, required=True)

    class Meta:
        model = models.User
        fields = ['username', 'email', 'role', 'password1', 'password2']



