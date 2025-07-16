from django.urls import path
from . import views

urlpatterns = [
    path('clinicas/', views.clinica_list, name='clinica_list'),
    path('clinicas/<int:pk>/', views.clinica_detail, name='clinica_detail'),
    path('clinicas/new/', views.clinica_create, name='clinica_create'),
    path('clinicas/<int:pk>/edit/', views.clinica_update, name='clinica_update'),
    path('clinicas/<int:pk>/delete/', views.clinica_delete, name='clinica_delete'),
]