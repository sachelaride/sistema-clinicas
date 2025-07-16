
from django.shortcuts import render, redirect, get_object_or_404
from .models import Clinica
from .forms import ClinicaForm

def clinica_list(request):
    clinicas = Clinica.objects.all()
    return render(request, 'clinica/clinica_list.html', {'clinicas': clinicas})

def clinica_detail(request, pk):
    clinica = get_object_or_404(Clinica, pk=pk)
    return render(request, 'clinica/clinica_detail.html', {'clinica': clinica})

def clinica_create(request):
    if request.method == 'POST':
        form = ClinicaForm(request.POST)
        if form.is_valid():
            clinica = form.save()
            return redirect('clinica_detail', pk=clinica.pk)
    else:
        form = ClinicaForm()
    return render(request, 'clinica/clinica_form.html', {'form': form, 'action': 'Criar'})

def clinica_update(request, pk):
    clinica = get_object_or_404(Clinica, pk=pk)
    if request.method == 'POST':
        form = ClinicaForm(request.POST, instance=clinica)
        if form.is_valid():
            clinica = form.save()
            return redirect('clinica_detail', pk=clinica.pk)
    else:
        form = ClinicaForm(instance=clinica)
    return render(request, 'clinica/clinica_form.html', {'form': form, 'action': 'Atualizar'})

def clinica_delete(request, pk):
    clinica = get_object_or_404(Clinica, pk=pk)
    if request.method == 'POST':
        clinica.delete()
        return redirect('clinica_list')
    return render(request, 'clinica/clinica_confirm_delete.html', {'clinica': clinica})
