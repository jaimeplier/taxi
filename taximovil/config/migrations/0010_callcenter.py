# Generated by Django 2.0.3 on 2019-06-19 19:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0009_administradorsitio'),
    ]

    operations = [
        migrations.CreateModel(
            name='Callcenter',
            fields=[
                ('usuario_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('sitio', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='config.Sitio')),
            ],
            options={
                'db_table': 'callcenter',
                'managed': True,
            },
            bases=('config.usuario',),
        ),
    ]