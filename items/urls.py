from django.urls import path


from items.views import index, item_detail, new_item

urlpatterns = [
    path('', index, name='index'),
    path('items/<int:pk>', item_detail, name='item_detail'),
    path('new_item/', new_item, name='new_item'),
]
