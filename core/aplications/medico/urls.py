from django.urls import path
from .views import  Get_Especialidades

urlpatterns = [
    path('Listar_Especialidades/',Get_Especialidades.as_view(),)
]
