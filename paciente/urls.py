
from django.urls import path
from . import views

urlpatterns = [
    path('pacientes/', views.paciente_list, name='paciente_list'),
    path('pacientes/partial/', views.paciente_list_partial, name='paciente_list_partial'),
    path('pacientes/<uuid:pk>/', views.paciente_detail, name='paciente_detail'),
    path('pacientes/new/', views.paciente_create, name='paciente_create'),
    path('pacientes/<uuid:pk>/edit/', views.paciente_update, name='paciente_update'),
    path('pacientes/<uuid:pk>/delete/', views.paciente_delete, name='paciente_delete'),

    path('pacientes/<uuid:paciente_pk>/responsaveis/new/', views.responsavel_legal_create, name='responsavel_legal_create'),
    path('responsaveis/<uuid:pk>/edit/', views.responsavel_legal_update, name='responsavel_legal_update'),
    path('responsaveis/<uuid:pk>/delete/', views.responsavel_legal_delete, name='responsavel_legal_delete'),

    path('tipos-documento/', views.tipo_documento_list, name='tipo_documento_list'),
    path('tipos-documento/new/', views.tipo_documento_create, name='tipo_documento_create'),
    path('tipos-documento/<int:pk>/edit/', views.tipo_documento_update, name='tipo_documento_update'),
    path('tipos-documento/<int:pk>/delete/', views.tipo_documento_delete, name='tipo_documento_delete'),

    path('pacientes/<uuid:paciente_pk>/documentos/new/', views.documento_paciente_create, name='documento_paciente_create'),
    path('documentos/<uuid:pk>/edit/', views.documento_paciente_update, name='documento_paciente_update'),
    path('documentos/<uuid:pk>/delete/', views.documento_paciente_delete, name='documento_paciente_delete'),

    path('pacientes/<uuid:paciente_pk>/consentimentos/new/', views.consentimento_paciente_create, name='consentimento_paciente_create'),
    path('consentimentos/<int:pk>/edit/', views.consentimento_paciente_update, name='consentimento_paciente_update'),
    path('consentimentos/<int:pk>/delete/', views.consentimento_paciente_delete, name='consentimento_paciente_delete'),
]
