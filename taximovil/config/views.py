from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse
from django.views.generic import CreateView, UpdateView
from django_datatables_view.base_datatable_view import BaseDatatableView

from config.forms import EmpresaForm, UsuarioForm, ChoferForm, SitioForm, ZonaForm, BaseForm, DireccionForm, PaisForm, \
    CiudadForm, SucursalForm, TipoPagoForm, TipoVehiculoForm, ClienteForm
from config.models import Empresa, Usuario, Rol, Chofer, Sitio, Zona, Base, Pais, Ciudad, Sucursal, TipoPago, \
    TipoVehiculo, Direccion, Cliente
from django.contrib.gis.geos import Point


def index(request):
    template_name = 'tablas.html'
    return render(request, template_name)


class EmpresaCrear(CreateView):
    model = Empresa
    form_class = EmpresaForm
    template_name = 'form_1col.html'

    def get_success_url(self):
        return reverse('config:list_empresa')

def empresaListar(request):
    template_name = 'config/tab_empresa.html'
    return render(request, template_name)

class EmpresaListarAjaxListView(BaseDatatableView):
    redirect_field_name = 'next'
    model = Empresa
    columns = ['nombre', 'direccion', 'editar', 'eliminar']
    order_columns = ['nombre']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('config:edit_empresa',
                                                             kwargs={
                                                                 'pk': row.pk}) + '"><i class="material-icons">edit</i></a>'
        elif column == 'eliminar':
            return '<a class=" modal-trigger" href ="#" onclick="actualiza(' + str(
                row.pk) + ')"><i class="material-icons">delete_forever</i></a>'

        return super(EmpresaListarAjaxListView, self).render_column(row, column)

    def get_initial_queryset(self):
        return Empresa.objects.all()


class EmpresaActualizar(UpdateView):
    redirect_field_name = 'next'
    model = Empresa
    template_name = 'form_1col.html'
    form_class = EmpresaForm

    def get_success_url(self):
        return reverse('config:list_empresa')

def empresa_eliminar(request, pk):
    e = get_object_or_404(Empresa, pk=pk)
    e.delete()
    return JsonResponse({'result': 1})

class UsuarioCrear(CreateView):
    model = Usuario
    form_class = UsuarioForm
    template_name = 'form_1col.html'

    def form_valid(self, form):
        form.instance.set_password(form.cleaned_data['password'])
        form.instance.rol = Rol(pk=2)
        return super(UsuarioCrear,self).form_valid(form)

    def get_success_url(self):
        return reverse('config:list_usuario')

def usuarioListar(request):
    template_name = 'config/tab_usuario.html'
    return render(request, template_name)

class UsuarioListarAjaxListView(BaseDatatableView):
    redirect_field_name = 'next'
    model = Usuario
    columns = ['nombre', 'email', 'telefono','estatus','editar', 'eliminar']
    order_columns = ['nombre']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('config:edit_usuario',
                                                             kwargs={
                                                                 'pk': row.pk}) + '"><i class="material-icons">edit</i></a>'
        elif column == 'nombre':
            return row.get_full_name()
        elif column == 'eliminar':
            return '<a class=" modal-trigger" href ="#" onclick="actualiza(' + str(
                row.pk) + ')"><i class="material-icons">delete_forever</i></a>'

        return super(UsuarioListarAjaxListView, self).render_column(row, column)

    def get_initial_queryset(self):
        return Usuario.objects.filter(estatus=True, rol=2)

class UsuarioActualizar(UpdateView):
    redirect_field_name = 'next'
    model = Usuario
    template_name = 'form_1col.html'
    form_class = UsuarioForm

    def get_success_url(self):
        return reverse('config:list_usuario')

def usuario_eliminar(request, pk):
    u = get_object_or_404(Usuario, pk=pk)
    u.estatus = False
    u.save()
    return JsonResponse({'result': 1})


