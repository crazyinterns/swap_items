from django.shortcuts import render, get_object_or_404

from items.models import Item, Category, Image
from django.contrib.auth.decorators import login_required
from items.forms import ItemForm
from django.http import HttpResponseRedirect
from django.shortcuts import reverse


def index(request):
    items = Item.objects.all()
    categories = Category.objects.all()
    return render(
        request,
        'items/index.html',
        {'items': items, 'categories': categories}
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
