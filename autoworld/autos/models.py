from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Auto(models.Model):
    brand = models.CharField(max_length=100, verbose_name='марка')
    model = models.CharField(max_length=100, verbose_name='модель')
    vin = models.CharField(max_length=17, verbose_name='VIN', unique=True)
    odo = models.PositiveIntegerField(verbose_name='пробег')
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='владелец')

    def __str__(self):
        return f'{self.brand} {self.model}'

    class Meta:
        verbose_name = 'автомобиль'
        verbose_name_plural = 'автомобили'
        constraints = [
            models.CheckConstraint(
                check=models.Q(vin__iregex=r'[a-zA-Z0-9]{17}'),
                name='длина VIN-номера 17 символов',
                violation_error_message='длина VIN-номера должна быть 17 символов')
        ]


class Request(models.Model):
    EXIST = 'EX'
    AUTODOC = 'AD'
    SITE_CHOICES = [
        (EXIST, 'Exist'),
        (AUTODOC, 'Autodoc'),
    ]

    spare = models.ForeignKey('Spare', on_delete=models.CASCADE, verbose_name='запчасть', related_name='requests')
    site = models.CharField(max_length=2, choices=SITE_CHOICES, verbose_name='сайт')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='создано')
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='пользователь')
    price = models.SmallIntegerField(verbose_name='цена')
    delivery_time = models.SmallIntegerField(verbose_name='срок доставки')
    difference = models.SmallIntegerField(default=0, verbose_name='отличие от предыдущей цены')

    def __str__(self):
        return f'Запрос № {self.pk}'

    class Meta:
        verbose_name = 'запрос'
        verbose_name_plural = 'запросы'
        ordering = ['-time_create']


class Spare(models.Model):
    name = models.CharField(max_length=100, verbose_name='название')
    car = models.ForeignKey('Auto', on_delete=models.DO_NOTHING, verbose_name='автомобиль')
    manufacturer = models.CharField(max_length=100, verbose_name='производитель')
    partnumber = models.CharField(max_length=100, verbose_name='артикул', unique=True)
    price_graph = models.ImageField(null=True, blank=True, upload_to='graphs', verbose_name='график изменения цен')
    autodoc_URL = models.URLField(blank=True, verbose_name='ссылка на Autodoc', unique=True, null=True)
    exist_URL = models.URLField(blank=True, verbose_name='ссылка на Exist', unique=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('spare', kwargs={'spare_id': self.partnumber})

    class Meta:
        verbose_name = 'запчасть'
        verbose_name_plural = 'запчасти'
