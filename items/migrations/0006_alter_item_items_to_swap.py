# Generated by Django 3.2.7 on 2021-09-22 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0005_alter_item_items_to_swap'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='items_to_swap',
            field=models.ManyToManyField(blank=True, related_name='_items_item_items_to_swap_+', to='items.Item', verbose_name='вещи, которые хотят поменять'),
        ),
    ]
