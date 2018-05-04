from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.views import password_reset_confirm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.urls import reverse
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.views.generic import CreateView, UpdateView
from django_datatables_view.base_datatable_view import BaseDatatableView

from webapp.forms import EmpresaForm, UsuarioForm, ChoferForm, SitioForm, ZonaForm, BaseForm, DireccionForm, PaisForm, \
    CiudadForm, SucursalForm, TipoPagoForm, TipoVehiculoForm, ClienteForm, TipoServicioForm, MarcaForm, ModeloForm, \
    PropietarioForm, VehiculoForm, TarifaForm, ComisionForm, PermisosForm
from config.models import Empresa, Usuario, Rol, Chofer, Sitio, Zona, Base, Pais, Ciudad, Sucursal, TipoPago, \
    TipoVehiculo, Direccion, Cliente, TipoServicio, Marca, Modelo, Propietario, Vehiculo, Tarifa, Comisiones, Horario, \
    ChoferHasVehiculo, RolHasPermissions
from django.contrib.gis.geos import Point

class RolCrear(CreateView):
    #redirect_field_name = 'next'
    #login_url = '/webapp/'
    #permission_required = 'add_empresa'
    #raise_exception = True
    model = Rol
    form_class = PermisosForm
    template_name = 'config/form_1col.html'

    def get_success_url(self):
        return reverse('webapp:list_empresa')

#@login_required(redirect_field_name='next', login_url='/webapp/')
def rol_listar(request):
    template_name = 'webapp/tab_rol.html'
    return render(request, template_name)


class RolListarAjaxListView(BaseDatatableView):
    model = Rol
    columns = ['nombre', 'editar', 'eliminar']
    order_columns = ['nombre']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('webapp:edit_rol',
                                                   kwargs={
                                                       'pk': row.pk}) + '"><i class="material-icons">edit</i></a>'
        elif column == 'eliminar':
            return '<a class=" modal-trigger" href ="#" onclick="actualiza(' + str(
                row.pk) + ')"><i class="material-icons">delete_forever</i></a>'

        return super(RolListarAjaxListView, self).render_column(row, column)

    def get_initial_queryset(self):
        return Rol.objects.all()


class RolActualizar(UpdateView):
    model = Rol
    template_name = 'config/form_1col.html'
    form_class = PermisosForm

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_rol = kwargs['pk']
        rol = self.model.objects.get(id=id_rol)
        form = self.form_class(request.POST, instance=rol)
        if form.is_valid():

            permisos = form.cleaned_data.get('permisos')
            RolHasPermissions.objects.filter(rol__pk=id_rol).delete()
            for permiso in permisos:

                tc = RolHasPermissions(rol=rol, permission=permiso)
                tc.save()

            rol = form.save(commit=False)
            rol.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse('webapp:list_rol')


def rol_eliminar(request, pk):
    e = get_object_or_404(Rol, pk=pk)
    id_rol = e.id
    RolHasPermissions.objects.filter(rol__pk=id_rol).delete()
    e.delete()
    return JsonResponse({'result': 1})

def login(request):
    error_message = ''
    if request.user.is_authenticated:
        return redirect(reverse('webapp:list_chofer'))
    if request.method == 'POST':
        correo = request.POST['correo']
        password = request.POST['password']
        user = authenticate(email=correo, password=password)
        if user is not None:
            if user.estatus:
                auth_login(request, user)
                if request.POST.get('next') is not None:
                    return redirect(request.POST.get('next'))
                return redirect(reverse('webapp:list_chofer'))
            else:
                error_message = "Usuario inactivo"
        else:
            error_message = "Usuario y/o contraseña incorrectos"
    context = {
        'error_message': error_message
    }
    if request.GET.get('next') is not None:
        context['next'] = request.GET.get('next')
    return render(request, 'webapp/login.html', context)

    # template_name = 'webapp/login.html'
    # return render(request, template_name)
def logout_view(request):
    logout(request)
    return redirect(reverse('webapp:login'))

class EmpresaCrear(PermissionRequiredMixin, CreateView):
    redirect_field_name = 'next'
    login_url = '/webapp/'
    permission_required = 'add_empresa'
    #raise_exception = True
    model = Empresa
    form_class = EmpresaForm
    template_name = 'config/form_1col.html'

    def get_success_url(self):
        return reverse('webapp:list_empresa')

@login_required(redirect_field_name='next', login_url='/webapp/')
def empresa_listar(request):
    template_name = 'webapp/tab_empresa.html'
    return render(request, template_name)


class EmpresaListarAjaxListView(BaseDatatableView, LoginRequiredMixin):
    redirect_field_name = 'next'
    login_url = '/webapp/'
    model = Empresa
    columns = ['nombre', 'direccion', 'editar', 'eliminar']
    order_columns = ['nombre']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('webapp:edit_empresa',
                                                   kwargs={
                                                       'pk': row.pk}) + '"><i class="material-icons">edit</i></a>'
        elif column == 'eliminar':
            return '<a class=" modal-trigger" href ="#" onclick="actualiza(' + str(
                row.pk) + ')"><i class="material-icons">delete_forever</i></a>'

        return super(EmpresaListarAjaxListView, self).render_column(row, column)

    def get_initial_queryset(self):
        return Empresa.objects.all()


