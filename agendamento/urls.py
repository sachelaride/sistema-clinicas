from django.urls import path
from . import views

urlpatterns = [
    path('servicos/', views.servico_list, name='servico_list'),
    path('servicos/<int:pk>/', views.servico_detail, name='servico_detail'),
    path('servicos/new/', views.servico_create, name='servico_create'),
    path('servicos/<int:pk>/edit/', views.servico_update, name='servico_update'),
    path('servicos/<int:pk>/delete/', views.servico_delete, name='servico_delete'),

    path('salas/', views.sala_list, name='sala_list'),
    path('salas/<int:pk>/', views.sala_detail, name='sala_detail'),
    path('salas/new/', views.sala_create, name='sala_create'),
    path('salas/<int:pk>/edit/', views.sala_update, name='sala_update'),
    path('salas/<int:pk>/delete/', views.sala_delete, name='sala_delete'),

    path('horarios/', views.horario_list, name='horario_list'),
    path('horarios/<int:pk>/', views.horario_detail, name='horario_detail'),
    path('horarios/new/', views.horario_create, name='horario_create'),
    path('horarios/<int:pk>/edit/', views.horario_update, name='horario_update'),
    path('horarios/<int:pk>/delete/', views.horario_delete, name='horario_delete'),

    path('status-agendamento/', views.status_agendamento_list, name='status_agendamento_list'),
    path('status-agendamento/<int:pk>/', views.status_agendamento_detail, name='status_agendamento_detail'),
    path('status-agendamento/new/', views.status_agendamento_create, name='status_agendamento_create'),
    path('status-agendamento/<int:pk>/edit/', views.status_agendamento_update, name='status_agendamento_update'),
    path('status-agendamento/<int:pk>/delete/', views.status_agendamento_delete, name='status_agendamento_delete'),

    path('agendamentos/', views.agendamento_list, name='agendamento_list'),
    path('agendamentos/<uuid:pk>/', views.agendamento_detail, name='agendamento_detail'),
    path('agendamentos/new/', views.agendamento_create, name='agendamento_create'),
    path('agendamentos/<uuid:pk>/edit/', views.agendamento_update, name='agendamento_update'),
    path('agendamentos/<uuid:pk>/delete/', views.agendamento_delete, name='agendamento_delete'),

    path('calendario/', views.calendario_view, name='calendario_view'),
    path('eventos-calendario/', views.get_eventos_calendario, name='get_eventos_calendario'),
]