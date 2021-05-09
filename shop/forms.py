from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms


class UserAdminCreationForm(UserCreationForm):
    """
    A Custom form for creating new users.
    """
    email = forms.CharField(max_length=76, required=True, widget=forms.EmailInput(attrs={
        'class': 'ap_email',
        'tabindex': 1,
        'autocomplete':
            'email', 'id':
            'ap_email'
    }))

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "ap_password1",
        "tabindex": 2,
        "autocomplete": "off",
        "maxlength": 1024,
        "id": "ap_password1",
        "placeholder": "At least 8 characters"
    }))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "ap_password2",
        "tabindex": 3,
        "autocomplete": "off",
        "maxlength": 1024,
        "id": "ap_password2",
        "placeholder": "Should be same as password"
    }))

    class Meta:
        model = get_user_model()
        fields = ['email']


class AuthenticateForm(AuthenticationForm):
    username = forms.CharField(widget=forms.EmailInput(attrs={
        'autofocus': True,
        "class": "ap_email",
        "tabindex": 1,
        "autocomplete": "email",
        "maxlength": 64,
        "id": "ap_email",
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'autocomplete': 'current-password',
        "class": "ap_password1",
        "tabindex": 2,
        "maxlength": 1024,
        "id": "ap_password1",
        "placeholder": "At least 8 characters",
    }))