class EmpresaActualizar(PermissionRequiredMixin, UpdateView):
    redirect_field_name = 'next'
    login_url = '/webapp/'
    permission_required = 'change_empresa'
    redirect_field_name = 'next'
    login_url = '/webapp/'
    redirect_field_name = 'next'
    model = Empresa
    template_name = 'config/form_1col.html'
    form_class = EmpresaForm

    def get_success_url(self):
        return reverse('webapp:list_empresa')


def empresa_eliminar(request, pk):
    e = get_object_or_404(Empresa, pk=pk)
    e.delete()
    return JsonResponse({'result': 1})


class UsuarioCrear(CreateView):
    model = Usuario
    form_class = UsuarioForm
    template_name = 'config/form_1col.html'

    def form_valid(self, form):
        form.instance.set_password(form.cleaned_data['password'])
        form.instance.rol = Rol(pk=2)
        return super(UsuarioCrear, self).form_valid(form)

    def get_success_url(self):
        return reverse('webapp:list_usuario')


def usuario_listar(request):
    template_name = 'webapp/tab_usuario.html'
    return render(request, template_name)


class UsuarioListarAjaxListView(BaseDatatableView):
    redirect_field_name = 'next'
    model = Usuario
    columns = ['nombre', 'email', 'telefono', 'estatus', 'editar', 'eliminar']
    order_columns = ['nombre']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('webapp:edit_usuario',
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
    template_name = 'config/form_1col.html'
    form_class = UsuarioForm

    def get_success_url(self):
        return reverse('webapp:list_usuario')


def usuario_eliminar(request, pk):
    u = get_object_or_404(Usuario, pk=pk)
    u.estatus = False
    u.save()
    return JsonResponse({'result': 1})


class ChoferCrear(PermissionRequiredMixin, CreateView):
    redirect_field_name = 'next'
    login_url = '/webapp/'
    permission_required = 'add_chofer'
    model = Chofer
    form_class = ChoferForm
    segundo_form = DireccionForm
    template_name = 'config/formMap.html'

    def get_context_data(self, **kwargs):
        context = super(ChoferCrear, self).get_context_data(**kwargs)
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

            # form.instance.set_password(form.cleaned_data['password'])
            print(form.cleaned_data('taxis'))
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
        return reverse('webapp:list_chofer')


def chofer_listar(request):
    template_name = 'webapp/tab_chofer.html'
    return render(request, template_name)


class ChoferListarAjaxListView(BaseDatatableView):
    redirect_field_name = 'next'
    model = Chofer
    columns = ['nombre', 'email', 'telefono', 'estatus','documentos', 'vehiculos', 'editar', 'eliminar']
    order_columns = ['nombre', 'email', 'telefono', 'estatus']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('webapp:edit_chofer',
                                                   kwargs={
                                                       'pk': row.pk}) + '"><i class="material-icons">edit</i></a>'
        elif column == 'documentos':
            return '<a class="" href ="' + reverse('webapp:edit_chofer',
                                                   kwargs={
                                                       'pk': row.pk}) + '"><i class="material-icons">assignment_ind</i></a>'
        elif column == 'vehiculos':
            return '<a class="" href ="' + reverse('webapp:vehiculo_chofer',
                                                   kwargs={
                                                       'pk': row.pk}) + '"><i class="material-icons">directions_car</i></a>'
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


class ChoferActualizar(PermissionRequiredMixin, UpdateView):
    redirect_field_name = 'next'
    login_url = '/webapp/'
    permission_required = 'change_chofer'

    model = Chofer
    segundoModelo = Direccion
    template_name = 'config/formBase.html'
    form_class = ChoferForm
    segundo_form = DireccionForm

    def get_context_data(self, **kwargs):
        context = super(ChoferActualizar, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        chofer = self.model.objects.get(id=pk)
        direccion = self.segundoModelo.objects.get(id=chofer.direccion_id)

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

            taxis = form.cleaned_data.get('taxis')
            ChoferHasVehiculo.objects.filter(chofer__pk=id_chofer).delete()
            for taxi in taxis:

                tc = ChoferHasVehiculo(chofer=chofer, vehiculo=taxi)
                tc.save()

            chofer = form.save(commit=False)
            chofer.direccion = form2.save()
            chofer.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form, form2=form2))

    def get_success_url(self):
        return reverse('webapp:list_chofer')


def chofer_eliminar(request, pk):
    u = get_object_or_404(Chofer, pk=pk)
    u.estatus = False
    u.save()
    return JsonResponse({'result': 1})


class SitioCrear(PermissionRequiredMixin, CreateView):
    redirect_field_name = 'next'
    login_url = '/webapp/'
    permission_required = 'add_sitio'
    model = Sitio
    form_class = SitioForm
    template_name = 'config/form_1col.html'

    def get_success_url(self):
        return reverse('webapp:list_sitio')


def sitio_listar(request):
    template_name = 'webapp/tab_sitio.html'
    return render(request, template_name)


