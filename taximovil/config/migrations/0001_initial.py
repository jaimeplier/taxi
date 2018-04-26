# Generated by Django 2.0.3 on 2018-04-25 16:14

from django.conf import settings
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=128, unique=True)),
                ('password', models.CharField(max_length=512)),
                ('nombre', models.CharField(max_length=64)),
                ('a_paterno', models.CharField(max_length=64)),
                ('a_materno', models.CharField(blank=True, max_length=64, null=True)),
                ('telefono', models.CharField(max_length=20, unique=True)),
                ('estatus', models.BooleanField(default=True)),
                ('fecha_registro', models.DateField(auto_now_add=True)),
            ],
            options={
                'db_table': 'usuario',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Base',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identificador', models.CharField(max_length=15)),
                ('numero_espacio', models.IntegerField()),
                ('telefono', models.CharField(max_length=25, unique=True)),
            ],
            options={
                'db_table': 'base',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='BitacoraEstatusServicio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(auto_now_add=True)),
            ],
            options={
                'db_table': 'bitacora_estatus_servicio',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Ciudad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=45)),
                ('estatus', models.BooleanField(default=True)),
                ('factor_tiempo', models.FloatField()),
                ('centro', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('radio', models.IntegerField()),
            ],
            options={
                'db_table': 'ciudad',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Codigo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=5)),
                ('telefono', models.CharField(max_length=10)),
                ('fecha', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
                'db_table': 'codigo',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Comisiones',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('tipo', models.IntegerField()),
                ('factor', models.FloatField()),
            ],
            options={
                'db_table': 'comisiones',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Cuentas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cie', models.CharField(max_length=7)),
                ('clabe', models.CharField(max_length=18)),
            ],
            options={
                'db_table': 'cuentas',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Direccion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('colonia', models.CharField(max_length=100)),
                ('calle', models.CharField(max_length=100)),
                ('numero_interior', models.CharField(blank=True, max_length=20, null=True)),
                ('numero_exterior', models.CharField(max_length=50)),
                ('cp', models.CharField(max_length=10)),
                ('latlgn', django.contrib.gis.db.models.fields.PointField(srid=4326)),
            ],
            options={
                'db_table': 'direccion',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Documentos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('licencia_condicir', models.CharField(max_length=200)),
                ('licencia_auto', models.CharField(max_length=200)),
                ('seguro_auto', models.CharField(max_length=200)),
                ('tarjeta_circulacion', models.CharField(max_length=200)),
                ('placas', models.CharField(max_length=200, unique=True)),
                ('verificacion', models.CharField(max_length=200)),
                ('penales', models.CharField(max_length=200)),
                ('toxicologico', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'documentos',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('direccion', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'empresa',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Estado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=45)),
                ('hora_diferencia', models.IntegerField()),
            ],
            options={
                'db_table': 'estado',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='EstatusPago',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'estatus_pago',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='EstatusServicio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'estatus_servicio',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Horario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('diasemana', models.IntegerField()),
                ('horainicio', models.TimeField()),
                ('horafin', models.TimeField()),
            ],
            options={
                'db_table': 'horario',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Marca',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'marca',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Modelo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=45)),
                ('marca', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='config.Marca')),
            ],
            options={
                'db_table': 'modelo',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Municipio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=45)),
                ('estado', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='config.Estado')),
            ],
            options={
                'db_table': 'municipio',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Pais',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'pais',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Puerta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=45)),
                ('comentarios', models.CharField(max_length=150)),
            ],
            options={
                'db_table': 'puerta',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Rol',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=64)),
            ],
            options={
                'db_table': 'rol',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='RolHasPermissions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('permission', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='auth.Permission')),
                ('rol', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='config.Rol')),
            ],
            options={
                'db_table': 'rol_has_permissions',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Servicio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hora_registro', models.DateTimeField(auto_now_add=True)),
                ('ubicacion_usuario', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('destino', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('direccion_servicio', models.CharField(max_length=400)),
                ('direccion_destino', models.CharField(max_length=400)),
                ('tiempo_aproximado', models.CharField(max_length=20)),
                ('ref_lugar', models.CharField(max_length=200)),
                ('ref_persona', models.CharField(max_length=200)),
                ('distancia', models.CharField(max_length=20)),
                ('costo', models.CharField(max_length=20)),
                ('estatus', models.IntegerField()),
            ],
            options={
                'db_table': 'servicio',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ServicioChofer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estatus', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'servicio_asociado',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Sitio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('num_espacio', models.IntegerField()),
                ('pv', models.CharField(max_length=45)),
                ('estatus_sesion', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'sitio',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Sucursal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clave', models.CharField(max_length=50)),
                ('nombre', models.CharField(max_length=200)),
                ('coordenadas', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('direccion', models.CharField(max_length=200)),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='config.Empresa')),
            ],
            options={
                'db_table': 'sucursal',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Tarifa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tarifa_base', models.FloatField()),
                ('costo_minimo', models.FloatField()),
                ('costo_km', models.FloatField()),
                ('distancia_max', models.FloatField()),
                ('incremento_distancia', models.FloatField()),
                ('costo_minuto', models.FloatField()),
                ('comision', models.FloatField()),
                ('base', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='config.Base')),
                ('ciudad', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='config.Ciudad')),
                ('comisiones', models.ManyToManyField(to='config.Comisiones')),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='config.Empresa')),
            ],
            options={
                'db_table': 'tarifa',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='TipoMateria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'tipo_materia',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='TipoPago',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=45)),
                ('precio', models.FloatField()),
                ('plan', models.CharField(blank=True, max_length=20, null=True)),
            ],
            options={
                'db_table': 'tipo_pago',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='TipoServicio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'tipo_servicio',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='TipoVehiculo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=45, unique=True)),
                ('caracteristicas', models.CharField(max_length=200)),
                ('num_max_pasajeros', models.IntegerField()),
                ('num_maletas', models.IntegerField()),
            ],
            options={
                'db_table': 'tipo_vehiculo',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Vehiculo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('placa', models.CharField(max_length=45, unique=True)),
                ('anio', models.IntegerField()),
                ('cromatica', models.CharField(max_length=45)),
                ('estatus', models.BooleanField(default=True)),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
                ('economico', models.CharField(max_length=15, unique=True)),
                ('activo', models.BooleanField(default=True)),
                ('ciudad', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='config.Ciudad')),
                ('modelo', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='config.Modelo')),
            ],
            options={
                'db_table': 'vehiculo',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Zona',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=45)),
                ('centro', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('radio', models.FloatField()),
            ],
            options={
                'db_table': 'zona',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Chofer',
            fields=[
                ('usuario_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('foto', models.FileField(db_column='foto', null=True, upload_to='asociados/')),
                ('numero_licencia', models.CharField(max_length=64)),
                ('turno', models.CharField(max_length=3)),
                ('saldo', models.FloatField()),
            ],
            options={
                'db_table': 'chofer',
                'managed': True,
            },
            bases=('config.usuario',),
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('usuario_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('rfc', models.CharField(max_length=45)),
                ('cp', models.IntegerField()),
                ('lada', models.IntegerField()),
            ],
            options={
                'db_table': 'cliente',
                'managed': True,
            },
            bases=('config.usuario',),
        ),
        migrations.CreateModel(
            name='Personal',
            fields=[
                ('usuario_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'persona',
                'managed': True,
            },
            bases=('config.usuario',),
        ),
        migrations.CreateModel(
            name='Propietario',
            fields=[
                ('usuario_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('tipo_persona', models.CharField(max_length=45)),
                ('razon_social', models.CharField(max_length=45)),
                ('direccion_fiscal', models.CharField(max_length=45)),
                ('nombre_banco', models.CharField(max_length=45)),
                ('titular_cuenta', models.CharField(max_length=45)),
                ('clabe', models.CharField(max_length=45)),
                ('numero_cuenta', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'propietario',
                'managed': True,
            },
            bases=('config.usuario',),
        ),
        migrations.AddField(
            model_name='tarifa',
            name='pago',
            field=models.ManyToManyField(to='config.TipoPago'),
        ),
        migrations.AddField(
            model_name='tarifa',
            name='pais',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='config.Pais'),
        ),
        migrations.AddField(
            model_name='tarifa',
            name='sitio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='config.Sitio'),
        ),
        migrations.AddField(
            model_name='tarifa',
            name='sucursal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='config.Sucursal'),
        ),
        migrations.AddField(
            model_name='tarifa',
            name='tipo_servicio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='config.TipoServicio'),
        ),
        migrations.AddField(
            model_name='tarifa',
            name='tipo_vehiculo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='config.TipoVehiculo'),
        ),
        migrations.AddField(
            model_name='tarifa',
            name='zona_destino',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='zona_destino', to='config.Zona'),
        ),
        migrations.AddField(
            model_name='tarifa',
            name='zona_origen',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='zona_origen', to='config.Zona'),
        ),
        migrations.AddField(
            model_name='sucursal',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='servicio',
            name='forma_pago',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='config.TipoPago'),
        ),
        migrations.AddField(
            model_name='servicio',
            name='sitio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='config.Sitio'),
        ),
        migrations.AddField(
            model_name='servicio',
            name='tarifa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='config.Tarifa'),
        ),
        migrations.AddField(
            model_name='servicio',
            name='tipo_servicio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='config.TipoServicio'),
        ),
        migrations.AddField(
            model_name='servicio',
            name='vehiculo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='config.Vehiculo'),
        ),
        migrations.AddField(
            model_name='rol',
            name='permisos',
            field=models.ManyToManyField(through='config.RolHasPermissions', to='auth.Permission'),
        ),
        migrations.AddField(
            model_name='horario',
            name='tarifa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='config.Tarifa'),
        ),
        migrations.AddField(
            model_name='direccion',
            name='municipio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='config.Municipio'),
        ),
        migrations.AddField(
            model_name='ciudad',
            name='pais',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='config.Pais'),
        ),
        migrations.AddField(
            model_name='bitacoraestatusservicio',
            name='estatus',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='config.EstatusServicio'),
        ),
        migrations.AddField(
            model_name='base',
            name='direccion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='config.Direccion'),
        ),
        migrations.AddField(
            model_name='base',
            name='sitio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='config.Sitio'),
        ),
        migrations.AddField(
            model_name='usuario',
            name='rol',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='config.Rol'),
        ),
        migrations.AddField(
            model_name='vehiculo',
            name='propietario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='config.Propietario'),
        ),
        migrations.AddField(
            model_name='serviciochofer',
            name='chofer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='config.Chofer'),
        ),
        migrations.AddField(
            model_name='servicio',
            name='cliente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='config.Cliente'),
        ),
        migrations.AddField(
            model_name='documentos',
            name='chofer',
            field=models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='config.Chofer'),
        ),
        migrations.AddField(
            model_name='chofer',
            name='direccion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='config.Direccion'),
        ),
    ]