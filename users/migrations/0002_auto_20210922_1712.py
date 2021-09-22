# Generated by Django 3.2.7 on 2021-09-22 17:12

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='address',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='адрес'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='other_contact',
            field=models.CharField(blank=True, max_length=100, verbose_name='Прочий контакт'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='phonenumber',
            field=phonenumber_field.modelfields.PhoneNumberField(default=0, max_length=128, region=None, verbose_name='Мобильный номер'),
            preserve_default=False,
        ),
    ]
