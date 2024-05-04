from django.urls import path
from .views import  Get_Especialidades,Create_Horario,Get_Horarios,ListAllDoctors

urlpatterns = [
    path('medico/listar',ListAllDoctors.as_view()),
    path('especialidades/listar/',Get_Especialidades.as_view(),),
    path('horario/crear/',Create_Horario.as_view(),),
    path('horario/obtener/',Get_Horarios.as_view())
]
