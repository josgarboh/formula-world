from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from web.models import User

class RegistroForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'email')
    
    def save(self, commit=True):
        user = super(RegistroForm, self).save(commit=False)
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    username_or_email = forms.CharField(label='Nombre de usuario o correo electrónico')
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