class ChoferCrear(CreateView):
    model = Chofer
    form_class = ChoferForm
    segundo_form = DireccionForm
    template_name = 'formMap.html'

    def get_context_data(self, **kwargs):
        context = super(ChoferCrear,self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        if 'formDireccion' not in context:
            context['form2'] = self.segundo_form(self.request.GET)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        form2 = self.segundo_form(request.POST)
        lon = self.request.POST.get('lgn')
        lat = self.request.POST.get('lat')
        if form.is_valid() and form2.is_valid():

            pnt = Point(float(lon), float(lat))
            form2.instance.latlgn = pnt

            #form.instance.set_password(form.cleaned_data['password'])
            form.instance.rol = Rol(pk=3)

            base = form.save(commit=False)
            base.direccion = form2.save()
            base.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form, form2=form2))

    # def form_valid(self, form):
    #     form.instance.set_password(form.cleaned_data['password'])
    #     form.instance.rol = Rol(pk=3)
    #     return super(ChoferCrear, self).form_valid(form)

    def get_success_url(self):
        return reverse('config:list_chofer')

def choferListar(request):
    template_name = 'config/tab_chofer.html'
    return render(request, template_name)

class ChoferListarAjaxListView(BaseDatatableView):
    redirect_field_name = 'next'
    model = Chofer
    columns = ['nombre', 'email', 'telefono', 'estatus', 'editar', 'eliminar']
    order_columns = ['nombre', 'email', 'telefono', 'estatus']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('config:edit_chofer',
                                                             kwargs={
                                                                 'pk': row.pk}) + '"><i class="material-icons">edit</i></a>'
        elif column == 'nombre':
            return row.get_full_name()
        elif column == 'foto':
            return '<img src="' + row.foto.url + '" class="responsive-img dimension_fija" width="50" />'
        elif column == 'eliminar':
            return '<a class=" modal-trigger" href ="#" onclick="actualiza(' + str(
                row.pk) + ')"><i class="material-icons">delete_forever</i></a>'

        return super(ChoferListarAjaxListView, self).render_column(row, column)

    def get_initial_queryset(self):
        return Chofer.objects.filter(estatus=True)


class ChoferActualizar(UpdateView):
    model = Chofer
    segundoModelo = Direccion
    template_name = 'formBase.html'
    form_class = ChoferForm
    segundo_form = DireccionForm

    def get_context_data(self, **kwargs):
        context = super(ChoferActualizar,self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        chofer = self.model.objects.get(id=pk)
        direccion = self.segundoModelo.objects.get(id= chofer.direccion_id)

        if 'form' not in context:
            context['form'] = self.form_class()
        if 'form2' not in context:
            self.segundo_form
            context['form2'] = self.segundo_form(instance=direccion)
            context['latitud'] = direccion.latitud
            context['longitud'] = direccion.longitud
        context['id'] = pk
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_chofer = kwargs['pk']
        chofer = self.model.objects.get(id=id_chofer)
        direccion = self.segundoModelo.objects.get(id=chofer.direccion_id)
        form = self.form_class(request.POST, instance=chofer)
        form2 = self.segundo_form(request.POST, instance=direccion)
        lon = self.request.POST.get('lgn')
        lat = self.request.POST.get('lat')
        if form.is_valid() and form2.is_valid():

            pnt = Point(float(lon), float(lat))
            form2.instance.latlgn = pnt

            chofer = form.save(commit=False)
            chofer.direccion = form2.save()
            chofer.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form, form2=form2))
        
    def get_success_url(self):
        return reverse('config:list_chofer')


def chofer_eliminar(request, pk):
    u = get_object_or_404(Chofer, pk=pk)
    u.estatus = False
    u.save()
    return JsonResponse({'result': 1})


class SitioCrear(CreateView):
    model = Sitio
    form_class = SitioForm
    template_name = 'form_1col.html'

    def get_success_url(self):
        return reverse('config:list_sitio')

def sitioListar(request):
    template_name = 'config/tab_sitio.html'
    return render(request, template_name)

class SitioListarAjaxListView(BaseDatatableView):
    redirect_field_name = 'next'
    model = Sitio
    columns = ['nombre','num_espacio','pv', 'editar', 'eliminar']
    order_columns = ['nombre','num_espacio','pv']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('config:edit_sitio',
                                                             kwargs={
                                                                 'pk': row.pk}) + '"><i class="material-icons">edit</i></a>'
        elif column == 'eliminar':
            return '<a class=" modal-trigger" href ="#" onclick="actualiza(' + str(
                row.pk) + ')"><i class="material-icons">delete_forever</i></a>'

        return super(SitioListarAjaxListView, self).render_column(row, column)

    def get_initial_queryset(self):
        return Sitio.objects.all()


