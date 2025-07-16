
from django.urls import path
from . import views

urlpatterns = [
    path('atendimentos/', views.atendimento_list, name='atendimento_list'),
    path('atendimentos/<uuid:pk>/', views.atendimento_detail, name='atendimento_detail'),
    path('atendimentos/new/', views.atendimento_create, name='atendimento_create'),
    path('atendimentos/<uuid:pk>/edit/', views.atendimento_update, name='atendimento_update'),
    path('atendimentos/<uuid:pk>/delete/', views.atendimento_delete, name='atendimento_delete'),
]
