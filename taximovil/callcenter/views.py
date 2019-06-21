from django.contrib.auth.decorators import permission_required
from django.shortcuts import render

@permission_required(perm='callcenter', login_url = '/webapp/')
def llamada(request):
    template_name = 'callcenter/llamada.html'
    return render(request, template_name)