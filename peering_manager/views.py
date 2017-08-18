from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.utils.http import is_safe_url

from .forms import LoginForm


def login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            # Check where should the user be redirected
            next_redirect = request.POST.get('next', '')
            if not is_safe_url(url=next_redirect, host=request.get_host()):
                next_redirect = reverse('peering:home')

            auth_login(request, form.get_user())
            messages.info(request, "Logged in as {}.".format(request.user))
            return HttpResponseRedirect(next_redirect)
    else:
        form = LoginForm()

    return render(request, 'auth/login.html', {'form': form})


def logout(request):
    auth_logout(request)
    messages.info(request, "You have logged out.")
    return redirect('peering:home')
