# Generated by Django 2.0.3 on 2019-06-18 21:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0006_auto_20190614_1628'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdministradorCiudad',
            fields=[
                ('usuario_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('ciudad', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='config.Ciudad')),
            ],
            options={
                'managed': True,
                'db_table': 'admin_ciudad',
            },
            bases=('config.usuario',),
        ),
    ]