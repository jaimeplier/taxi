from django.shortcuts import render

def llamada(request):
    template_name = 'callcenter/llamada.html'
    return render(request, template_name)