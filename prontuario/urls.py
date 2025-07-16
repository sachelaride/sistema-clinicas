
from django.urls import path
from . import views

urlpatterns = [
    path('prontuarios/', views.prontuario_list, name='prontuario_list'),
    path('prontuarios/<uuid:pk>/', views.prontuario_detail, name='prontuario_detail'),
    path('prontuarios/new/', views.prontuario_create, name='prontuario_create'),
    path('prontuarios/<uuid:pk>/edit/', views.prontuario_update, name='prontuario_update'),
    path('prontuarios/<uuid:pk>/delete/', views.prontuario_delete, name='prontuario_delete'),

    path('prontuarios/<uuid:prontuario_pk>/anexos/new/', views.anexo_prontuario_create, name='anexo_prontuario_create'),
    path('anexos/<uuid:pk>/edit/', views.anexo_prontuario_update, name='anexo_prontuario_update'),
    path('anexos/<uuid:pk>/delete/', views.anexo_prontuario_delete, name='anexo_prontuario_delete'),

    path('prontuarios/<uuid:prontuario_pk>/versoes/new/', views.versao_prontuario_create, name='versao_prontuario_create'),
    path('versoes/<uuid:pk>/edit/', views.versao_prontuario_update, name='versao_prontuario_update'),
    path('versoes/<uuid:pk>/delete/', views.versao_prontuario_delete, name='versao_prontuario_delete'),
]
