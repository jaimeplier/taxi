from django.urls import path
from . import views

app_name='callcenter'

urlpatterns = [
    path('llamada/', views.llamada, name='llamada'),
]