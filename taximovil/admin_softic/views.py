from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import CreateView, UpdateView
from django_datatables_view.base_datatable_view import BaseDatatableView

from admin_softic.forms import AdministradorCiudadForm
from config.models import AdministradorCiudad, AdministradorSitio, Rol


class AdministradorCiudadCrear(PermissionRequiredMixin, CreateView):
    redirect_field_name = 'next'
    login_url = '/webapp/'
    permission_required = 'admin_softic'
    model = AdministradorCiudad
    form_class = AdministradorCiudadForm
    template_name = 'config/form_1col.html'

    def get_context_data(self, **kwargs):
        context = super(AdministradorCiudadCrear, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Registro de administrador_ciudad'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Completa todos los campos para registrar un personal de administrador_ciudad'
        return context

    def form_valid(self, form):
        administrador_sitio = AdministradorSitio.objects.get(pk=self.request.user)

        user = form.save(commit=False)
        user.set_password(user.password)
        user.rol = Rol(pk=5)
        user.sitio = administrador_sitio.sitio
        user.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('admin_softic:list_administrador_ciudad')

@permission_required(perm='admin_softic', login_url='/webapp/')
def administrador_ciudad_listar(request):
    template_name = 'admin_softic/tab_administrador_ciudad.html'
    return render(request, template_name)


class AdministradorCiudadListarAjaxListView(PermissionRequiredMixin, BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/webapp/'
    permission_required = 'admin_softic'
    model = AdministradorCiudad
    columns = ['nombre', 'email', 'telefono', 'editar', 'estatus']
    order_columns = ['nombre', 'email', 'telefono', '', 'estatus']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('admin_softic:edit_administrador_ciudad',
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

        return super(AdministradorCiudadListarAjaxListView, self).render_column(row, column)

    def get_initial_queryset(self):
        return AdministradorCiudad.objects.all()


class AdministradorCiudadActualizar(PermissionRequiredMixin, UpdateView):
    redirect_field_name = 'next'
    login_url = '/webapp/'
    permission_required = 'admin_softic'
    model = AdministradorCiudad
    template_name = 'config/form_1col.html'
    form_class = AdministradorCiudadForm

    def get_context_data(self, **kwargs):
        context = super(AdministradorCiudadActualizar, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Modificación de administrador_ciudad'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Modifica los campos que requieras'
        return context

    def form_valid(self, form):
        form.instance.set_password(form.cleaned_data['password'])
        form.save()
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('admin_softic:list_administrador_ciudad')

