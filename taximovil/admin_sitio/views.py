from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import UpdateView, CreateView
from django_datatables_view.base_datatable_view import BaseDatatableView

from admin_sitio.forms import TarifaForm
from config.models import Tarifa, TipoPago, Ciudad, Pais, Empresa, Sucursal, Zona, Sitio, Base, TipoVehiculo, \
    TipoServicio


class TarifaCrear(PermissionRequiredMixin, CreateView):
    redirect_field_name = 'next'
    login_url = '/webapp/'
    permission_required = 'add_tarifa'
    model = Tarifa
    form_class = TarifaForm
    template_name = 'webapp/registro_tarifario.html'

    def get_context_data(self, **kwargs):
        context = super(TarifaCrear, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'tipoPago' not in context:
            context['tipoPago'] = TipoPago.objects.all()
        if 'titulo' not in context:
            context['titulo'] = 'Registro de tarifa'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Completa todos los campos para registrar una tarifa'
        return context

    def get_success_url(self):
        return reverse('webapp:list_tarifa')


class TarifaActualizar(PermissionRequiredMixin, UpdateView):
    redirect_field_name = 'next'
    login_url = '/webapp/'
    permission_required = 'change_tarifa'
    model = Tarifa
    template_name = 'webapp/registro_tarifario.html'
    form_class = TarifaForm

    def get_context_data(self, **kwargs):
        context = super(TarifaActualizar, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Modificación de tarifa'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Modifica los campos que requieras'
        return context

    def get_success_url(self):
        return reverse('webapp:list_tarifa')


def tarifa_crear(request):
    template_name = 'webapp/registro_tarifario.html'
    if request.method == 'POST':
        form = TarifaForm(request.POST)
        if form.is_valid():
            form.save()
            return reverse('webapp:list_tarifa')
        return render(request, template_name, {'form': form})
    else:
        form = TarifaForm()
        # elif request.method == 'GET':
        #     c = Ciudad.objects.all()
        #     s = Sucursal.objects.all()
        #     z = Zona.objects.all()
        #     p = Pais.objects.all()
        #     tv = TipoVehiculo.objects.all()
        #     e = Empresa.objects.all()
        #     ts = TipoServicio.objects.all()
        #     z = Zona.objects.all()
        #     b = Base.objects.all()
        #     si = Sitio.objects.all()
        #     fp = TipoPago.objects.all()
        #     context = dict(sucursales=s, ciudades=c, zonas=z, paises=p, vehiculos=tv, empresas=e, servicios=ts, bases=b,
        #                    sitios=si, pagos=fp)
        #     return render(request, template_name, context)
        # form = TarifaForm()
        return render(request, template_name, {'form': form})


def tarifa_add(request):
    response_data = {}
    try:
        pago = request.POST.get('pago')
        pago = pago.split(",")
        pago.pop(0)
        pagoList = []
        for i in pago:
            pagoList.append(int(i))
        tarifa = Tarifa(tarifa_base=request.POST.get('tarifaBase'), costo_minimo=request.POST.get('costoMinimo'),
                        costo_km=request.POST.get('costoKm'),
                        distancia_max=request.POST.get('distanciaMaxima'),
                        incremento_distancia=request.POST.get('incrementoDistancia'),
                        costo_minuto=request.POST.get('costoMinuto'),
                        ciudad=Ciudad.objects.get(pk=request.POST.get('ciudad')),
                        pais=Pais.objects.get(pk=request.POST.get('pais')),
                        empresa=Empresa.objects.get(pk=request.POST.get('empresa')),
                        sucursal=Sucursal.objects.get(pk=request.POST.get('sucursal')),
                        zona_origen=Zona.objects.get(pk=request.POST.get('zonaOrigen')),
                        zona_destino=Zona.objects.get(pk=request.POST.get('zonaDestino')),
                        sitio=Sitio.objects.get(pk=request.POST.get('sitio')),
                        base=Base.objects.get(pk=request.POST.get('base')),
                        tipo_vehiculo=TipoVehiculo.objects.get(pk=request.POST.get('tipoVehiculo')),
                        tipo_servicio=TipoServicio.objects.get(pk=request.POST.get('servicio')))
        tarifa.save()
        try:
            for i in range(len(pagoList)):
                pk_pago = TipoPago.objects.get(pk=pagoList[i])
                tarifa.pago.add(pk_pago)
        except ValueError:
            response_data['success'] = 'fail'
            return JsonResponse(response_data)
        response_data['success'] = 'success'
    except:
        response_data['error'] = 'error'
    return JsonResponse(response_data)


def tarifa_listar(request):
    template_name = 'webapp/tab_tarifa.html'
    return render(request, template_name)


class TarifaListarAjaxListView(BaseDatatableView):
    redirect_field_name = 'next'
    model = Tarifa
    columns = ['tarifa_base', 'ciudad', 'sitio', 'sucursal.empresa.nombre', 'sucursal.nombre', 'ciudad.pais.nombre',
               'horario', 'editar', 'eliminar']
    order_columns = ['tarifa_base', 'ciudad', 'sitio', 'sucursal.empresa.nombre', 'sucursal.nombre',
                     'ciudad.pais.nombre']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('webapp:edit_tarifa',
                                                   kwargs={
                                                       'pk': row.pk}) + '"><i class="material-icons">edit</i></a>'
        elif column == 'horario':
            return '<a class="" href ="' + reverse('webapp:horario_tarifa',
                                                   kwargs={
                                                       'pk': row.pk}) + '"><i class="material-icons">access_time</i></a>'
        elif column == 'ciudad':
            return row.ciudad.nombre
        elif column == 'sitio':
            return row.sitio.nombre
        elif column == 'eliminar':
            return '<a class=" modal-trigger" href ="#" onclick="actualiza(' + str(
                row.pk) + ')"><i class="material-icons">delete_forever</i></a>'

        return super(TarifaListarAjaxListView, self).render_column(row, column)

    def get_initial_queryset(self):
        return Tarifa.objects.all()
