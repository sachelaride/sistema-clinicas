
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required
from .models import Paciente, ResponsavelLegal, TipoDocumento, DocumentoPaciente, ConsentimentoPaciente
from .forms import PacienteForm, ResponsavelLegalForm, TipoDocumentoForm, DocumentoPacienteForm, ConsentimentoPacienteForm

def paciente_list(request):
    pacientes = Paciente.objects.all()
    return render(request, 'paciente/paciente_list.html', {'pacientes': pacientes})

def paciente_list_partial(request):
    pacientes = Paciente.objects.all()
    return render(request, 'paciente/includes/paciente_list_content.html', {'pacientes': pacientes})

def paciente_detail(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)
    return render(request, 'paciente/paciente_detail.html', {'paciente': paciente})

def paciente_create(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            paciente = form.save()
            return redirect('paciente_detail', pk=paciente.pk)
    else:
        form = PacienteForm()
    return render(request, 'paciente/paciente_form.html', {'form': form, 'action': 'Criar'})

def paciente_update(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)
    if request.method == 'POST':
        form = PacienteForm(request.POST, instance=paciente)
        if form.is_valid():
            paciente = form.save()
            return redirect('paciente_detail', pk=paciente.pk)
    else:
        form = PacienteForm(instance=paciente)
    return render(request, 'paciente/paciente_form.html', {'form': form, 'action': 'Atualizar'})

def paciente_delete(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)
    if request.method == 'POST':
        paciente.delete()
        return redirect('paciente_list')
    return render(request, 'paciente/paciente_confirm_delete.html', {'paciente': paciente})

# Views para ResponsavelLegal
def responsavel_legal_create(request, paciente_pk):
    paciente = get_object_or_404(Paciente, pk=paciente_pk)
    if request.method == 'POST':
        form = ResponsavelLegalForm(request.POST)
        if form.is_valid():
            responsavel = form.save(commit=False)
            responsavel.paciente = paciente
            responsavel.save()
            return redirect('paciente_detail', pk=paciente.pk)
    else:
        form = ResponsavelLegalForm(initial={'paciente': paciente})
    return render(request, 'paciente/responsavel_legal_form.html', {'form': form, 'paciente': paciente, 'action': 'Adicionar'})

def responsavel_legal_update(request, pk):
    responsavel = get_object_or_404(ResponsavelLegal, pk=pk)
    if request.method == 'POST':
        form = ResponsavelLegalForm(request.POST, instance=responsavel)
        if form.is_valid():
            responsavel = form.save()
            return redirect('paciente_detail', pk=responsavel.paciente.pk)
    else:
        form = ResponsavelLegalForm(instance=responsavel)
    return render(request, 'paciente/responsavel_legal_form.html', {'form': form, 'responsavel': responsavel, 'action': 'Atualizar'})

def responsavel_legal_delete(request, pk):
    responsavel = get_object_or_404(ResponsavelLegal, pk=pk)
    paciente_pk = responsavel.paciente.pk
    if request.method == 'POST':
        responsavel.delete()
        return redirect('paciente_detail', pk=paciente_pk)
    return render(request, 'paciente/responsavel_legal_confirm_delete.html', {'responsavel': responsavel})

# Views para TipoDocumento
def tipo_documento_list(request):
    tipos_documento = TipoDocumento.objects.all()
    return render(request, 'paciente/tipo_documento_list.html', {'tipos_documento': tipos_documento})

def tipo_documento_create(request):
    if request.method == 'POST':
        form = TipoDocumentoForm(request.POST)
        if form.is_valid():
            tipo_documento = form.save()
            return redirect('tipo_documento_list')
    else:
        form = TipoDocumentoForm()
    return render(request, 'paciente/tipo_documento_form.html', {'form': form, 'action': 'Criar'})

def tipo_documento_update(request, pk):
    tipo_documento = get_object_or_404(TipoDocumento, pk=pk)
    if request.method == 'POST':
        form = TipoDocumentoForm(request.POST, instance=tipo_documento)
        if form.is_valid():
            tipo_documento = form.save()
            return redirect('tipo_documento_list')
    else:
        form = TipoDocumentoForm(instance=tipo_documento)
    return render(request, 'paciente/tipo_documento_form.html', {'form': form, 'action': 'Atualizar'})

def tipo_documento_delete(request, pk):
    tipo_documento = get_object_or_404(TipoDocumento, pk=pk)
    if request.method == 'POST':
        tipo_documento.delete()
        return redirect('tipo_documento_list')
    return render(request, 'paciente/tipo_documento_confirm_delete.html', {'tipo_documento': tipo_documento})

# Views para DocumentoPaciente
def documento_paciente_create(request, paciente_pk):
    paciente = get_object_or_404(Paciente, pk=paciente_pk)
    if request.method == 'POST':
        form = DocumentoPacienteForm(request.POST, request.FILES)
        if form.is_valid():
            documento = form.save(commit=False)
            documento.paciente = paciente
            documento.save()
            return redirect('paciente_detail', pk=paciente.pk)
    else:
        form = DocumentoPacienteForm(initial={'paciente': paciente})
    return render(request, 'paciente/documento_paciente_form.html', {'form': form, 'paciente': paciente, 'action': 'Adicionar'})

def documento_paciente_update(request, pk):
    documento = get_object_or_404(DocumentoPaciente, pk=pk)
    if request.method == 'POST':
        form = DocumentoPacienteForm(request.POST, request.FILES, instance=documento)
        if form.is_valid():
            documento = form.save()
            return redirect('paciente_detail', pk=documento.paciente.pk)
    else:
        form = DocumentoPacienteForm(instance=documento)
    return render(request, 'paciente/documento_paciente_form.html', {'form': form, 'documento': documento, 'action': 'Atualizar'})

def documento_paciente_delete(request, pk):
    documento = get_object_or_404(DocumentoPaciente, pk=pk)
    paciente_pk = documento.paciente.pk
    if request.method == 'POST':
        documento.delete()
        return redirect('paciente_detail', pk=paciente_pk)
    return render(request, 'paciente/documento_paciente_confirm_delete.html', {'documento': documento})

# Views para ConsentimentoPaciente
def consentimento_paciente_create(request, paciente_pk):
    paciente = get_object_or_404(Paciente, pk=paciente_pk)
    if request.method == 'POST':
        form = ConsentimentoPacienteForm(request.POST)
        if form.is_valid():
            consentimento = form.save(commit=False)
            consentimento.paciente = paciente
            consentimento.save()
            return redirect('paciente_detail', pk=paciente.pk)
    else:
        form = ConsentimentoPacienteForm(initial={'paciente': paciente})
    return render(request, 'paciente/consentimento_paciente_form.html', {'form': form, 'paciente': paciente, 'action': 'Adicionar'})

def consentimento_paciente_update(request, pk):
    consentimento = get_object_or_404(ConsentimentoPaciente, pk=pk)
    if request.method == 'POST':
        form = ConsentimentoPacienteForm(request.POST, instance=consentimento)
        if form.is_valid():
            consentimento = form.save()
            return redirect('paciente_detail', pk=consentimento.paciente.pk)
    else:
        form = ConsentimentoPacienteForm(instance=consentimento)
    return render(request, 'paciente/consentimento_paciente_form.html', {'form': form, 'consentimento': consentimento, 'action': 'Atualizar'})

def consentimento_paciente_delete(request, pk):
    consentimento = get_object_or_404(ConsentimentoPaciente, pk=pk)
    paciente_pk = consentimento.paciente.pk
    if request.method == 'POST':
        consentimento.delete()
        return redirect('paciente_detail', pk=paciente_pk)
    return render(request, 'paciente/consentimento_paciente_confirm_delete.html', {'consentimento': consentimento})
