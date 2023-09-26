from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from web.models import User

class RegistroForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email', 'first_name', 'last_name')
    
    def save(self, commit=True):
        user = super(RegistroForm, self).save(commit=False)
        if commit:
            user.save()
        return user
    
    def __init__(self, *args, **kwargs):
        super(RegistroForm, self).__init__(*args, **kwargs)
        self.fields['password1'].help_text = 'Tu contraseña debe ser de al menos 8 caracteres, no completamente numérica y no contener tu username.'

class LoginForm(forms.Form):
    username_or_email = forms.CharField(label='Nombre de usuario o correo electrónico')
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
