
from rest_framework import serializers
from paciente.models import Paciente, ResponsavelLegal, TipoDocumento, DocumentoPaciente, ConsentimentoPaciente

class ResponsavelLegalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResponsavelLegal
        fields = '__all__'

class TipoDocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoDocumento
        fields = '__all__'

class DocumentoPacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentoPaciente
        fields = '__all__'

class ConsentimentoPacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsentimentoPaciente
        fields = '__all__'

class PacienteSerializer(serializers.ModelSerializer):
    responsaveis = ResponsavelLegalSerializer(many=True, read_only=True)
    documentos = DocumentoPacienteSerializer(many=True, read_only=True)
    consentimentos = ConsentimentoPacienteSerializer(many=True, read_only=True)

    class Meta:
        model = Paciente
        fields = (
            'paciente_id', 'nome', 'sobrenome', 'cpf', 'data_nascimento', 'sexo', 
            'endereco', 'telefone', 'email', 'perfil_epidemiologico', 'clinicas',
            'criado_em', 'atualizado_em', 'nome_completo', 'idade',
            'responsaveis', 'documentos', 'consentimentos'
        )
        read_only_fields = ('nome_completo', 'idade')
