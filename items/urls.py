from django.urls import path


from items.views import index, item_detail, new_item, send_offer, \
    offers, user_items

urlpatterns = [
    path('', index, name='index'),
    path('items/<int:pk>', item_detail, name='item_detail'),
    path('new_item/', new_item, name='new_item'),
    path('send_offer/<int:pk>', send_offer, name='send_offer'),
    path('offers/', offers, name='offers'),
    path('user_items/<int:pk>', user_items, name='user_items'),
]