class SitioListarAjaxListView(BaseDatatableView):
    redirect_field_name = 'next'
    model = Sitio
    columns = ['nombre', 'num_espacio', 'pv', 'editar', 'eliminar']
    order_columns = ['nombre', 'num_espacio', 'pv']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('webapp:edit_sitio',
                                                   kwargs={
                                                       'pk': row.pk}) + '"><i class="material-icons">edit</i></a>'
        elif column == 'eliminar':
            return '<a class=" modal-trigger" href ="#" onclick="actualiza(' + str(
                row.pk) + ')"><i class="material-icons">delete_forever</i></a>'

        return super(SitioListarAjaxListView, self).render_column(row, column)

    def get_initial_queryset(self):
        return Sitio.objects.all()


class SitioActualizar(PermissionRequiredMixin, UpdateView):
    redirect_field_name = 'next'
    login_url = '/webapp/'
    permission_required = 'change_sitio'
    redirect_field_name = 'next'
    model = Sitio
    template_name = 'config/form_1col.html'
    form_class = SitioForm

    def get_success_url(self):
        return reverse('webapp:list_sitio')


def sitio_eliminar(request, pk):
    e = get_object_or_404(Sitio, pk=pk)
    e.delete()
    return JsonResponse({'result': 1})


class ZonaCrear(PermissionRequiredMixin, CreateView):
    redirect_field_name = 'next'
    login_url = '/webapp/'
    permission_required = 'add_zona'
    model = Zona
    form_class = ZonaForm
    template_name = 'config/formMap.html'

    def get_success_url(self):
        return reverse('webapp:list_zona')

    def form_valid(self, form):
        lon = self.request.POST.get('lgn')
        lat = self.request.POST.get('lat')
        pnt = Point(float(lon), float(lat))
        form.instance.centro = pnt
        return super(ZonaCrear, self).form_valid(form)


def zona_listar(request):
    template_name = 'webapp/tab_zona.html'
    return render(request, template_name)


class ZonaListarAjaxListView(BaseDatatableView):
    redirect_field_name = 'next'
    model = Zona
    columns = ['nombre', 'radio', 'editar', 'eliminar']
    order_columns = ['nombre']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('webapp:edit_zona',
                                                   kwargs={
                                                       'pk': row.pk}) + '"><i class="material-icons">edit</i></a>'
        elif column == 'eliminar':
            return '<a class=" modal-trigger" href ="#" onclick="actualiza(' + str(
                row.pk) + ')"><i class="material-icons">delete_forever</i></a>'

        return super(ZonaListarAjaxListView, self).render_column(row, column)

    def get_initial_queryset(self):
        return Zona.objects.all()


class ZonaActualizar(PermissionRequiredMixin, UpdateView):
    redirect_field_name = 'next'
    login_url = '/webapp/'
    permission_required = 'change_zona'
    redirect_field_name = 'next'
    model = Zona
    template_name = 'config/formMap.html'
    form_class = ZonaForm

    def form_valid(self, form):
        lon = self.request.POST.get('lgn')
        lat = self.request.POST.get('lat')
        pnt = Point(float(lon), float(lat))
        form.instance.centro = pnt
        return super(ZonaActualizar, self).form_valid(form)

    def get_success_url(self):
        return reverse('webapp:list_zona')


def zona_eliminar(request, pk):
    z = get_object_or_404(Zona, pk=pk)
    z.delete()
    return JsonResponse({'result': 1})


class BaseCrear(PermissionRequiredMixin, CreateView):
    redirect_field_name = 'next'
    login_url = '/webapp/'
    permission_required = 'add_base'
    model = Base
    form_class = BaseForm
    segundo_form = DireccionForm
    template_name = 'config/formMap.html'

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
        return reverse('webapp:list_base')


def base_listar(request):
    template_name = 'webapp/tab_bases.html'
    return render(request, template_name)


class BaseListarAjaxListView(BaseDatatableView):
    redirect_field_name = 'next'
    model = Base
    columns = ['identificador', 'numero_espacio', 'telefono', 'direccion', 'sitio', 'editar', 'eliminar']
    order_columns = ['identificador']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('webapp:edit_base',
                                                   kwargs={
                                                       'pk': row.pk}) + '"><i class="material-icons">edit</i></a>'
        elif column == 'eliminar':
            return '<a class=" modal-trigger" href ="#" onclick="actualiza(' + str(
                row.pk) + ')"><i class="material-icons">delete_forever</i></a>'
        elif column == 'direccion':
            return row.direccion.get_address()
        elif column == 'sitio':
            return row.sitio.__str__()

        return super(BaseListarAjaxListView, self).render_column(row, column)

    def get_initial_queryset(self):
        return Base.objects.all()


