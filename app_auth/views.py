from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import ExtendedUserCreationForm
from django.http import HttpResponse
import sqlite3

def login_view(request):
    redirect_url = reverse('main_page')
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect(redirect_url)
        else:
            return render(request, 'app_auth/login.html')
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect(redirect_url)
    return render(request, 'app_auth/login.html')


@login_required(login_url=reverse_lazy('login'))
def profile_view(request):
    connection = sqlite3.connect('./db.sqlite3', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Inventory')
    inventory = [list(i) for i in cursor.fetchall()]
    cursor.close()
    data = {"my_inventory": [[i[1], i[2], i[3]] for i in inventory if i[4]==str(request.user)]}
    return render(request, 'app_auth/profile.html', context=data)


def logout_view(request):
    logout(request)
    return redirect(reverse('login'))


def register_view(request):
    if request.method == "POST":
        form = ExtendedUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(username=user.username, password=request.POST['password1'])
            login(request, user=user)
            return redirect(reverse('profile'))
    else:
        form = ExtendedUserCreationForm()
    context = {
        'form': form
    }
    return render(request, 'app_auth/register.html', context)
