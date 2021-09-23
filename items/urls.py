from django.urls import path


from items.views import index, item_detail

urlpatterns = [
    path('', index, name='index'),
    path('items/<int:pk>', item_detail, name='item_detail')
]