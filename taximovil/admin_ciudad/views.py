from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, UpdateView
from django_datatables_view.base_datatable_view import BaseDatatableView

from admin_ciudad.forms import SitioForm, AdministradorSitioForm
from config.models import AdministradorSitio, Sitio, Rol


class SitioCrear(PermissionRequiredMixin, CreateView):
    redirect_field_name = 'next'
    login_url = '/webapp/'
    permission_required = 'admin_ciudad'
    model = Sitio
    form_class = SitioForm
    template_name = 'config/form_1col.html'

    def get_context_data(self, **kwargs):
        context = super(SitioCrear, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Registro de sitios'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Completa todos los campos para registrar un sitio'
        return context

    def get_success_url(self):
        return reverse('admin_ciudad:list_sitio')


def sitio_listar(request):
    template_name = 'admin_ciudad/tab_sitio.html'
    return render(request, template_name)


class SitioListarAjaxListView(BaseDatatableView):
    redirect_field_name = 'next'
    model = Sitio
    columns = ['nombre', 'num_espacio', 'pv', 'editar', 'eliminar']
    order_columns = ['nombre', 'num_espacio', 'pv']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('admin_ciudad:edit_sitio',
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
    permission_required = 'admin_ciudad'
    model = Sitio
    template_name = 'config/form_1col.html'
    form_class = SitioForm

    def get_context_data(self, **kwargs):
        context = super(SitioActualizar, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Edición de sitios'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Modifica los campos que requieras'
        return context

    def get_success_url(self):
        return reverse('admin_ciudad:list_sitio')


def sitio_eliminar(request, pk):
    e = get_object_or_404(Sitio, pk=pk)
    e.delete()
    return JsonResponse({'result': 1})

class AdministradorSitioCrear(PermissionRequiredMixin, CreateView):
    redirect_field_name = 'next'
    login_url = '/webapp/'
    permission_required = 'admin_sitio'
    model = AdministradorSitio
    form_class = AdministradorSitioForm
    template_name = 'config/form_1col.html'

    def get_context_data(self, **kwargs):
        context = super(AdministradorSitioCrear, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Registro de admin_ciudad'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Completa todos los campos para registrar un personal de admin_ciudad'
        return context

    def form_valid(self, form):
        administrador_sitio = AdministradorSitio.objects.get(pk=self.request.user)
        config_sitio = ConfigUsuariosSitio.objects.filter(sitio = administrador_sitio.sitio)
        if not config_sitio.exists():
            new_config_admin_ciudad = ConfigUsuariosSitio.objects.create(sitio=administrador_sitio.sitio)
            num_usuarios_admin_ciudad = AdministradorSitio.objects.filter(sitio=administrador_sitio.sitio, estatus=True).count()
            if num_usuarios_admin_ciudad >= new_config_admin_ciudad.max_admin_ciudad:
                return render(self.request, template_name=self.template_name,
                              context={'form': form,
                                       'error': 'Tienes registrados '+ str(num_usuarios_admin_ciudad) + ' usuarios activos de '+
                                                str(config_sitio.max_admin_ciudad)+ ' permitidos, no puedes registrar mas.'})
        else:
            config_sitio =config_sitio.first()
            num_usuarios_admin_ciudad = AdministradorSitio.objects.filter(sitio=administrador_sitio.sitio, estatus=True).count()
            if num_usuarios_admin_ciudad >= config_sitio.max_admin_ciudad:
                return render(self.request, template_name=self.template_name,
                              context={'form': form,
                                       'error': 'Tienes registrados '+ str(num_usuarios_admin_ciudad) + ' usuarios activos de '+
                                                str(config_sitio.max_admin_ciudad)+ ' permitidos, no puedes registrar mas.'})

        user = form.save(commit=False)
        user.set_password(user.password)
        user.rol = Rol(pk=10)
        user.sitio = administrador_sitio.sitio
        user.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('admin_sitio:list_admin_ciudad')

@permission_required(perm='admin_sitio', login_url='/webapp/')
def admin_ciudad_listar(request):
    template_name = 'admin_sitio/tab_admin_ciudad.html'
    return render(request, template_name)


class AdministradorSitioListarAjaxListView(PermissionRequiredMixin, BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/webapp/'
    permission_required = 'admin_sitio'
    model = AdministradorSitio
    columns = ['nombre', 'email', 'telefono', 'editar', 'estatus']
    order_columns = ['nombre', 'email', 'telefono', '', 'estatus']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('admin_sitio:edit_admin_ciudad',
                                                   kwargs={
                                                       'pk': row.pk}) + '"><i class="material-icons">edit</i></a>'
        elif column == 'nombre':
            return row.get_full_name()
        elif column == 'eliminar':
            return '<a class=" modal-trigger" href ="#" onclick="actualiza(' + str(
                row.pk) + ')"><i class="material-icons">delete_forever</i></a>'
        elif column == 'estatus':
            if row.estatus:
                return '<div class="switch"><label>Off<input type="checkbox" checked onchange=cambiar_estatus(' + str(
                    row.pk) + ')><span class="lever"></span>On</label></div>'
            else:
                return '<div class="switch"><label>Off<input type="checkbox" onchange=cambiar_estatus(' + str(
                    row.pk) + ')><span class="lever"></span>On</label></div>'

        return super(AdministradorSitioListarAjaxListView, self).render_column(row, column)

    def get_initial_queryset(self):
        admin_sitio = AdministradorSitio.objects.get(pk=self.request.user)
        sitio = admin_sitio.sitio
        return AdministradorSitio.objects.filter(sitio=sitio)


class AdministradorSitioActualizar(PermissionRequiredMixin, UpdateView):
    redirect_field_name = 'next'
    login_url = '/webapp/'
    permission_required = 'admin_sitio'
    model = AdministradorSitio
    template_name = 'config/form_1col.html'
    form_class = AdministradorSitioForm

    def get_context_data(self, **kwargs):
        context = super(AdministradorSitioActualizar, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Modificación de admin_ciudad'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Modifica los campos que requieras'
        return context

    def form_valid(self, form):
        form.instance.set_password(form.cleaned_data['password'])
        form.save()
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('admin_sitio:list_admin_ciudad')
