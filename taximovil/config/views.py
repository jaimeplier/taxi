from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse
from django.views.generic import CreateView, UpdateView
from django_datatables_view.base_datatable_view import BaseDatatableView

from config.forms import EmpresaForm, UsuarioForm
from config.models import Empresa, Usuario, Rol, Chofer


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
            return '<a class="white-text" href ="' + reverse('config:edit_empresa',
                                                             kwargs={
                                                                 'pk': row.pk}) + '"><i class="material-icons">edit</i>Editar</a>'
        elif column == 'eliminar':
            return '<a class="white-text modal-trigger" href ="#" onclick="actualiza(' + str(
                row.pk) + ')"><i class="material-icons">delete_forever</i>Eliminar</a>'

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
    template_name = 'config/registro.html'

    def form_valid(self, form):
        form.instance.set_password(form.cleaned_data['password'])
        form.instance.rol = Rol(pk=2)
        return super(UsuarioCrear,self).form_valid(form)

    def get_success_url(self):
        return reverse('config:listar_usuario')

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
            return '<a class="white-text" href ="' + reverse('config:editar_usuario',
                                                             kwargs={
                                                                 'pk': row.pk}) + '"><i class="material-icons">edit</i>Editar</a>'
        elif column == 'nombre':
            return row.get_full_name()
        elif column == 'estatus':
            return 'activo' if row.activo==True else 'inactivo'
        elif column == 'eliminar':
            return '<a class="white-text modal-trigger" href ="#" onclick="actualiza(' + str(
                row.pk) + ')"><i class="material-icons">delete_forever</i>Eliminar</a>'

        return super(UsuarioListarAjaxListView, self).render_column(row, column)

    def get_initial_queryset(self):
        return Usuario.objects.all()

class UsuarioActualizar(UpdateView):
    redirect_field_name = 'next'
    model = Usuario
    template_name = 'config/registro.html'
    form_class = UsuarioForm

    def get_success_url(self):
        return reverse('config:listar_usuario')

def usuario_eliminar(request, pk):
    u = get_object_or_404(Usuario, pk=pk)
    u.estatus = False
    u.save()
    return JsonResponse({'result': 1})


class ChoferCrear(CreateView):
    model = Chofer
    form_class = UsuarioForm
    template_name = 'config/registro.html'

    def form_valid(self, form):
        form.instance.set_password(form.cleaned_data['password'])
        form.instance.rol = Rol(pk=3)
        return super(ChoferCrear, self).form_valid(form)

    def get_success_url(self):
        return reverse('config:listar_chofer')

def choferListar(request):
    template_name = 'config/tab_chofer.html'
    return render(request, template_name)

class ChoferListarAjaxListView(BaseDatatableView):
    redirect_field_name = 'next'
    model = Chofer
    columns = ['nombre', 'email', 'password', 'telefono', 'estatus', 'editar', 'eliminar']
    order_columns = ['nombre']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="white-text" href ="' + reverse('config:editar_chofer',
                                                             kwargs={
                                                                 'pk': row.pk}) + '"><i class="material-icons">edit</i>Editar</a>'
        elif column == 'nombre':
            return row.get_full_name()
        elif column == 'estatus':
            return 'activo' if row.activo == True else 'inactivo'
        elif column == 'eliminar':
            return '<a class="white-text modal-trigger" href ="#" onclick="actualiza(' + str(
                row.pk) + ')"><i class="material-icons">delete_forever</i>Eliminar</a>'

        return super(ChoferListarAjaxListView, self).render_column(row, column)

    def get_initial_queryset(self):
        return Chofer.objects.all()


class ChoferActualizar(UpdateView):
    redirect_field_name = 'next'
    model = Chofer
    template_name = 'config/registro.html'
    form_class = UsuarioForm

    def get_success_url(self):
        return reverse('config:listar_chofer')


def chofer_eliminar(request, pk):
    u = get_object_or_404(Chofer, pk=pk)
    u.estatus = False
    u.save()
    return JsonResponse({'result': 1})