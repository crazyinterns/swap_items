from django.shortcuts import render

from django.urls import reverse_lazy
from users.forms import CustomUserCreationForm

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import logout, authenticate, login
from users.forms import CustomUserCreationForm
from django.shortcuts import reverse


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    if request.method != 'POST':
        form = CustomUserCreationForm()
    else:
        form = CustomUserCreationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            authenticated_user = authenticate(
                username=new_user.username,
                password=request.POST['password1']
                )
            login(request, authenticated_user)
            return HttpResponseRedirect(reverse('login'))
    context = {'form': form}
    return render(request, 'register.html', context)