class SitioActualizar(UpdateView):
    redirect_field_name = 'next'
    model = Sitio
    template_name = 'form_1col.html'
    form_class = SitioForm

    def get_success_url(self):
        return reverse('config:list_sitio')

def sitio_eliminar(request, pk):
    e = get_object_or_404(Sitio, pk=pk)
    e.delete()
    return JsonResponse({'result': 1})


class ZonaCrear(CreateView):
    model = Zona
    form_class = ZonaForm
    template_name = 'formMap.html'

    def get_success_url(self):
        return reverse('config:list_zona')

    def form_valid(self, form):
        lon = self.request.POST.get('lgn')
        lat = self.request.POST.get('lat')
        pnt = Point(float(lon), float(lat))
        form.instance.centro = pnt
        return super(ZonaCrear, self).form_valid(form)

def zonaListar(request):
    template_name = 'config/tab_zona.html'
    return render(request, template_name)

class ZonaListarAjaxListView(BaseDatatableView):
    redirect_field_name = 'next'
    model = Zona
    columns = ['nombre', 'radio', 'editar', 'eliminar']
    order_columns = ['nombre']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('config:edit_zona',
                                                             kwargs={
                                                                 'pk': row.pk}) + '"><i class="material-icons">edit</i></a>'
        elif column == 'eliminar':
            return '<a class=" modal-trigger" href ="#" onclick="actualiza(' + str(
                row.pk) + ')"><i class="material-icons">delete_forever</i></a>'

        return super(ZonaListarAjaxListView, self).render_column(row, column)

    def get_initial_queryset(self):
        return Zona.objects.all()


class ZonaActualizar(UpdateView):
    redirect_field_name = 'next'
    model = Zona
    template_name = 'formMap.html'
    form_class = ZonaForm

    def form_valid(self, form):
        lon = self.request.POST.get('lgn')
        lat = self.request.POST.get('lat')
        pnt = Point(float(lon), float(lat))
        form.instance.centro = pnt
        return super(ZonaActualizar, self).form_valid(form)

    def get_success_url(self):
        return reverse('config:list_zona')

def zona_eliminar(request, pk):
    z = get_object_or_404(Zona, pk=pk)
    z.delete()
    return JsonResponse({'result': 1})

class BaseCrear(CreateView):
    model = Base
    form_class = BaseForm
    segundo_form = DireccionForm
    template_name = 'formMap.html'

    def get_context_data(self, **kwargs):
        context = super(BaseCrear, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        if 'formDireccion' not in context:
            context['form2'] = self.segundo_form(self.request.GET)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        form2 = self.segundo_form(request.POST)
        lon = self.request.POST.get('lgn')
        lat = self.request.POST.get('lat')
        if form.is_valid() and form2.is_valid() and lat:

            pnt = Point(float(lon), float(lat))
            form2.instance.latlgn = pnt

            base = form.save(commit=False)
            base.direccion = form2.save()
            base.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form, form2=form2))

    def get_success_url(self):
        return reverse('config:list_base')

def baseListar(request):
    template_name = 'config/tab_base.html'
    return render(request, template_name)

class BaseListarAjaxListView(BaseDatatableView):
    redirect_field_name = 'next'
    model = Base
    columns = ['identificador', 'numero_espacio','telefono', 'direccion', 'sitio', 'editar', 'eliminar']
    order_columns = ['identificador']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('config:edit_base',
                                                             kwargs={
                                                                 'pk': row.pk}) + '"><i class="material-icons">edit</i></a>'
        elif column == 'eliminar':
            return '<a class=" modal-trigger" href ="#" onclick="actualiza(' + str(
                row.pk) + ')"><i class="material-icons">delete_forever</i></a>'
        elif column == 'direccion':
            return row.direccion.get_address()
        elif column == 'sitio':
            return  row.sitio.__str__()

        return super(BaseListarAjaxListView, self).render_column(row, column)

    def get_initial_queryset(self):
        return Base.objects.all()

