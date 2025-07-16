
from django.urls import path
from . import views

urlpatterns = [
    path('prioridades/', views.prioridade_fila_list, name='prioridade_fila_list'),
    path('prioridades/<int:pk>/', views.prioridade_fila_detail, name='prioridade_fila_detail'),
    path('prioridades/new/', views.prioridade_fila_create, name='prioridade_fila_create'),
    path('prioridades/<int:pk>/edit/', views.prioridade_fila_update, name='prioridade_fila_update'),
    path('prioridades/<int:pk>/delete/', views.prioridade_fila_delete, name='prioridade_fila_delete'),

    path('filas/', views.fila_espera_list, name='fila_espera_list'),
    path('filas/<uuid:pk>/', views.fila_espera_detail, name='fila_espera_detail'),
    path('filas/new/', views.fila_espera_create, name='fila_espera_create'),
    path('filas/<uuid:pk>/edit/', views.fila_espera_update, name='fila_espera_update'),
    path('filas/<uuid:pk>/delete/', views.fila_espera_delete, name='fila_espera_delete'),
    path('filas/chamar-proximo/', views.chamar_proximo_paciente, name='chamar_proximo_paciente'),
]
