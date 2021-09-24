from django.shortcuts import render, get_object_or_404

from items.models import Item, Category, Image
from django.contrib.auth.decorators import login_required
from items.forms import ItemForm
from django.http import HttpResponseRedirect
from django.shortcuts import reverse
from django.core.paginator import Paginator
from django.conf import settings


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
    return render(request, 'items/detail.html', {'item': item})


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
