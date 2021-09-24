from django.shortcuts import render

from django.urls import reverse_lazy
from users.forms import CustomUserCreationForm

from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth import logout, authenticate, login
from users.forms import CustomUserCreationForm
from django.shortcuts import reverse
from django.shortcuts import render, get_object_or_404
from users.models import CustomUser
from users.forms import CustomUserChangeForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.conf import settings


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
    return render(request, 'registration/register.html', context)


@login_required
def profile(request, pk):
    user = get_object_or_404(CustomUser, id=pk)
    items = user.items.all()
    paginator = Paginator(items, settings.ITEMS_PER_PAGE)

    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    is_paginated = page.has_other_pages()

    if user != request.user:
        raise Http404

    if request.method != 'POST':
        form = CustomUserChangeForm(instance=user)
    else:
        form = CustomUserChangeForm(instance=user, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('profile', args=[user.id]))
    return render(
        request,
        'users/profile.html',
        {
            'user_form': form,
            'page_obj': page,
            'is_paginated': is_paginated
        }
    )
