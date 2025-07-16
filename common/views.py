
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy

from usuario.models import LogAcesso, LogAuditoria

class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'common/password_change_form.html'
    success_url = reverse_lazy('password_change_done')

class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'common/password_change_done.html'

class CustomPasswordResetView(PasswordResetView):
    template_name = 'common/password_reset_form.html'
    email_template_name = 'common/password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'common/password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'common/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'common/password_reset_complete.html'

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Log de auditoria para login bem-sucedido
                LogAuditoria.objects.create(
                    usuario=user,
                    acao="LOGIN",
                    endereco_ip=request.META.get('REMOTE_ADDR', 'unknown')
                )
                return redirect('home')
            else:
                # Lógica de log de acesso para falha de autenticação (já tratada no backend)
                pass
    else:
        form = AuthenticationForm()
    return render(request, 'common/login.html', {'form': form})

@login_required
def logout_view(request):
    # Log de auditoria para logout
    LogAuditoria.objects.create(
        usuario=request.user,
        acao="LOGOUT",
        endereco_ip=request.META.get('REMOTE_ADDR', 'unknown')
    )
    logout(request)
    return redirect('login')
