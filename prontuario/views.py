
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required
from .models import Prontuario, AnexoProntuario, VersaoProntuario
from .forms import ProntuarioForm, AnexoProntuarioForm, VersaoProntuarioForm

# Views para Prontuario
def prontuario_list(request):
    prontuarios = Prontuario.objects.all()
    return render(request, 'prontuario/prontuario_list.html', {'prontuarios': prontuarios})

def prontuario_detail(request, pk):
    prontuario = get_object_or_404(Prontuario, pk=pk)
    return render(request, 'prontuario/prontuario_detail.html', {'prontuario': prontuario})

@permission_required('usuario.can_manage_prontuario')
def prontuario_create(request):
    if request.method == 'POST':
        form = ProntuarioForm(request.POST)
        if form.is_valid():
            prontuario = form.save()
            return redirect('prontuario_detail', pk=prontuario.pk)
    else:
        form = ProntuarioForm()
    return render(request, 'prontuario/prontuario_form.html', {'form': form, 'action': 'Criar'})

@permission_required('usuario.can_manage_prontuario')
def prontuario_update(request, pk):
    prontuario = get_object_or_404(Prontuario, pk=pk)
    if request.method == 'POST':
        form = ProntuarioForm(request.POST, instance=prontuario)
        if form.is_valid():
            prontuario = form.save()
            return redirect('prontuario_detail', pk=prontuario.pk)
    else:
        form = ProntuarioForm(instance=prontuario)
    return render(request, 'prontuario/prontuario_form.html', {'form': form, 'action': 'Atualizar'})

@permission_required('usuario.can_manage_prontuario')
def prontuario_delete(request, pk):
    prontuario = get_object_or_404(Prontuario, pk=pk)
    if request.method == 'POST':
        prontuario.delete()
        return redirect('prontuario_list')
    return render(request, 'prontuario/prontuario_confirm_delete.html', {'prontuario': prontuario})

# Views para AnexoProntuario
@permission_required('usuario.can_manage_prontuario')
def anexo_prontuario_create(request, prontuario_pk):
    prontuario = get_object_or_404(Prontuario, pk=prontuario_pk)
    if request.method == 'POST':
        form = AnexoProntuarioForm(request.POST, request.FILES)
        if form.is_valid():
            anexo = form.save(commit=False)
            anexo.prontuario = prontuario
            anexo.save()
            return redirect('prontuario_detail', pk=prontuario.pk)
    else:
        form = AnexoProntuarioForm(initial={'prontuario': prontuario})
    return render(request, 'prontuario/anexo_prontuario_form.html', {'form': form, 'prontuario': prontuario, 'action': 'Adicionar'})

@permission_required('usuario.can_manage_prontuario')
def anexo_prontuario_update(request, pk):
    anexo = get_object_or_404(AnexoProntuario, pk=pk)
    if request.method == 'POST':
        form = AnexoProntuarioForm(request.POST, request.FILES, instance=anexo)
        if form.is_valid():
            anexo = form.save()
            return redirect('prontuario_detail', pk=anexo.prontuario.pk)
    else:
        form = AnexoProntuarioForm(instance=anexo)
    return render(request, 'prontuario/anexo_prontuario_form.html', {'form': form, 'anexo': anexo, 'action': 'Atualizar'})

@permission_required('usuario.can_manage_prontuario')
def anexo_prontuario_delete(request, pk):
    anexo = get_object_or_404(AnexoProntuario, pk=pk)
    prontuario_pk = anexo.prontuario.pk
    if request.method == 'POST':
        anexo.delete()
        return redirect('prontuario_detail', pk=prontuario_pk)
    return render(request, 'prontuario/anexo_prontuario_confirm_delete.html', {'anexo': anexo})

# Views para VersaoProntuario
@permission_required('usuario.can_manage_prontuario')
def versao_prontuario_create(request, prontuario_pk):
    prontuario = get_object_or_404(Prontuario, pk=prontuario_pk)
    if request.method == 'POST':
        form = VersaoProntuarioForm(request.POST)
        if form.is_valid():
            versao = form.save(commit=False)
            versao.prontuario = prontuario
            versao.save()
            return redirect('prontuario_detail', pk=prontuario.pk)
    else:
        form = VersaoProntuarioForm(initial={'prontuario': prontuario})
    return render(request, 'prontuario/versao_prontuario_form.html', {'form': form, 'prontuario': prontuario, 'action': 'Adicionar'})

@permission_required('usuario.can_manage_prontuario')
def versao_prontuario_update(request, pk):
    versao = get_object_or_404(VersaoProntuario, pk=pk)
    if request.method == 'POST':
        form = VersaoProntuarioForm(request.POST, instance=versao)
        if form.is_valid():
            versao = form.save()
            return redirect('prontuario_detail', pk=versao.prontuario.pk)
    else:
        form = VersaoProntuarioForm(instance=versao)
    return render(request, 'prontuario/versao_prontuario_form.html', {'form': form, 'versao': versao, 'action': 'Atualizar'})

@permission_required('usuario.can_manage_prontuario')
def versao_prontuario_delete(request, pk):
    versao = get_object_or_404(VersaoProntuario, pk=pk)
    prontuario_pk = versao.prontuario.pk
    if request.method == 'POST':
        versao.delete()
        return redirect('prontuario_detail', pk=prontuario_pk)
    return render(request, 'prontuario/versao_prontuario_confirm_delete.html', {'versao': versao})
