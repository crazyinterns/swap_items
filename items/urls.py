from django.urls import path


from items.views import index, item_detail, new_item, send_offer, \
    offers, user_items, delete_item, edit_item, delete_image

urlpatterns = [
    path('', index, name='index'),
    path('items/<int:pk>', item_detail, name='item_detail'),
    path('new_item/', new_item, name='new_item'),
    path('send_offer/<int:pk>', send_offer, name='send_offer'),
    path('offers/', offers, name='offers'),
    path('user_items/<int:pk>', user_items, name='user_items'),
    path('delete_item/<int:pk>', delete_item, name='delete_item'),
    path('edit_item/<int:pk>', edit_item, name='edit_item'),
    path('delete_image/<int:pk>', delete_image, name='delete_image'),
]
