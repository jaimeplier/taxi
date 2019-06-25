from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import CreateView, UpdateView
from django_datatables_view.base_datatable_view import BaseDatatableView

from admin_ciudad.forms import SitioForm, AdministradorSitioForm
from admin_sitio.forms import CallcenterForm
from config.models import AdministradorSitio, Sitio, Rol, AdministradorCiudad, ConfigUsuariosSitio, Callcenter


def sitio_owner(request, sitio_pk):
    try:
        admin_ciudad = AdministradorCiudad.objects.get(pk=request.user)
        sitios = Sitio.objects.filter(admin_ciudad=admin_ciudad).values_list('pk', flat=True)
        if sitio_pk in sitios:
            return True
        else:
            return False
    except:
        return False

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
    columns = ['nombre', 'num_espacio', 'pv', 'admin_sitio', 'personal_callcenter', 'editar', 'eliminar']
    order_columns = ['nombre', 'num_espacio', 'pv', '', '', '', '']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('admin_ciudad:edit_sitio',
                                                   kwargs={
                                                       'pk': row.pk}) + '"><i class="material-icons">edit</i></a>'
        elif column == 'eliminar':
            return '<a class=" modal-trigger" href ="#" onclick="actualiza(' + str(
                row.pk) + ')"><i class="material-icons">delete_forever</i></a>'
        elif column == 'admin_sitio':
            return '<a class="" href ="' + reverse('admin_ciudad:list_admin_sitio',
                                                   kwargs={
                                                       'sitio': row.pk}) + '"><i class="material-icons">people</i></a>'
        elif column == 'personal_callcenter':
            return '<a class="" href ="' + reverse('admin_ciudad:list_callcenter',
                                                   kwargs={
                                                       'sitio': row.pk}) + '"><i class="material-icons">contact_phone</i></a>'

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
    permission_required = 'admin_ciudad'
    model = AdministradorSitio
    form_class = AdministradorSitioForm
    template_name = 'config/form_1col.html'

    def get_context_data(self, **kwargs):
        context = super(AdministradorSitioCrear, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Registro de administrador de sitio'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Completa todos los campos para registrar un administrador de sitio'
        return context

    def form_valid(self, form):
        if sitio_owner(self.request, self.kwargs['sitio']):
            config_sitio = ConfigUsuariosSitio.objects.get(sitio = self.kwargs['sitio'])
            num_usuarios_admin_sitio = AdministradorSitio.objects.filter(sitio=config_sitio.sitio, estatus=True).count()
            if num_usuarios_admin_sitio >= config_sitio.max_administradores:
                return render(self.request, template_name=self.template_name,
                              context={'form': form,
                                       'error': 'Tienes registrados '+ str(num_usuarios_admin_sitio) + ' usuarios activos de '+
                                                str(config_sitio.max_administradores)+ ' permitidos, no puedes registrar mas.'})
            user = form.save(commit=False)
            user.set_password(user.password)
            user.rol = Rol(pk=10)
            user.sitio = config_sitio.sitio
            user.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return HttpResponseForbidden()

    def get_success_url(self):
        return reverse('admin_ciudad:list_admin_sitio', kwargs={'sitio': self.kwargs['sitio']})

@permission_required(perm='admin_ciudad', login_url='/webapp/')
def admin_sitio_listar(request, sitio):
    admin_ciudad = AdministradorCiudad.objects.get(pk=request.user)
    sitios = Sitio.objects.filter(admin_ciudad=admin_ciudad).values_list('pk', flat=True)
    sitio_pk = sitio
    if sitio_pk in sitios:
        sitio = Sitio.objects.get(pk=sitio)
    else:
        return HttpResponseForbidden()
    context = {'sitio': sitio}
    template_name = 'admin_ciudad/tab_admin_sitio.html'
    return render(request, template_name, context)


class AdministradorSitioListarAjaxListView(PermissionRequiredMixin, BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/webapp/'
    permission_required = 'admin_ciudad'
    model = AdministradorSitio
    columns = ['nombre', 'email', 'telefono', 'editar', 'estatus']
    order_columns = ['nombre', 'email', 'telefono', '', 'estatus']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('admin_ciudad:edit_admin_sitio',
                                                   kwargs={
                                                       'pk': row.pk, 'sitio': row.sitio.pk}) + '"><i class="material-icons">edit</i></a>'
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
        sitio_pk = self.kwargs['sitio']
        return AdministradorSitio.objects.filter(sitio__pk=sitio_pk)


class AdministradorSitioActualizar(PermissionRequiredMixin, UpdateView):
    redirect_field_name = 'next'
    login_url = '/webapp/'
    permission_required = 'admin_ciudad'
    model = AdministradorSitio
    template_name = 'config/form_1col.html'
    form_class = AdministradorSitioForm

    def get_context_data(self, **kwargs):
        context = super(AdministradorSitioActualizar, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Modificación de administrador de sitio'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Modifica los campos que requieras'
        return context

    def form_valid(self, form):
        form.instance.set_password(form.cleaned_data['password'])
        form.save()
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('admin_ciudad:list_admin_sitio', kwargs={'sitio': self.kwargs['sitio']})


class CallcenterCrear(PermissionRequiredMixin, CreateView):
    redirect_field_name = 'next'
    login_url = '/webapp/'
    permission_required = 'admin_ciudad'
    model = Callcenter
    form_class = CallcenterForm
    template_name = 'config/form_1col.html'

    def get_context_data(self, **kwargs):
        context = super(CallcenterCrear, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Registro de callcenter'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Completa todos los campos para registrar un personal de callcenter'
        return context

    def form_valid(self, form):
        sitio = self.kwargs['sitio']
        if sitio_owner(self.request, sitio):
            config_sitio = ConfigUsuariosSitio.objects.get(sitio__pk = sitio)
            num_usuarios_callcenter = Callcenter.objects.filter(sitio__pk=sitio, estatus=True).count()
            if num_usuarios_callcenter >= config_sitio.max_callcenter:
                return render(self.request, template_name=self.template_name,
                              context={'form': form,
                                       'error': 'Tienes registrados '+ str(num_usuarios_callcenter) + ' usuarios activos de '+
                                                str(config_sitio.max_callcenter)+ ' permitidos, no puedes registrar mas.'})

            user = form.save(commit=False)
            user.set_password(user.password)
            user.rol = Rol(pk=10)
            user.sitio = config_sitio.sitio
            user.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return HttpResponseForbidden()

    def get_success_url(self):
        return reverse('admin_ciudad:list_callcenter', kwargs={'sitio', self.kwargs['sitio']})

@permission_required(perm='admin_ciudad', login_url='/webapp/')
def callcenter_listar(request, sitio):
    if sitio_owner(request, sitio):
        template_name = 'admin_ciudad/tab_callcenter.html'
        sitio = Sitio.objects.get(pk=sitio)
        context = {'sitio': sitio}
        return render(request, template_name, context)
    else:
        return HttpResponseForbidden()


class CallcenterListarAjaxListView(PermissionRequiredMixin, BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/webapp/'
    permission_required = 'admin_ciudad'
    model = Callcenter
    columns = ['nombre', 'email', 'telefono', 'editar', 'estatus']
    order_columns = ['nombre', 'email', 'telefono', '', 'estatus']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('admin_ciudad:edit_callcenter',
                                                   kwargs={
                                                       'pk': row.pk, 'sitio': self.kwargs['sitio']}) + '"><i class="material-icons">edit</i></a>'
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

        return super(CallcenterListarAjaxListView, self).render_column(row, column)

    def get_initial_queryset(self):
        return Callcenter.objects.filter(sitio__pk=self.kwargs['sitio'])


class CallcenterActualizar(PermissionRequiredMixin, UpdateView):
    redirect_field_name = 'next'
    login_url = '/webapp/'
    permission_required = 'admin_ciudad'
    model = Callcenter
    template_name = 'config/form_1col.html'
    form_class = CallcenterForm

    def get_context_data(self, **kwargs):
        context = super(CallcenterActualizar, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Modificación de callcenter'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Modifica los campos que requieras'
        return context

    def form_valid(self, form):
        form.instance.set_password(form.cleaned_data['password'])
        form.save()
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('admin_ciudad:list_callcenter', kwargs={'sitio':self.kwargs['sitio']})