from django.shortcuts import render, get_object_or_404

from items.models import Item, Category


def index(request):
    items = Item.objects.all()
    categories = Category.objects.all()
    return render(request, 'items/index.html', {'items': items, 'categories': categories})


def item_detail(request, pk):
    item = get_object_or_404(Item, id=pk)
    return render(request, 'items/detail.html', {'item': item})
