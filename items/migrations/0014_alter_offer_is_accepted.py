# Generated by Django 3.2.7 on 2021-09-26 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0013_rename_is_accept_offer_is_accepted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='is_accepted',
            field=models.BooleanField(default=None, null=True),
        ),
    ]