class BaseActualizar(PermissionRequiredMixin, UpdateView):
    redirect_field_name = 'next'
    login_url = '/webapp/'
    permission_required = 'change_base'
    model = Base
    segundoModelo = Direccion
    template_name = 'config/formBase.html'
    form_class = BaseForm
    segundo_form = DireccionForm
    id_base = 0

    def get_context_data(self, **kwargs):
        context = super(BaseActualizar, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        base = self.model.objects.get(id=pk)
        direccion = self.segundoModelo.objects.get(id=base.direccion_id)
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
            # lon= self.request.POST.get('lgn')
            # lat = self.request.POST.get('lat')
            # pnt = Point(float(lon), float(lat))
            # self.segundo_form.instance.latlgn = pnt

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
        return reverse('webapp:list_base')


def base_eliminar(request, pk):
    b = get_object_or_404(Base, pk=pk)
    id_direccion = b.direccion.id
    d = get_object_or_404(Direccion, pk=id_direccion)
    d.delete()
    b.delete()
    return JsonResponse({'result': 1})


class PaisCrear(PermissionRequiredMixin, CreateView):
    redirect_field_name = 'next'
    login_url = '/webapp/'
    permission_required = 'add_pais'
    model = Pais
    form_class = PaisForm
    template_name = 'config/form_1col.html'

    def get_success_url(self):
        return reverse('webapp:list_pais')


def pais_listar(request):
    template_name = 'webapp/tab_pais.html'
    return render(request, template_name)


class PaisListarAjaxListView(BaseDatatableView):
    redirect_field_name = 'next'
    model = Pais
    columns = ['nombre', 'editar', 'eliminar']
    order_columns = ['nombre']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('webapp:edit_pais',
                                                   kwargs={
                                                       'pk': row.pk}) + '"><i class="material-icons">edit</i></a>'
        elif column == 'eliminar':
            return '<a class="modal-trigger" href ="#" onclick="actualiza(' + str(
                row.pk) + ')"><i class="material-icons">delete_forever</i></a>'

        return super(PaisListarAjaxListView, self).render_column(row, column)

    def get_initial_queryset(self):
        return Pais.objects.all()


class PaisActualizar(PermissionRequiredMixin, UpdateView):
    redirect_field_name = 'next'
    login_url = '/webapp/'
    permission_required = 'change_pais'
    redirect_field_name = 'next'
    model = Pais
    template_name = 'config/form_1col.html'
    form_class = PaisForm

    def get_success_url(self):
        return reverse('webapp:list_pais')


def pais_eliminar(request, pk):
    p = get_object_or_404(Pais, pk=pk)
    p.delete()
    return JsonResponse({'result': 1})


class CiudadCrear(PermissionRequiredMixin, CreateView):
    redirect_field_name = 'next'
    login_url = '/webapp/'
    permission_required = 'add_ciudad'
    model = Ciudad
    form_class = CiudadForm
    template_name = 'config/formMap.html'

    def form_valid(self, form):
        lon = self.request.POST.get('lgn')
        lat = self.request.POST.get('lat')
        pnt = Point(float(lon), float(lat))
        form.instance.centro = pnt
        return super(CiudadCrear, self).form_valid(form)

    def get_success_url(self):
        return reverse('webapp:list_ciudad')


def ciudad_listar(request):
    template_name = 'webapp/tab_ciudad.html'
    return render(request, template_name)


class CiudadListarAjaxListView(BaseDatatableView):
    redirect_field_name = 'next'
    model = Ciudad
    columns = ['nombre', 'factor_tiempo', 'radio', 'pais', 'editar', 'eliminar']
    order_columns = ['nombre']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('webapp:edit_ciudad',
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


class CiudadActualizar(PermissionRequiredMixin, UpdateView):
    redirect_field_name = 'next'
    login_url = '/webapp/'
    permission_required = 'change_ciudad'
    model = Ciudad
    template_name = 'config/formMap.html'
    form_class = CiudadForm

    def form_valid(self, form):
        lon = self.request.POST.get('lgn')
        lat = self.request.POST.get('lat')
        pnt = Point(float(lon), float(lat))
        form.instance.centro = pnt
        return super(CiudadActualizar, self).form_valid(form)

    def get_success_url(self):
        return reverse('webapp:list_ciudad')


def ciudad_eliminar(request, pk):
    c = get_object_or_404(Ciudad, pk=pk)
    c.delete()
    return JsonResponse({'result': 1})


class SucursalCrear(PermissionRequiredMixin, CreateView):
    redirect_field_name = 'next'
    login_url = '/webapp/'
    permission_required = 'add_sucursal'
    model = Sucursal
    form_class = SucursalForm
    template_name = 'config/formMap.html'

    def form_valid(self, form):
        lon = self.request.POST.get('lgn')
        lat = self.request.POST.get('lat')
        pnt = Point(float(lon), float(lat))
        form.instance.coordenadas = pnt
        return super(SucursalCrear, self).form_valid(form)

    def get_success_url(self):
        return reverse('webapp:list_sucursal')


def sucursal_listar(request):
    template_name = 'webapp/tab_sucursal.html'
    return render(request, template_name)


class SucursalListarAjaxListView(BaseDatatableView):
    redirect_field_name = 'next'
    model = Sucursal
    columns = ['nombre', 'clave', 'direccion', 'usuario', 'empresa', 'editar', 'eliminar']
    order_columns = ['nombre', 'clave', 'direccion', 'usuario', 'empresa']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('webapp:edit_sucursal',
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


class SucursalActualizar(PermissionRequiredMixin, UpdateView):
    redirect_field_name = 'next'
    login_url = '/webapp/'
    permission_required = 'change_sucursal'
    model = Sucursal
    template_name = 'config/formMap.html'
    form_class = SucursalForm

    def form_valid(self, form):
        lon = self.request.POST.get('lgn')
        lat = self.request.POST.get('lat')
        pnt = Point(float(lon), float(lat))
        form.instance.coordenadas = pnt
        return super(SucursalActualizar, self).form_valid(form)

    def get_success_url(self):
        return reverse('webapp:list_sucursal')


def sucursal_eliminar(request, pk):
    s = get_object_or_404(Sucursal, pk=pk)
    s.delete()
    return JsonResponse({'result': 1})


class FormaPagoCrear(PermissionRequiredMixin, CreateView):
    redirect_field_name = 'next'
    login_url = '/webapp/'
    permission_required = 'add_tipopago'
    model = TipoPago
    form_class = TipoPagoForm
    template_name = 'config/form_1col.html'

    def get_success_url(self):
        return reverse('webapp:list_forma_pago')


def forma_pago_listar(request):
    template_name = 'webapp/tab_forma_pago.html'
    return render(request, template_name)


class FormaPagoListarAjaxListView(BaseDatatableView):
    redirect_field_name = 'next'
    model = TipoPago
    columns = ['nombre', 'precio', 'plan', 'editar', 'eliminar']
    order_columns = ['nombre', 'precio', 'plan']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('webapp:edit_forma_pago',
                                                   kwargs={
                                                       'pk': row.pk}) + '"><i class="material-icons">edit</i></a>'
        elif column == 'eliminar':
            return '<a class=" modal-trigger" href ="#" onclick="actualiza(' + str(
                row.pk) + ')"><i class="material-icons">delete_forever</i></a>'

        return super(FormaPagoListarAjaxListView, self).render_column(row, column)

    def get_initial_queryset(self):
        return TipoPago.objects.all()


class FormaPagoActualizar(PermissionRequiredMixin, UpdateView):
    redirect_field_name = 'next'
    login_url = '/webapp/'
    permission_required = 'change_tipopago'
    model = TipoPago
    template_name = 'config/form_1col.html'
    form_class = TipoPagoForm

    def get_success_url(self):
        return reverse('webapp:list_forma_pago')


def forma_pago_eliminar(request, pk):
    tp = get_object_or_404(TipoPago, pk=pk)
    tp.delete()
    return JsonResponse({'result': 1})


class TipoVehiculoCrear(PermissionRequiredMixin, CreateView):
    redirect_field_name = 'next'
    login_url = '/webapp/'
    permission_required = 'add_tipovehiculo'
    model = TipoVehiculo
    form_class = TipoVehiculoForm
    template_name = 'config/form_1col.html'

    def get_success_url(self):
        return reverse('webapp:list_tipo_vehiculo')


def tipo_vehiculo_listar(request):
    template_name = 'webapp/tab_tipo_vehiculo.html'
    return render(request, template_name)


class TipoVehiculoListarAjaxListView(BaseDatatableView):
    redirect_field_name = 'next'
    model = TipoVehiculo
    columns = ['nombre', 'num_max_pasajeros', 'num_maletas', 'editar', 'eliminar']
    order_columns = ['nombre', 'num_max_pasajeros', 'num_maletas']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('webapp:edit_tipo_vehiculo',
                                                   kwargs={
                                                       'pk': row.pk}) + '"><i class="material-icons">edit</i></a>'
        elif column == 'eliminar':
            return '<a class=" modal-trigger" href ="#" onclick="actualiza(' + str(
                row.pk) + ')"><i class="material-icons">delete_forever</i></a>'

        return super(TipoVehiculoListarAjaxListView, self).render_column(row, column)

    def get_initial_queryset(self):
        return TipoVehiculo.objects.all()


class TipoVehiculoActualizar(PermissionRequiredMixin, UpdateView):
    redirect_field_name = 'next'
    login_url = '/webapp/'
    permission_required = 'change_tipovehiculo'
    model = TipoVehiculo
    template_name = 'config/form_1col.html'
    form_class = TipoVehiculoForm

    def get_success_url(self):
        return reverse('webapp:list_tipo_vehiculo')


def tipoVehiculoEliminar(request, pk):
    tv = get_object_or_404(TipoVehiculo, pk=pk)
    tv.delete()
    return JsonResponse({'result': 1})


class ClienteCrear(PermissionRequiredMixin, CreateView):
    redirect_field_name = 'next'
    login_url = '/webapp/'
    permission_required = 'add_cliente'
    model = Cliente
    form_class = ClienteForm
    template_name = 'config/form_1col.html'

    def form_valid(self, form):
        form.instance.set_password(form.cleaned_data['password'])
        form.instance.rol = Rol(pk=2)
        return super(ClienteCrear, self).form_valid(form)

    def get_success_url(self):
        return reverse('webapp:list_cliente')


def cliente_listar(request):
    template_name = 'webapp/tab_cliente.html'
    return render(request, template_name)


class ClienteListarAjaxListView(BaseDatatableView):
    redirect_field_name = 'next'
    model = Cliente
    columns = ['nombre', 'email', 'telefono', 'rfc', 'estatus', 'editar', 'eliminar']
    order_columns = ['nombre', 'email', 'telefono', 'rfc', 'estatus']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('webapp:edit_cliente',
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


class ClienteActualizar(PermissionRequiredMixin, UpdateView):
    redirect_field_name = 'next'
    login_url = '/webapp/'
    permission_required = 'change_cliente'
    model = Cliente
    template_name = 'config/form_1col.html'
    form_class = ClienteForm

    def get_success_url(self):
        return reverse('webapp:list_cliente')


def cliente_eliminar(request, pk):
    u = get_object_or_404(Cliente, pk=pk)
    u.estatus = False
    u.save()
    return JsonResponse({'result': 1})


class TipoServicioCrear(PermissionRequiredMixin, CreateView):
    redirect_field_name = 'next'
    login_url = '/webapp/'
    permission_required = 'add_tiposervicio'
    model = TipoServicio
    form_class = TipoServicioForm
    template_name = 'config/form_1col.html'

    def get_success_url(self):
        return reverse('webapp:list_tipoServicio')


def tipo_servicio_listar(request):
    template_name = 'webapp/tab_tipo_servicio.html'
    return render(request, template_name)


class TipoServicioListarAjaxListView(BaseDatatableView):
    redirect_field_name = 'next'
    model = TipoServicio
    columns = ['nombre', 'editar', 'eliminar']
    order_columns = ['nombre']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('webapp:edit_tipoServicio',
                                                   kwargs={
                                                       'pk': row.pk}) + '"><i class="material-icons">edit</i></a>'
        elif column == 'eliminar':
            return '<a class=" modal-trigger" href ="#" onclick="actualiza(' + str(
                row.pk) + ')"><i class="material-icons">delete_forever</i></a>'

        return super(TipoServicioListarAjaxListView, self).render_column(row, column)

    def get_initial_queryset(self):
        return TipoServicio.objects.all()


class TipoServicioActualizar(PermissionRequiredMixin, UpdateView):
    redirect_field_name = 'next'
    login_url = '/webapp/'
    permission_required = 'change_tiposervicio'
    model = TipoServicio
    template_name = 'config/form_1col.html'
    form_class = TipoServicioForm

    def get_success_url(self):
        return reverse('webapp:list_tipoServicio')


def tipoServicio_eliminar(request, pk):
    ts = get_object_or_404(TipoServicio, pk=pk)
    ts.delete()
    return JsonResponse({'result': 1})


class MarcaCrear(PermissionRequiredMixin, CreateView):
    redirect_field_name = 'next'
    login_url = '/webapp/'
    permission_required = 'add_marca'
    model = Marca
    form_class = MarcaForm
    template_name = 'config/form_1col.html'

    def get_success_url(self):
        return reverse('webapp:list_marca')


def marca_listar(request):
    template_name = 'webapp/tab_marca.html'
    return render(request, template_name)


class MarcaListarAjaxListView(BaseDatatableView):
    redirect_field_name = 'next'
    model = Marca
    columns = ['nombre', 'editar', 'eliminar']
    order_columns = ['nombre']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('webapp:edit_marca',
                                                   kwargs={
                                                       'pk': row.pk}) + '"><i class="material-icons">edit</i></a>'
        elif column == 'eliminar':
            return '<a class=" modal-trigger" href ="#" onclick="actualiza(' + str(
                row.pk) + ')"><i class="material-icons">delete_forever</i></a>'

        return super(MarcaListarAjaxListView, self).render_column(row, column)

    def get_initial_queryset(self):
        return Marca.objects.all()


class MarcaActualizar(PermissionRequiredMixin, UpdateView):
    redirect_field_name = 'next'
    login_url = '/webapp/'
    permission_required = 'change_marca'
    model = Marca
    template_name = 'config/form_1col.html'
    form_class = MarcaForm

    def get_success_url(self):
        return reverse('webapp:list_marca')


def marca_eliminar(request, pk):
    m = get_object_or_404(Marca, pk=pk)
    m.delete()
    return JsonResponse({'result': 1})


class ModeloCrear(PermissionRequiredMixin, CreateView):
    redirect_field_name = 'next'
    login_url = '/webapp/'
    permission_required = 'add_modelo'
    model = Modelo
    form_class = ModeloForm
    template_name = 'config/form_1col.html'

    def get_success_url(self):
        return reverse('webapp:list_modelo')


def modelo_listar(request):
    template_name = 'webapp/tab_modelo.html'
    return render(request, template_name)


class ModeloListarAjaxListView(BaseDatatableView):
    redirect_field_name = 'next'
    model = Modelo
    columns = ['nombre', 'marca', 'editar', 'eliminar']
    order_columns = ['nombre', 'marca']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('webapp:edit_modelo',
                                                   kwargs={
                                                       'pk': row.pk}) + '"><i class="material-icons">edit</i></a>'
        elif column == 'eliminar':
            return '<a class=" modal-trigger" href ="#" onclick="actualiza(' + str(
                row.pk) + ')"><i class="material-icons">delete_forever</i></a>'
        elif column == 'marca':
            return row.marca.nombre

        return super(ModeloListarAjaxListView, self).render_column(row, column)

    def get_initial_queryset(self):
        return Modelo.objects.all()


class ModeloActualizar(PermissionRequiredMixin, UpdateView):
    redirect_field_name = 'next'
    login_url = '/webapp/'
    permission_required = 'change_modelo'
    model = Modelo
    template_name = 'config/form_1col.html'
    form_class = ModeloForm

    def get_success_url(self):
        return reverse('webapp:list_modelo')


def modelo_eliminar(request, pk):
    m = get_object_or_404(Modelo, pk=pk)
    m.delete()
    return JsonResponse({'result': 1})


class PropietarioCrear(PermissionRequiredMixin, CreateView):
    redirect_field_name = 'next'
    login_url = '/webapp/'
    permission_required = 'add_propietario'
    model = Propietario
    form_class = PropietarioForm
    template_name = 'config/form_1col.html'

    def form_valid(self, form):
        form.instance.set_password(form.cleaned_data['password'])
        form.instance.rol = Rol(pk=4)
        return super(PropietarioCrear, self).form_valid(form)

    def get_success_url(self):
        return reverse('webapp:list_propietario')


def propietario_listar(request):
    template_name = 'webapp/tab_propietario.html'
    return render(request, template_name)


class PropietarioListarAjaxListView(BaseDatatableView):
    redirect_field_name = 'next'
    model = Propietario
    columns = ['nombre', 'email', 'telefono', 'razon_social', 'estatus', 'editar', 'eliminar']
    order_columns = ['nombre', 'email', 'telefono', 'razon_social', 'estatus']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('webapp:edit_propietario',
                                                   kwargs={
                                                       'pk': row.pk}) + '"><i class="material-icons">edit</i></a>'
        elif column == 'nombre':
            return row.get_full_name()
        elif column == 'eliminar':
            return '<a class=" modal-trigger" href ="#" onclick="actualiza(' + str(
                row.pk) + ')"><i class="material-icons">delete_forever</i></a>'

        return super(PropietarioListarAjaxListView, self).render_column(row, column)

    def get_initial_queryset(self):
        return Propietario.objects.filter(estatus=True, rol=4)


class PropietarioActualizar(PermissionRequiredMixin, UpdateView):
    redirect_field_name = 'next'
    login_url = '/webapp/'
    permission_required = 'change_propietario'
    model = Propietario
    template_name = 'config/form_1col.html'
    form_class = PropietarioForm

    def get_success_url(self):
        return reverse('webapp:list_propietario')


def propietario_eliminar(request, pk):
    u = get_object_or_404(Propietario, pk=pk)
    u.estatus = False
    u.save()
    return JsonResponse({'result': 1})


class VehiculoCrear(PermissionRequiredMixin, CreateView):
    redirect_field_name = 'next'
    login_url = '/webapp/'
    permission_required = 'add_vehiculo'
    model = Vehiculo
    form_class = VehiculoForm
    template_name = 'config/form_1col.html'

    def get_success_url(self):
        return reverse('webapp:list_vehiculo')


def vehiculo_listar(request):
    template_name = 'webapp/tab_vehiculo.html'
    return render(request, template_name)


class VehiculoListarAjaxListView(BaseDatatableView):
    redirect_field_name = 'next'
    model = Vehiculo
    columns = ['placa', 'anio', 'modelo', 'cromatica', 'propietario', 'economico', 'ciudad', 'editar', 'eliminar']
    order_columns = ['placa', 'anio', 'modelo', 'cromatica', 'propietario', 'economico', 'ciudad']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('webapp:edit_vehiculo',
                                                   kwargs={
                                                       'pk': row.pk}) + '"><i class="material-icons">edit</i></a>'
        elif column == 'propietario':
            return row.propietario.get_full_name()
        elif column == 'modelo':
            return row.modelo.nombre
        elif column == 'ciudad':
            return row.ciudad.nombre
        elif column == 'eliminar':
            return '<a class=" modal-trigger" href ="#" onclick="actualiza(' + str(
                row.pk) + ')"><i class="material-icons">delete_forever</i></a>'

        return super(VehiculoListarAjaxListView, self).render_column(row, column)

    def get_initial_queryset(self):
        return Vehiculo.objects.filter(estatus=True)


class VehiculoActualizar(PermissionRequiredMixin, UpdateView):
    redirect_field_name = 'next'
    login_url = '/webapp/'
    permission_required = 'change_vehiculo'
    model = Vehiculo
    template_name = 'config/form_1col.html'
    form_class = VehiculoForm

    def get_success_url(self):
        return reverse('webapp:list_vehiculo')


def vehiculo_eliminar(request, pk):
    v = get_object_or_404(Vehiculo, pk=pk)
    v.estatus = False
    v.save()
    return JsonResponse({'result': 1})


class TarifaCrear(PermissionRequiredMixin, CreateView):
    redirect_field_name = 'next'
    login_url = '/webapp/'
    permission_required = 'add_tarifa'
    model = Tarifa
    form_class = TarifaForm
    template_name = 'webapp/registro_tarifario.html'

    def get_context_data(self, **kwargs):
        context = super(TarifaCrear, self).get_context_data(**kwargs)
        context['tipoPago'] = TipoPago.objects.all()
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

    def get_success_url(self):
        return reverse('webapp:list_tarifa')

def tarifa_crear(request):
    template_name = 'webapp/registro_tarifario.html'
    if request.method == 'POST':
        form = TarifaForm(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            return reverse('webapp:list_tarifa')
        return render(request, template_name, {'form': form})
    else:
        form = TarifaForm()
        print(form)
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
        print(pago)
        pago = pago.split(",")
        pago.pop(0)
        print(pago)
        pagoList = []
        for i in pago:
            pagoList.append(int(i))
        print(pagoList)
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
        print(tarifa)
        tarifa.save()
        print(pago)
        try:
            for i in range(len(pagoList)):
                pk_pago = TipoPago.objects.get(pk=pagoList[i])
                tarifa.pago.add(pk_pago)
        except ValueError:
            print("no se puede convertir")
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
    columns = ['tarifa_base', 'ciudad', 'sitio', 'empresa', 'sucursal', 'pais', 'horario', 'editar', 'eliminar']
    order_columns = ['tarifa_base', 'ciudad', 'sitio', 'empresa', 'sucursal', 'pais']
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
        elif column == 'empresa':
            return row.empresa.nombre
        elif column == 'sucursal':
            return row.sucursal.nombre
        elif column == 'pais':
            return row.pais.nombre
        elif column == 'eliminar':
            return '<a class=" modal-trigger" href ="#" onclick="actualiza(' + str(
                row.pk) + ')"><i class="material-icons">delete_forever</i></a>'

        return super(TarifaListarAjaxListView, self).render_column(row, column)

    def get_initial_queryset(self):
        return Tarifa.objects.all()

def horarios_tarifa(request, pk):
    template_name = 'webapp/horario_tarifa.html'
    t = get_object_or_404(Tarifa, pk=pk)
    horarios = t.horario_set.all()
    context = {"horarios": horarios, "tarifa": t}
    return render(request, template_name, context)

def agregar_horario(request):
    response_data = {}
    try:
        t = Tarifa.objects.get(pk=request.POST.get('tarifa'))
        h = Horario(horainicio=request.POST.get('horainicio'),
                    horafin=request.POST.get('horafin'), diasemana=request.POST.get('diasemana'),
                    tarifa=t)
        h.save()
        response_data['success'] = 'success'
        return redirect(
            reverse('webapp:horario_tarifa', kwargs={'pk': t.pk}))
    except Exception as e:
        response_data['error'] = 'error'
    return JsonResponse(response_data)

def editar_horario(request, pk):
    response_data = {}
    try:
        h = Horario.objects.get(pk=pk)
        h.horainicio = request.POST.get('horainicio')
        h.horafin = request.POST.get('horafin')
        h.diasemana = request.POST.get('diasemana')
        h.save()
        response_data['success'] = 'success'
    except Horario.DoesNotExist:
        response_data['error'] = 'error'
    return JsonResponse(response_data)

def eliminar_horario(request, pk):
    response_data = {}
    try:
        h = Horario.objects.get(pk=pk)
        h.delete()
        response_data['success'] = 'success'
    except Horario.DoesNotExist:
        response_data['error'] = 'error'
    return JsonResponse(response_data)

def vehiculos_chofer(request, pk):
    template_name = 'webapp/vehiculo_chofer.html'
    c = get_object_or_404(Chofer, pk=pk)
    vehiculos = c.taxis.all()
    context = {"horarios": vehiculos, "chofer": c}
    return render(request, template_name, context)



class ComisionCrear(PermissionRequiredMixin, CreateView):
    redirect_field_name = 'next'
    login_url = '/webapp/'
    permission_required = 'add_comisiones'
    model = Comisiones
    form_class = ComisionForm
    template_name = 'config/form_1col.html'

    def get_success_url(self):
        return reverse('webapp:list_comision')


def comision_listar(request):
    template_name = 'webapp/tab_comision.html'
    return render(request, template_name)


class ComisionListarAjaxListView(BaseDatatableView):
    redirect_field_name = 'next'
    model = Comisiones
    columns = ['nombre', 'tipo', 'factor', 'editar', 'eliminar']
    order_columns = ['nombre', 'tipo', 'factor']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('webapp:edit_comision',
                                                   kwargs={
                                                       'pk': row.pk}) + '"><i class="material-icons">edit</i></a>'
        elif column == 'tipo':
            return '%' if row.tipo == 1 else '$'
        elif column == 'eliminar':
            return '<a class=" modal-trigger" href ="#" onclick="actualiza(' + str(
                row.pk) + ')"><i class="material-icons">delete_forever</i></a>'

        return super(ComisionListarAjaxListView, self).render_column(row, column)

    def get_initial_queryset(self):
        return Comisiones.objects.all()


class ComisionActualizar(PermissionRequiredMixin, UpdateView):
    redirect_field_name = 'next'
    login_url = '/webapp/'
    permission_required = 'change_comisiones'
    model = Comisiones
    template_name = 'config/form_1col.html'
    form_class = ComisionForm

    def get_success_url(self):
        return reverse('webapp:list_comision')


def comision_eliminar(request, pk):
    c = get_object_or_404(Comisiones, pk=pk)
    c.delete()
    return JsonResponse({'result': 1})


def reset_confirm(request, uidb64=None, token=None):
    uid = force_text(urlsafe_base64_decode(uidb64))
    return password_reset_confirm(request, template_name='webapp/reset.html',
                                  uidb64=uidb64,
                                  token=token,
                                  # post_reset_redirect=reverse('webapp:index')
                                  post_reset_redirect=reverse('webapp:index')
                                  )
