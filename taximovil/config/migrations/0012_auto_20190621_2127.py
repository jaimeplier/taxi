# Generated by Django 2.0.3 on 2019-06-21 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0011_configusuariosciudad_configusuariossitio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='configusuariossitio',
            name='max_callcenter',
            field=models.PositiveIntegerField(default=15),
        ),
    ]