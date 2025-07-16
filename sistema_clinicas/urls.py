"""
URL configuration for sistema_clinicas project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'), name='home'), # Página inicial
    path('', include('common.urls')),
    path('pacientes/', include('paciente.urls')),
    path('estoque/', include('estoque.urls')),
    path('usuarios/', include('usuario.urls')),
    path('clinicas/', include('clinica.urls')),
    path('agendamento/', include('agendamento.urls')),
    path('prontuario/', include('prontuario.urls')),
    path('fila/', include('fila.urls')),
    path('atendimento/', include('atendimento.urls')),
    path('api/', include('api.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
