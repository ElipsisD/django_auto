# Generated by Django 4.1.7 on 2023-04-09 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autos', '0006_alter_spare_price_graph'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='difference',
            field=models.SmallIntegerField(default=0, verbose_name='отличие от предыдущей цены'),
        ),
    ]
