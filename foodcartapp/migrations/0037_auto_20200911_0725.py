# Generated by Django 3.0.7 on 2020-09-11 07:25

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0036_auto_20200911_0706'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='registrated_at',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, verbose_name='Время заказа'),
        ),
    ]
