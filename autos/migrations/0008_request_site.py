# Generated by Django 4.1.7 on 2023-04-10 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autos', '0007_request_difference'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='site',
            field=models.CharField(choices=[('EX', 'Exist'), ('AD', 'Autodoc')], default='AD', max_length=2, verbose_name='сайт'),
            preserve_default=False,
        ),
    ]