# Generated by Django 3.2.7 on 2021-09-25 07:36

from django.db import migrations


def fill_items_address(apps, schema_editor):
    Item = apps.get_model('items', 'Item')
    for item in Item.objects.all():
        item.address = (item.owner.address or 'Не задан')
        item.save()


def fill_items_address_reverse(apps, schema_editor):
    Item = apps.get_model('items', 'Item')
    for item in Item.objects.all():
        item.address = 'Не задан'
        item.save()


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0007_item_address'),
    ]

    operations = [
        migrations.RunPython(fill_items_address , reverse_code=fill_items_address_reverse),
    ]