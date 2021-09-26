from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import reverse
from django.core.paginator import Paginator
from django.conf import settings
from django.db.models import Q

from users.models import CustomUser
from items.models import Item, Category, Image, Offer
from items.forms import ItemForm, ItemChangeForm


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
    offered_items = item.item_to_swap_offers.filter(item_to_swap__owner=user).order_by('-created_at')

    context = {
        'user': user,
        'item': item,
        'can_delete': settings.CAN_DELETE_ON_PAGE,
        'offered_items': offered_items
    }

    return render(request, 'items/detail.html', context)


@login_required
def offers(request):
    user = request.user

    sorting = request.GET.get('sorting')

    if sorting == 'asc':
        sort_by = 'created_at'
    else:
        sort_by = '-created_at'

    if request.GET.get('type') == 'wishlist':
        offers = Offer.objects.filter(item_to_swap__owner=user, is_accepted=False).order_by(sort_by)
        title = 'Мой список желаний'
    elif request.GET.get('type') == 'matched':
        offers = Offer.objects.filter(
            Q(item_to_swap__owner=user, is_accepted=True) |
            Q(wanted_item__owner=user, is_accepted=True)
        ).order_by(sort_by)
        title = 'Принятые предложения'
    else:
        offers = Offer.objects.filter(wanted_item__owner=user, is_accepted=False).order_by(sort_by)
        title = 'Мне предлагают'

    paginator = Paginator(offers, settings.ITEMS_PER_PAGE)

    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    is_paginated = page.has_other_pages()

    context = {
        'page_obj': page,
        'is_paginated': is_paginated,
        'offers': offers,
        'title': title
    }

    return render(request, 'items/offers.html', context)


@login_required
def send_offer(request, pk):
    if request.method == 'POST':
        wanted_item = get_object_or_404(Item, id=pk)
        item_to_offer_id = request.POST.get('items_to_offer')
        if item_to_offer_id:
            item_to_offer = get_object_or_404(Item, id=item_to_offer_id)

            offers = Offer.objects.filter(item_to_swap=wanted_item, wanted_item=item_to_offer)

            if offers:
                offer = offers[0]
                offer.is_accepted = True
                offer.save()
            else:
                Offer.objects.create(
                    wanted_item=wanted_item,
                    item_to_swap=item_to_offer
                )
            return HttpResponseRedirect(reverse('wishlist'))
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
                owner=user,
                address=cleaned_data['address']
            )
            item.save()
            images = [Image(img=file, item=item) for file in files]

            item.images.set(images, bulk=False)

            return HttpResponseRedirect(reverse('item_detail', args=[item.id]))
    return render(request, 'items/new_item.html', {'item_form': item_form})


@login_required
def edit_item(request, pk):
    item = get_object_or_404(Item, id=pk)
    if request.method != 'POST':
        item_form = ItemChangeForm(instance=item)
    else:
        item_form = ItemChangeForm(
            data=request.POST,
        )
        files = request.FILES.getlist('images')
        if item_form.is_valid():

            cleaned_data = item_form.cleaned_data

            item.title = cleaned_data['title']
            item.description = cleaned_data['description']
            item.category = cleaned_data['category']
            item.address = cleaned_data['address']

            if files:
                images = [Image(img=file, item=item) for file in files]
                item.images.set(images, bulk=False)
            item.save()

            return HttpResponseRedirect(reverse('item_detail', args=[item.id]))

    return render(
        request,
        'items/edit_item.html',
        {
            'item': item,
            'item_form': item_form,
            'can_delete': settings.CAN_DELETE_ON_PAGE
        }
    )


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
            'user_details': user
        }
    )


@login_required(login_url='/users/login/')
def delete_item(request, pk):
    if request.method == 'POST':
        user = request.user
        item = get_object_or_404(Item, id=pk)
        item.delete()
        return HttpResponseRedirect(reverse('profile', args=[user.id]))


@login_required(login_url='/users/login/')
def delete_image(request, pk):
    if request.method == 'POST':
        image = get_object_or_404(Image, id=pk)
        image.delete()
        return HttpResponseRedirect(reverse('edit_item', args=[image.item.id]))
