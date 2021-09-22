from django.db import models


class Category(models.Model):
    title = models.CharField(verbose_name='Категория', max_length=50)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self): return self.title
