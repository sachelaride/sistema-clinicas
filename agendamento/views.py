from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import permission_required
from django.http import JsonResponse
from .models import Servico, Sala, Horario, StatusAgendamento, Agendamento
from .forms import ServicoForm, SalaForm, HorarioForm, StatusAgendamentoForm, AgendamentoForm

# Views para Servico
def servico_list(request):
    servicos = Servico.objects.all()
    return render(request, 'agendamento/servico_list.html', {'servicos': servicos})

def servico_detail(request, pk):
    servico = get_object_or_404(Servico, pk=pk)
    return render(request, 'agendamento/servico_detail.html', {'servico': servico})

@permission_required('agendamento.add_servico')
def servico_create(request):
    if request.method == 'POST':
        form = ServicoForm(request.POST)
        if form.is_valid():
            servico = form.save()
            return redirect('servico_detail', pk=servico.pk)
    else:
        form = ServicoForm()
    return render(request, 'agendamento/servico_form.html', {'form': form, 'action': 'Criar'})

@permission_required('agendamento.change_servico')
def servico_update(request, pk):
    servico = get_object_or_404(Servico, pk=pk)
    if request.method == 'POST':
        form = ServicoForm(request.POST, instance=servico)
        if form.is_valid():
            servico = form.save()
            return redirect('servico_detail', pk=servico.pk)
    else:
        form = ServicoForm(instance=servico)
    return render(request, 'agendamento/servico_form.html', {'form': form, 'action': 'Atualizar'})

@permission_required('agendamento.delete_servico')
def servico_delete(request, pk):
    servico = get_object_or_404(Servico, pk=pk)
    if request.method == 'POST':
        servico.delete()
        return redirect('servico_list')
    return render(request, 'agendamento/servico_confirm_delete.html', {'servico': servico})

# Views para Sala
def sala_list(request):
    salas = Sala.objects.all()
    return render(request, 'agendamento/sala_list.html', {'salas': salas})

def sala_detail(request, pk):
    sala = get_object_or_404(Sala, pk=pk)
    return render(request, 'agendamento/sala_detail.html', {'sala': sala})

@permission_required('agendamento.add_sala')
def sala_create(request):
    if request.method == 'POST':
        form = SalaForm(request.POST)
        if form.is_valid():
            sala = form.save()
            return redirect('sala_detail', pk=sala.pk)
    else:
        form = SalaForm()
    return render(request, 'agendamento/sala_form.html', {'form': form, 'action': 'Criar'})

@permission_required('agendamento.change_sala')
def sala_update(request, pk):
    sala = get_object_or_404(Sala, pk=pk)
    if request.method == 'POST':
        form = SalaForm(request.POST, instance=sala)
        if form.is_valid():
            sala = form.save()
            return redirect('sala_detail', pk=sala.pk)
    else:
        form = SalaForm(instance=sala)
    return render(request, 'agendamento/sala_form.html', {'form': form, 'action': 'Atualizar'})

@permission_required('agendamento.delete_sala')
def sala_delete(request, pk):
    sala = get_object_or_404(Sala, pk=pk)
    if request.method == 'POST':
        sala.delete()
        return redirect('sala_list')
    return render(request, 'agendamento/sala_confirm_delete.html', {'sala': sala})

# Views para Horario
def horario_list(request):
    horarios = Horario.objects.all()
    return render(request, 'agendamento/horario_list.html', {'horarios': horarios})

def horario_detail(request, pk):
    horario = get_object_or_404(Horario, pk=pk)
    return render(request, 'agendamento/horario_detail.html', {'horario': horario})

@permission_required('agendamento.add_horario')
def horario_create(request):
    if request.method == 'POST':
        form = HorarioForm(request.POST)
        if form.is_valid():
            horario = form.save()
            return redirect('horario_detail', pk=horario.pk)
    else:
        form = HorarioForm()
    return render(request, 'agendamento/horario_form.html', {'form': form, 'action': 'Criar'})

@permission_required('agendamento.change_horario')
def horario_update(request, pk):
    horario = get_object_or_404(Horario, pk=pk)
    if request.method == 'POST':
        form = HorarioForm(request.POST, instance=horario)
        if form.is_valid():
            horario = form.save()
            return redirect('horario_detail', pk=horario.pk)
    else:
        form = HorarioForm(instance=horario)
    return render(request, 'agendamento/horario_form.html', {'form': form, 'action': 'Atualizar'})

@permission_required('agendamento.delete_horario')
def horario_delete(request, pk):
    horario = get_object_or_404(Horario, pk=pk)
    if request.method == 'POST':
        horario.delete()
        return redirect('horario_list')
    return render(request, 'agendamento/horario_confirm_delete.html', {'horario': horario})

# Views para StatusAgendamento
def status_agendamento_list(request):
    status_agendamentos = StatusAgendamento.objects.all()
    return render(request, 'agendamento/status_agendamento_list.html', {'status_agendamentos': status_agendamentos})

