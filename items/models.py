from django.db import models

from users.models import CustomUser


class Category(models.Model):
    title = models.CharField(verbose_name='Категория', max_length=50)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self): return self.title


class Item(models.Model):
    title = models.CharField(max_length=100, verbose_name='название')
    description = models.TextField(blank=True, verbose_name='описание')
    category = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE,
        verbose_name='категория',
        related_name='items'
    )
    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='владелец',
        related_name='items'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    address = models.CharField(
        'адрес',
        max_length=100,
        blank=True,
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'предмет на обмен'
        verbose_name_plural = 'предметы на обмен'
        ordering = ['-created_at', 'title']


class Offer(models.Model):
    wanted_item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        verbose_name='желаемая вещь',
        related_name='item_offers'

    )
    item_to_swap = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        verbose_name='вещь, предлагаемая на обмен',
        related_name='item_to_swap_offers'
    )
    is_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.wanted_item.title} - {self.item_to_swap.title}'

    class Model:
        verbose_name = 'предложение на обмен'
        verbose_name_plural = 'предложения на обмен'
        ordering = ['-created_at']


class Image(models.Model):
    img = models.ImageField(upload_to='images')
    item = models.ForeignKey(
        'Item',
        on_delete=models.CASCADE,
        related_name='images'
    )

    def __str__(self):
        return f'{self.id}. Изображение для {self.item.title}'

    class Meta:
        verbose_name = 'изображение'
        verbose_name_plural = 'изображения'
