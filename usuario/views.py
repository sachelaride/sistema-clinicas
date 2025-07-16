
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import permission_required
from .models import PerfilAluno, LogAcesso, LogAuditoria, AtividadeAluno
from .forms import UsuarioForm, PerfilAlunoForm, LogAcessoForm, LogAuditoriaForm, AtividadeAlunoForm

User = get_user_model()

def usuario_list(request):
    usuarios = User.objects.all()
    return render(request, 'usuario/usuario_list.html', {'usuarios': usuarios})

def usuario_detail(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    return render(request, 'usuario/usuario_detail.html', {'usuario': usuario})

@permission_required('auth.add_user') # Permissão padrão do Django para adicionar usuários
def usuario_create(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            return redirect('usuario_detail', pk=usuario.pk)
    else:
        form = UsuarioForm()
    return render(request, 'usuario/usuario_form.html', {'form': form, 'action': 'Criar'})

@permission_required('auth.change_user') # Permissão padrão do Django para alterar usuários
def usuario_update(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            usuario = form.save()
            return redirect('usuario_detail', pk=usuario.pk)
    else:
        form = UsuarioForm(instance=usuario)
    return render(request, 'usuario/usuario_form.html', {'form': form, 'action': 'Atualizar'})

@permission_required('auth.delete_user') # Permissão padrão do Django para excluir usuários
def usuario_delete(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        usuario.delete()
        return redirect('usuario_list')
    return render(request, 'usuario/usuario_confirm_delete.html', {'usuario': usuario})

def perfil_aluno_list(request):
    perfis_aluno = PerfilAluno.objects.all()
    return render(request, 'usuario/perfil_aluno_list.html', {'perfis_aluno': perfis_aluno})

def perfil_aluno_detail(request, pk):
    perfil_aluno = get_object_or_404(PerfilAluno, pk=pk)
    return render(request, 'usuario/perfil_aluno_detail.html', {'perfil_aluno': perfil_aluno})

@permission_required('usuario.add_perfilaluno')
def perfil_aluno_create(request, usuario_pk):
    usuario = get_object_or_404(User, pk=usuario_pk)
    if request.method == 'POST':
        form = PerfilAlunoForm(request.POST)
        if form.is_valid():
            perfil_aluno = form.save(commit=False)
            perfil_aluno.usuario = usuario
            perfil_aluno.save()
            return redirect('usuario_detail', pk=usuario.pk)
    else:
        form = PerfilAlunoForm(initial={'usuario': usuario})
    return render(request, 'usuario/perfil_aluno_form.html', {'form': form, 'usuario': usuario, 'action': 'Adicionar'})

@permission_required('usuario.change_perfilaluno')
def perfil_aluno_update(request, pk):
    perfil_aluno = get_object_or_404(PerfilAluno, pk=pk)
    if request.method == 'POST':
        form = PerfilAlunoForm(request.POST, instance=perfil_aluno)
        if form.is_valid():
            perfil_aluno = form.save()
            return redirect('usuario_detail', pk=perfil_aluno.usuario.pk)
    else:
        form = PerfilAlunoForm(instance=perfil_aluno)
    return render(request, 'usuario/perfil_aluno_form.html', {'form': form, 'perfil_aluno': perfil_aluno, 'action': 'Atualizar'})

@permission_required('usuario.delete_perfilaluno')
def perfil_aluno_delete(request, pk):
    perfil_aluno = get_object_or_404(PerfilAluno, pk=pk)
    usuario_pk = perfil_aluno.usuario.pk
    if request.method == 'POST':
        perfil_aluno.delete()
        return redirect('usuario_detail', pk=usuario_pk)
    return render(request, 'usuario/perfil_aluno_confirm_delete.html', {'perfil_aluno': perfil_aluno})

# Views para AtividadeAluno
def atividade_aluno_list(request):
    atividades = AtividadeAluno.objects.all()
    return render(request, 'usuario/atividade_aluno_list.html', {'atividades': atividades})

def atividade_aluno_detail(request, pk):
    atividade = get_object_or_404(AtividadeAluno, pk=pk)
    return render(request, 'usuario/atividade_aluno_detail.html', {'atividade': atividade})

@permission_required('usuario.add_atividadealuno')
def atividade_aluno_create(request, aluno_pk):
    aluno = get_object_or_404(User, pk=aluno_pk)
    if request.method == 'POST':
        form = AtividadeAlunoForm(request.POST)
        if form.is_valid():
            atividade = form.save(commit=False)
            atividade.aluno = aluno
            atividade.save()
            return redirect('usuario_detail', pk=aluno.pk)
    else:
        form = AtividadeAlunoForm(initial={'aluno': aluno})
    return render(request, 'usuario/atividade_aluno_form.html', {'form': form, 'aluno': aluno, 'action': 'Adicionar'})

@permission_required('usuario.change_atividadealuno')
def atividade_aluno_update(request, pk):
    atividade = get_object_or_404(AtividadeAluno, pk=pk)
    if request.method == 'POST':
        form = AtividadeAlunoForm(request.POST, instance=atividade)
        if form.is_valid():
            atividade = form.save()
            return redirect('usuario_detail', pk=atividade.aluno.pk)
    else:
        form = AtividadeAlunoForm(instance=atividade)
    return render(request, 'usuario/atividade_aluno_form.html', {'form': form, 'atividade': atividade, 'action': 'Atualizar'})

@permission_required('usuario.delete_atividadealuno')
def atividade_aluno_delete(request, pk):
    atividade = get_object_or_404(AtividadeAluno, pk=pk)
    aluno_pk = atividade.aluno.pk
    if request.method == 'POST':
        atividade.delete()
        return redirect('usuario_detail', pk=aluno_pk)
    return render(request, 'usuario/atividade_aluno_confirm_delete.html', {'atividade': atividade})

def log_acesso_list(request):
    logs_acesso = LogAcesso.objects.all()
    return render(request, 'usuario/log_acesso_list.html', {'logs_acesso': logs_acesso})

def log_acesso_detail(request, pk):
    log_acesso = get_object_or_404(LogAcesso, pk=pk)
    return render(request, 'usuario/log_acesso_detail.html', {'log_acesso': log_acesso})

def log_auditoria_list(request):
    logs_auditoria = LogAuditoria.objects.all()
    return render(request, 'usuario/log_auditoria_list.html', {'logs_auditoria': logs_auditoria})

def log_auditoria_detail(request, pk):
    log_auditoria = get_object_or_404(LogAuditoria, pk=pk)
    return render(request, 'usuario/log_auditoria_detail.html', {'log_auditoria': log_auditoria})
