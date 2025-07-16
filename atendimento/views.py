from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required
from .models import Atendimento
from .forms import AtendimentoForm

# Views para Atendimento
def atendimento_list(request):
    atendimentos = Atendimento.objects.all()
    return render(request, 'atendimento/atendimento_list.html', {'atendimentos': atendimentos})

def atendimento_detail(request, pk):
    atendimento = get_object_or_404(Atendimento, pk=pk)
    return render(request, 'atendimento/atendimento_detail.html', {'atendimento': atendimento})

@permission_required('usuario.can_attend_clinic')
def atendimento_create(request):
    if request.method == 'POST':
        form = AtendimentoForm(request.POST)
        if form.is_valid():
            atendimento = form.save()
            return redirect('atendimento_detail', pk=atendimento.pk)
    else:
        form = AtendimentoForm()
    return render(request, 'atendimento/atendimento_form.html', {'form': form, 'action': 'Criar'})

@permission_required('usuario.can_attend_clinic')
def atendimento_update(request, pk):
    atendimento = get_object_or_404(Atendimento, pk=pk)
    if request.method == 'POST':
        form = AtendimentoForm(request.POST, instance=atendimento)
        if form.is_valid():
            atendimento = form.save()
            return redirect('atendimento_detail', pk=atendimento.pk)
    else:
        form = AtendimentoForm(instance=atendimento)
    return render(request, 'atendimento/atendimento_form.html', {'form': form, 'action': 'Atualizar'})

@permission_required('usuario.can_attend_clinic')
def atendimento_delete(request, pk):
    atendimento = get_object_or_404(Atendimento, pk=pk)
    if request.method == 'POST':
        atendimento.delete()
        return redirect('atendimento_list')
    return render(request, 'atendimento/atendimento_confirm_delete.html', {'atendimento': atendimento})