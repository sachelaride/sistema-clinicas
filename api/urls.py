from rest_framework.routers import DefaultRouter
from paciente.api_views import PacienteViewSet, ResponsavelLegalViewSet, TipoDocumentoViewSet, DocumentoPacienteViewSet, ConsentimentoPacienteViewSet
from estoque.api_views import FornecedorViewSet, LocalizacaoEstoqueViewSet, ProdutoViewSet, LoteProdutoViewSet, PedidoCompraViewSet, ItemPedidoCompraViewSet, MovimentoEstoqueViewSet, AjusteEstoqueViewSet
from usuario.api_views import UsuarioViewSet, PerfilAlunoViewSet, AtividadeAlunoViewSet, LogAcessoViewSet, LogAuditoriaViewSet
from clinica.api_views import ClinicaViewSet
from agendamento.api_views import ServicoViewSet, SalaViewSet, HorarioViewSet, StatusAgendamentoViewSet, AgendamentoViewSet
from prontuario.api_views import ProntuarioViewSet, AnexoProntuarioViewSet, VersaoProntuarioViewSet
from fila.api_views import PrioridadeFilaViewSet, FilaEsperaViewSet
from atendimento.api_views import AtendimentoViewSet

router = DefaultRouter()
router.register(r'pacientes', PacienteViewSet)
router.register(r'responsaveis', ResponsavelLegalViewSet)
router.register(r'tipos-documento', TipoDocumentoViewSet)
router.register(r'documentos', DocumentoPacienteViewSet)
router.register(r'consentimentos', ConsentimentoPacienteViewSet)

router.register(r'fornecedores', FornecedorViewSet)
router.register(r'localizacoes-estoque', LocalizacaoEstoqueViewSet)
router.register(r'produtos', ProdutoViewSet)
router.register(r'lotes-produto', LoteProdutoViewSet)
router.register(r'pedidos-compra', PedidoCompraViewSet)
router.register(r'itens-pedido-compra', ItemPedidoCompraViewSet)
router.register(r'movimentos-estoque', MovimentoEstoqueViewSet)
router.register(r'ajustes-estoque', AjusteEstoqueViewSet)

router.register(r'usuarios', UsuarioViewSet)
router.register(r'perfis-aluno', PerfilAlunoViewSet)
router.register(r'atividades-aluno', AtividadeAlunoViewSet)
router.register(r'logs-acesso', LogAcessoViewSet)
router.register(r'logs-auditoria', LogAuditoriaViewSet)

router.register(r'clinicas', ClinicaViewSet)

router.register(r'servicos', ServicoViewSet)
router.register(r'salas', SalaViewSet)
router.register(r'horarios', HorarioViewSet)
router.register(r'status-agendamento', StatusAgendamentoViewSet)
router.register(r'agendamentos', AgendamentoViewSet)

router.register(r'prontuarios', ProntuarioViewSet)
router.register(r'anexos-prontuario', AnexoProntuarioViewSet)
router.register(r'versoes-prontuario', VersaoProntuarioViewSet)

router.register(r'prioridades-fila', PrioridadeFilaViewSet)
router.register(r'filas-espera', FilaEsperaViewSet)

router.register(r'atendimentos', AtendimentoViewSet)

urlpatterns = router.urls