class BaseActualizar(UpdateView):
    model = Base
    segundoModelo = Direccion
    template_name = 'formBase.html'
    form_class = BaseForm
    segundo_form = DireccionForm
    id_base =  0
    def get_context_data(self, **kwargs):
        context = super(BaseActualizar,self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        base = self.model.objects.get(id=pk)
        direccion = self.segundoModelo.objects.get(id= base.direccion_id)
        print(direccion.latitud)
        print(direccion.longitud)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'form2' not in context:
            self.segundo_form
            context['form2'] = self.segundo_form(instance=direccion)

            context['latitud'] = direccion.latitud
            context['longitud'] = direccion.longitud
            print(context)
            #lon= self.request.POST.get('lgn')
            #lat = self.request.POST.get('lat')
            #pnt = Point(float(lon), float(lat))
            #self.segundo_form.instance.latlgn = pnt

        context['id'] = pk
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_base = kwargs['pk']
        base = self.model.objects.get(id=id_base)
        direccion = self.segundoModelo.objects.get(id=base.direccion_id)
        # pk = self.kwargs.get('pk', 0)
        # base = self.model.objects.get(id=pk)
        # direccion = self.segundoModelo.objects.get(id=base.direccion_id)
        form = self.form_class(request.POST, instance=base)
        form2 = self.segundo_form(request.POST, instance=direccion)
        lon = self.request.POST.get('lgn')
        lat = self.request.POST.get('lat')
        if form.is_valid() and form2.is_valid():

            pnt = Point(float(lon), float(lat))
            form2.instance.latlgn = pnt

            base = form.save(commit=False)
            base.direccion = form2.save()
            base.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form, form2=form2))

    def form_valid(self, form):
        lon = self.request.POST.get('lgn')
        lat = self.request.POST.get('lat')
        pnt = Point(float(lon), float(lat))
        form.instance.latlgn = pnt
        return super(BaseActualizar, self).form_valid(form)

    def get_success_url(self):
        return reverse('config:list_base')

def base_eliminar(request, pk):
    b = get_object_or_404(Base, pk=pk)
    id_direccion = b.direccion.id
    d = get_object_or_404(Direccion, pk= id_direccion)
    d.delete()
    b.delete()
    return JsonResponse({'result': 1})

class PaisCrear(CreateView):
    model = Pais
    form_class = PaisForm
    template_name = 'form_1col.html'

    def get_success_url(self):
        return reverse('config:list_pais')

def paisListar(request):
    template_name = 'config/tab_pais.html'
    return render(request, template_name)

class PaisListarAjaxListView(BaseDatatableView):
    redirect_field_name = 'next'
    model = Pais
    columns = ['nombre', 'editar', 'eliminar']
    order_columns = ['nombre']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('config:edit_pais',
                                                             kwargs={
                                                                 'pk': row.pk}) + '"><i class="material-icons">edit</i></a>'
        elif column == 'eliminar':
            return '<a class="modal-trigger" href ="#" onclick="actualiza(' + str(
                row.pk) + ')"><i class="material-icons">delete_forever</i></a>'

        return super(PaisListarAjaxListView, self).render_column(row, column)

    def get_initial_queryset(self):
        return Pais.objects.all()


class PaisActualizar(UpdateView):
    redirect_field_name = 'next'
    model = Pais
    template_name = 'form_1col.html'
    form_class = PaisForm

    def get_success_url(self):
        return reverse('config:list_pais')

def pais_eliminar(request, pk):
    p = get_object_or_404(Pais, pk=pk)
    p.delete()
    return JsonResponse({'result': 1})


class CiudadCrear(CreateView):
    model = Ciudad
    form_class = CiudadForm
    template_name = 'formMap.html'

    def form_valid(self, form):
        lon = self.request.POST.get('lgn')
        lat = self.request.POST.get('lat')
        pnt = Point(float(lon), float(lat))
        form.instance.centro = pnt
        return super(CiudadCrear, self).form_valid(form)

    def get_success_url(self):
        return reverse('config:list_ciudad')

def ciudadListar(request):
    template_name = 'config/tab_ciudad.html'
    return render(request, template_name)

