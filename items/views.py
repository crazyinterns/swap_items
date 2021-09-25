from django.shortcuts import render, get_object_or_404, redirect

from items.models import Item, Category, Image
from django.contrib.auth.decorators import login_required
from items.forms import ItemForm
from django.http import HttpResponseRedirect
from django.shortcuts import reverse
from django.core.paginator import Paginator
from django.conf import settings
from users.models import CustomUser


def index(request):
    items = Item.objects.all()
    categories = Category.objects.all()

    category_name = request.GET.get('category')

    if category_name:
        items = items.filter(category__title=category_name)

    paginator = Paginator(items, settings.ITEMS_PER_PAGE)

    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    is_paginated = page.has_other_pages()

    return render(
        request,
        'items/index.html',
        {
            'page_obj': page,
            'is_paginated': is_paginated,
            'categories': categories,
            'category': category_name
        }
    )


def item_detail(request, pk):
    item = get_object_or_404(Item, id=pk)
    user = request.user

    context = {'user': user, 'item': item}

    return render(request, 'items/detail.html', context)


@login_required
def offers(request):
    items = request.user.items.filter(items_to_swap__isnull=False)
    items_to_swap = set()

    for item in items:
        items_to_swap.update(item.items_to_swap.all())

    paginator = Paginator(items, settings.ITEMS_PER_PAGE)

    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    is_paginated = page.has_other_pages()

    context = {
        'page_obj': page,
        'is_paginated': is_paginated,
        'items_to_swap': items_to_swap
    }

    return render(request, 'items/offers.html', context)


@login_required
def send_offer(request, pk):
    if request.method == 'POST':
        wanted_item = get_object_or_404(Item, id=pk)
        item_to_offer_id = request.POST.get('items_to_offer')
        if item_to_offer_id:
            item_to_offer = get_object_or_404(Item, id=item_to_offer_id)
            wanted_item.items_to_swap.set([item_to_offer])
            return HttpResponseRedirect(reverse('item_detail', args=[pk]))
    return HttpResponseRedirect(reverse('index'))


@login_required
def new_item(request):
    user = request.user
    if request.method != 'POST':
        item_form = ItemForm(
            phonenumber=user.phonenumber,
            email=user.email,
            other_contact=user.other_contact
        )
    else:
        item_form = ItemForm(
            data=request.POST,
            phonenumber=user.phonenumber,
            email=user.email,
            other_contact=user.other_contact
        )
        files = request.FILES.getlist('images')
        if item_form.is_valid():

            cleaned_data = item_form.cleaned_data
            item = Item(
                title=cleaned_data['title'],
                description=cleaned_data['description'],
                category=cleaned_data['category'],
                owner=user
            )
            item.save()
            images = [Image(img=file, item=item) for file in files]

            item.images.set(images, bulk=False)

            return HttpResponseRedirect(reverse('item_detail', args=[item.id]))
    return render(request, 'items/new_item.html', {'item_form': item_form})


def user_items(request, pk):
    user = get_object_or_404(CustomUser, id=pk)
    items = Item.objects.filter(owner=user)

    paginator = Paginator(items, settings.ITEMS_PER_PAGE)

    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    is_paginated = page.has_other_pages()

    return render(
        request,
        'items/user_items.html',
        {
            'page_obj': page,
            'is_paginated': is_paginated,
            'user_details' : user
        }
    )
