
from django.urls import path
from . import views

urlpatterns = [
    path('usuarios/', views.usuario_list, name='usuario_list'),
    path('usuarios/<uuid:pk>/', views.usuario_detail, name='usuario_detail'),
    path('usuarios/new/', views.usuario_create, name='usuario_create'),
    path('usuarios/<uuid:pk>/edit/', views.usuario_update, name='usuario_update'),
    path('usuarios/<uuid:pk>/delete/', views.usuario_delete, name='usuario_delete'),

    path('perfis-aluno/', views.perfil_aluno_list, name='perfil_aluno_list'),
    path('perfis-aluno/<uuid:pk>/', views.perfil_aluno_detail, name='perfil_aluno_detail'),
    path('usuarios/<uuid:usuario_pk>/perfis-aluno/new/', views.perfil_aluno_create, name='perfil_aluno_create'),
    path('perfis-aluno/<uuid:pk>/edit/', views.perfil_aluno_update, name='perfil_aluno_update'),
    path('perfis-aluno/<uuid:pk>/delete/', views.perfil_aluno_delete, name='perfil_aluno_delete'),

    path('atividades-aluno/', views.atividade_aluno_list, name='atividade_aluno_list'),
    path('atividades-aluno/<int:pk>/', views.atividade_aluno_detail, name='atividade_aluno_detail'),
    path('usuarios/<uuid:aluno_pk>/atividades/new/', views.atividade_aluno_create, name='atividade_aluno_create'),
    path('atividades-aluno/<int:pk>/edit/', views.atividade_aluno_update, name='atividade_aluno_update'),
    path('atividades-aluno/<int:pk>/delete/', views.atividade_aluno_delete, name='atividade_aluno_delete'),

    path('logs-acesso/', views.log_acesso_list, name='log_acesso_list'),
    path('logs-acesso/<int:pk>/', views.log_acesso_detail, name='log_acesso_detail'),

    path('logs-auditoria/', views.log_auditoria_list, name='log_auditoria_list'),
    path('logs-auditoria/<int:pk>/', views.log_auditoria_detail, name='log_auditoria_detail'),
]