class CiudadListarAjaxListView(BaseDatatableView):
    redirect_field_name = 'next'
    model = Ciudad
    columns = ['nombre','factor_tiempo', 'radio', 'pais', 'editar', 'eliminar']
    order_columns = ['nombre']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('config:edit_ciudad',
                                                             kwargs={
                                                                 'pk': row.pk}) + '"><i class="material-icons">edit</i></a>'
        elif column == 'eliminar':
            return '<a class="modal-trigger" href ="#" onclick="actualiza(' + str(
                row.pk) + ')"><i class="material-icons">delete_forever</i></a>'
        elif column == 'pais':
            return row.pais.__str__()


        return super(CiudadListarAjaxListView, self).render_column(row, column)

    def get_initial_queryset(self):
        return Ciudad.objects.all()


class CiudadActualizar(UpdateView):
    redirect_field_name = 'next'
    model = Ciudad
    template_name = 'formMap.html'
    form_class = CiudadForm

    def form_valid(self, form):
        lon = self.request.POST.get('lgn')
        lat = self.request.POST.get('lat')
        pnt = Point(float(lon), float(lat))
        form.instance.centro = pnt
        return super(CiudadActualizar, self).form_valid(form)

    def get_success_url(self):
        return reverse('config:list_ciudad')

def ciudad_eliminar(request, pk):
    c = get_object_or_404(Ciudad, pk=pk)
    c.delete()
    return JsonResponse({'result': 1})

class SucursalCrear(CreateView):
    model = Sucursal
    form_class = SucursalForm
    template_name = 'formMap.html'

    def form_valid(self, form):
        lon = self.request.POST.get('lgn')
        lat = self.request.POST.get('lat')
        pnt = Point(float(lon), float(lat))
        form.instance.coordenadas = pnt
        return super(SucursalCrear, self).form_valid(form)

    def get_success_url(self):
        return reverse('config:list_sucursal')

def sucursalListar(request):
    template_name = 'config/tab_sucursal.html'
    return render(request, template_name)

class SucursalListarAjaxListView(BaseDatatableView):
    redirect_field_name = 'next'
    model = Sucursal
    columns = ['nombre','clave', 'direccion', 'usuario','empresa', 'editar', 'eliminar']
    order_columns = ['nombre','clave', 'direccion', 'usuario','empresa']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('config:edit_sucursal',
                                                             kwargs={
                                                                 'pk': row.pk}) + '"><i class="material-icons">edit</i></a>'
        elif column == 'eliminar':
            return '<a class="modal-trigger" href ="#" onclick="actualiza(' + str(
                row.pk) + ')"><i class="material-icons">delete_forever</i></a>'
        elif column == 'empresa':
            return row.empresa.__str__()
        elif column == 'usuario':
            return row.usuario.get_full_name()


        return super(SucursalListarAjaxListView, self).render_column(row, column)

    def get_initial_queryset(self):
        return Sucursal.objects.all()


class SucursalActualizar(UpdateView):
    redirect_field_name = 'next'
    model = Sucursal
    template_name = 'formMap.html'
    form_class = SucursalForm

    def form_valid(self, form):
        lon = self.request.POST.get('lgn')
        lat = self.request.POST.get('lat')
        pnt = Point(float(lon), float(lat))
        form.instance.coordenadas = pnt
        return super(SucursalActualizar, self).form_valid(form)

    def get_success_url(self):
        return reverse('config:list_sucursal')

def sucursal_eliminar(request, pk):
    s = get_object_or_404(Sucursal, pk=pk)
    s.delete()
    return JsonResponse({'result': 1})

class FormaPagoCrear(CreateView):
    model = TipoPago
    form_class = TipoPagoForm
    template_name = 'form_1col.html'

    def get_success_url(self):
        return reverse('config:list_forma_pago')

def formaPagoListar(request):
    template_name = 'config/tab_forma_pago.html'
    return render(request, template_name)

