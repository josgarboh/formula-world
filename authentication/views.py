from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect, render
from django.views.decorators.http import require_safe

from . import forms
from .decorators import user_not_authenticated

@user_not_authenticated
def registro(request):

    if request.method == 'POST':
        form = forms.RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "¡Bienvenido a Fórmula World!")
            return redirect('landing')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    else:
        form = forms.RegistroForm()
    return render(request, "register.html", {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('landing')

@user_not_authenticated
def login_view(request):

    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data.get('username_or_email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username_or_email, password=password)
            if user is not None:
                login(request, user)
                return redirect('landing')
            else:
                messages.error(request, "El usuario o la contraseña introducidos no son correctos")
    else:
        form = forms.LoginForm()

    return render(request, "login.html", {'form': form})

