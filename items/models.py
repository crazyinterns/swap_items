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
        'CustomUser',
        on_delete=models.CASCADE,
        verbose_name='владелец',
        related_name='items'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'предмет на обмен'
        verbose_name_plural = 'предметы на обмен'
        ordering = ['-created_at']