class FormaPagoListarAjaxListView(BaseDatatableView):
    redirect_field_name = 'next'
    model = TipoPago
    columns = ['nombre', 'precio','plan', 'editar', 'eliminar']
    order_columns = ['nombre', 'precio','plan']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('config:edit_forma_pago',
                                                             kwargs={
                                                                 'pk': row.pk}) + '"><i class="material-icons">edit</i></a>'
        elif column == 'eliminar':
            return '<a class=" modal-trigger" href ="#" onclick="actualiza(' + str(
                row.pk) + ')"><i class="material-icons">delete_forever</i></a>'

        return super(FormaPagoListarAjaxListView, self).render_column(row, column)

    def get_initial_queryset(self):
        return TipoPago.objects.all()


class FormaPagoActualizar(UpdateView):
    redirect_field_name = 'next'
    model = TipoPago
    template_name = 'form_1col.html'
    form_class = TipoPagoForm

    def get_success_url(self):
        return reverse('config:list_forma_pago')

def forma_pago_eliminar(request, pk):
    tp = get_object_or_404(TipoPago, pk=pk)
    tp.delete()
    return JsonResponse({'result': 1})

class TipoVehiculoCrear(CreateView):
    model = TipoVehiculo
    form_class = TipoVehiculoForm
    template_name = 'form_1col.html'

    def get_success_url(self):
        return reverse('config:list_tipo_vehiculo')

def tipoVehiculoListar(request):
    template_name = 'config/tab_tipo_vehiculo.html'
    return render(request, template_name)

class TipoVehiculoListarAjaxListView(BaseDatatableView):
    redirect_field_name = 'next'
    model = TipoVehiculo
    columns = ['nombre', 'num_max_pasajeros','num_maletas', 'editar', 'eliminar']
    order_columns = ['nombre', 'num_max_pasajeros','num_maletas']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('config:edit_tipo_vehiculo',
                                                             kwargs={
                                                                 'pk': row.pk}) + '"><i class="material-icons">edit</i></a>'
        elif column == 'eliminar':
            return '<a class=" modal-trigger" href ="#" onclick="actualiza(' + str(
                row.pk) + ')"><i class="material-icons">delete_forever</i></a>'

        return super(TipoVehiculoListarAjaxListView, self).render_column(row, column)

    def get_initial_queryset(self):
        return TipoVehiculo.objects.all()


class TipoVehiculoActualizar(UpdateView):
    redirect_field_name = 'next'
    model = TipoVehiculo
    template_name = 'form_1col.html'
    form_class = TipoVehiculoForm

    def get_success_url(self):
        return reverse('config:list_tipo_vehiculo')

def tipoVehiculoEliminar(request, pk):
    tv = get_object_or_404(TipoVehiculo, pk=pk)
    tv.delete()
    return JsonResponse({'result': 1})



class ClienteCrear(CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'form_1col.html'

    def form_valid(self, form):
        form.instance.set_password(form.cleaned_data['password'])
        form.instance.rol = Rol(pk=2)
        return super(ClienteCrear,self).form_valid(form)

    def get_success_url(self):
        return reverse('config:list_cliente')

def clienteListar(request):
    template_name = 'config/tab_cliente.html'
    return render(request, template_name)

class ClienteListarAjaxListView(BaseDatatableView):
    redirect_field_name = 'next'
    model = Cliente
    columns = ['nombre', 'email', 'telefono','rfc','estatus','editar', 'eliminar']
    order_columns = ['nombre', 'email', 'telefono','rfc','estatus']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('config:edit_cliente',
                                                             kwargs={
                                                                 'pk': row.pk}) + '"><i class="material-icons">edit</i></a>'
        elif column == 'nombre':
            return row.get_full_name()
        elif column == 'eliminar':
            return '<a class=" modal-trigger" href ="#" onclick="actualiza(' + str(
                row.pk) + ')"><i class="material-icons">delete_forever</i></a>'

        return super(ClienteListarAjaxListView, self).render_column(row, column)

    def get_initial_queryset(self):
        return Cliente.objects.filter(estatus=True, rol=2)

class ClienteActualizar(UpdateView):
    redirect_field_name = 'next'
    model = Cliente
    template_name = 'form_1col.html'
    form_class = ClienteForm

    def get_success_url(self):
        return reverse('config:list_cliente')

def cliente_eliminar(request, pk):
    u = get_object_or_404(Cliente, pk=pk)
    u.estatus = False
    u.save()
    return JsonResponse({'result': 1})