def status_agendamento_detail(request, pk):
    status_agendamento = get_object_or_404(StatusAgendamento, pk=pk)
    return render(request, 'agendamento/status_agendamento_detail.html', {'status_agendamento': status_agendamento})

@permission_required('agendamento.add_statusagendamento')
def status_agendamento_create(request):
    if request.method == 'POST':
        form = StatusAgendamentoForm(request.POST)
        if form.is_valid():
            status_agendamento = form.save()
            return redirect('status_agendamento_detail', pk=status_agendamento.pk)
    else:
        form = StatusAgendamentoForm()
    return render(request, 'agendamento/status_agendamento_form.html', {'form': form, 'action': 'Criar'})

@permission_required('agendamento.change_statusagendamento')
def status_agendamento_update(request, pk):
    status_agendamento = get_object_or_404(StatusAgendamento, pk=pk)
    if request.method == 'POST':
        form = StatusAgendamentoForm(request.POST, instance=status_agendamento)
        if form.is_valid():
            status_agendamento = form.save()
            return redirect('status_agendamento_detail', pk=status_agendamento.pk)
    else:
        form = StatusAgendamentoForm(instance=status_agendamento)
    return render(request, 'agendamento/status_agendamento_form.html', {'form': form, 'action': 'Atualizar'})

@permission_required('agendamento.delete_statusagendamento')
def status_agendamento_delete(request, pk):
    status_agendamento = get_object_or_404(StatusAgendamento, pk=pk)
    if request.method == 'POST':
        status_agendamento.delete()
        return redirect('status_agendamento_list')
    return render(request, 'agendamento/status_agendamento_confirm_delete.html', {'status_agendamento': status_agendamento})

# Views para Agendamento
def agendamento_list(request):
    agendamentos = Agendamento.objects.all()
    return render(request, 'agendamento/agendamento_list.html', {'agendamentos': agendamentos})

def agendamento_detail(request, pk):
    agendamento = get_object_or_404(Agendamento, pk=pk)
    return render(request, 'agendamento/agendamento_detail.html', {'agendamento': agendamento})

@permission_required('usuario.can_schedule_appointment')
def agendamento_create(request):
    if request.method == 'POST':
        form = AgendamentoForm(request.POST)
        if form.is_valid():
            agendamento = form.save()
            return redirect('agendamento_detail', pk=agendamento.pk)
    else:
        form = AgendamentoForm()
    return render(request, 'agendamento/agendamento_form.html', {'form': form, 'action': 'Criar'})

@permission_required('usuario.can_schedule_appointment')
def agendamento_update(request, pk):
    agendamento = get_object_or_404(Agendamento, pk=pk)
    if request.method == 'POST':
        form = AgendamentoForm(request.POST, instance=agendamento)
        if form.is_valid():
            agendamento = form.save()
            return redirect('agendamento_detail', pk=agendamento.pk)
    else:
        form = AgendamentoForm(instance=agendamento)
    return render(request, 'agendamento/agendamento_form.html', {'form': form, 'action': 'Atualizar'})

@permission_required('usuario.can_schedule_appointment')
def agendamento_delete(request, pk):
    agendamento = get_object_or_404(Agendamento, pk=pk)
    if request.method == 'POST':
        agendamento.delete()
        return redirect('agendamento_list')
    return render(request, 'agendamento/agendamento_confirm_delete.html', {'agendamento': agendamento})

# Views para o Calendário
def calendario_view(request):
    return render(request, 'agendamento/calendario.html')

def get_eventos_calendario(request):
    start_str = request.GET.get('start')
    end_str = request.GET.get('end')

    # Converter strings de data para objetos datetime
    start_date = timezone.datetime.fromisoformat(start_str.replace('Z', '+00:00')) if start_str else None
    end_date = timezone.datetime.fromisoformat(end_str.replace('Z', '+00:00')) if end_str else None

    agendamentos = Agendamento.objects.all()
    if start_date and end_date:
        agendamentos = agendamentos.filter(horario__inicio__gte=start_date, horario__fim__lte=end_date)

    eventos = []
    for agendamento in agendamentos:
        # Definir uma cor base para o evento
        color = '#3788d8'  # Cor padrão azul

        # Atribuir cores com base no atendente (aluno/coordenador)
        if agendamento.aluno:
            # Gerar uma cor consistente para cada aluno
            # Isso é um exemplo simples, em produção você pode ter um mapeamento de cores
            color = '#' + str(hash(agendamento.aluno.username) % 0xFFFFFF).zfill(6)
        elif agendamento.coordenador:
            color = '#' + str(hash(agendamento.coordenador.username) % 0xFFFFFF).zfill(6)

        eventos.append({
            'id': str(agendamento.agendamento_id),
            'title': f'{agendamento.paciente.nome_completo} - {agendamento.servico.nome}',
            'start': agendamento.horario.inicio.isoformat(),
            'end': agendamento.horario.fim.isoformat(),
            'color': color, # Cor do evento
            'url': f'/agendamento/agendamentos/{agendamento.agendamento_id}/', # Link para o detalhe do agendamento
        })
    return JsonResponse(eventos, safe=False)