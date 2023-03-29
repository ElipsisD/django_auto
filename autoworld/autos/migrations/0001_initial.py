# Generated by Django 4.1.6 on 2023-02-12 11:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Auto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(max_length=100, verbose_name='марка')),
                ('model', models.CharField(max_length=100, verbose_name='модель')),
                ('vin', models.CharField(max_length=17, verbose_name='VIN')),
                ('odo', models.PositiveIntegerField(verbose_name='пробег')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='владелец')),
            ],
            options={
                'verbose_name': 'автомобиль',
                'verbose_name_plural': 'автомобили',
            },
        ),
        migrations.CreateModel(
            name='Spare',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='название')),
                ('manufacturer', models.CharField(max_length=100, verbose_name='производитель')),
                ('partnumber', models.CharField(max_length=100, verbose_name='артикул')),
                ('autodoc_URL', models.URLField(blank=True, verbose_name='ссылка на Autodoc')),
                ('exist_URL', models.URLField(blank=True, verbose_name='ссылка на Exist')),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='autos.auto', verbose_name='автомобиль')),
            ],
            options={
                'verbose_name': 'запчасть',
                'verbose_name_plural': 'запчасти',
            },
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_create', models.DateTimeField(auto_now_add=True, verbose_name='создано')),
                ('price', models.SmallIntegerField(verbose_name='цена')),
                ('delivery_time', models.SmallIntegerField(verbose_name='срок доставки')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='пользователь')),
                ('spare', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='autos.spare', verbose_name='запчасть')),
            ],
            options={
                'verbose_name': 'запрос',
                'verbose_name_plural': 'запросы',
            },
        ),
    ]
