from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import PrioridadeFila, FilaEspera
from .forms import PrioridadeFilaForm, FilaEsperaForm

# Views para PrioridadeFila
def prioridade_fila_list(request):
    prioridades = PrioridadeFila.objects.all()
    return render(request, 'fila/prioridade_fila_list.html', {'prioridades': prioridades})

def prioridade_fila_detail(request, pk):
    prioridade = get_object_or_404(PrioridadeFila, pk=pk)
    return render(request, 'fila/prioridade_fila_detail.html', {'prioridade': prioridade})

def prioridade_fila_create(request):
    if request.method == 'POST':
        form = PrioridadeFilaForm(request.POST)
        if form.is_valid():
            prioridade = form.save()
            return redirect('prioridade_fila_detail', pk=prioridade.pk)
    else:
        form = PrioridadeFilaForm()
    return render(request, 'fila/prioridade_fila_form.html', {'form': form, 'action': 'Criar'})

def prioridade_fila_update(request, pk):
    prioridade = get_object_or_404(PrioridadeFila, pk=pk)
    if request.method == 'POST':
        form = PrioridadeFilaForm(request.POST, instance=prioridade)
        if form.is_valid():
            prioridade = form.save()
            return redirect('prioridade_fila_detail', pk=prioridade.pk)
    else:
        form = PrioridadeFilaForm(instance=prioridade)
    return render(request, 'fila/prioridade_fila_form.html', {'form': form, 'action': 'Atualizar'})

def prioridade_fila_delete(request, pk):
    prioridade = get_object_or_404(PrioridadeFila, pk=pk)
    if request.method == 'POST':
        prioridade.delete()
        return redirect('prioridade_fila_list')
    return render(request, 'fila/prioridade_fila_confirm_delete.html', {'prioridade': prioridade})

# Views para FilaEspera
def fila_espera_list(request):
    filas = FilaEspera.objects.all()
    return render(request, 'fila/fila_espera_list.html', {'filas': filas})

def fila_espera_detail(request, pk):
    fila = get_object_or_404(FilaEspera, pk=pk)
    return render(request, 'fila/fila_espera_detail.html', {'fila': fila})

def fila_espera_create(request):
    if request.method == 'POST':
        form = FilaEsperaForm(request.POST)
        if form.is_valid():
            fila = form.save()
            return redirect('fila_espera_detail', pk=fila.pk)
    else:
        form = FilaEsperaForm()
    return render(request, 'fila/fila_espera_form.html', {'form': form, 'action': 'Criar'})

def fila_espera_update(request, pk):
    fila = get_object_or_404(FilaEspera, pk=pk)
    if request.method == 'POST':
        form = FilaEsperaForm(request.POST, instance=fila)
        if form.is_valid():
            fila = form.save()
            return redirect('fila_espera_detail', pk=fila.pk)
    else:
        form = FilaEsperaForm(instance=fila)
    return render(request, 'fila/fila_espera_form.html', {'form': form, 'action': 'Atualizar'})

def fila_espera_delete(request, pk):
    fila = get_object_or_404(FilaEspera, pk=pk)
    if request.method == 'POST':
        fila.delete()
        return redirect('fila_espera_list')
    return render(request, 'fila/fila_espera_confirm_delete.html', {'fila': fila})

def chamar_proximo_paciente(request):
    # Lógica para chamar o próximo paciente com base na prioridade e tempo de espera
    # Por simplicidade, aqui apenas pega o primeiro aguardando
    proximo_paciente = FilaEspera.objects.filter(status='aguardando').order_by('prioridade__nivel', 'criado_em').first()
    if proximo_paciente:
        proximo_paciente.status = 'chamado'
        proximo_paciente.chamado_em = timezone.now()
        proximo_paciente.save()
        # Redirecionar para a página de detalhes do paciente ou para uma página de confirmação
        return redirect('fila_espera_detail', pk=proximo_paciente.pk)
    else:
        return render(request, 'fila/no_patient_in_queue.html')