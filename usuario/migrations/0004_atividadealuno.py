# Generated by Django 5.2.4 on 2025-07-15 01:47

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinica', '0002_clinica_tipo'),
        ('usuario', '0003_alter_usuario_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='AtividadeAluno',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_atividade', models.CharField(max_length=100)),
                ('descricao', models.TextField(blank=True, null=True)),
                ('data_atividade', models.DateTimeField(auto_now_add=True)),
                ('horas_dedicadas', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('aluno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='atividades', to=settings.AUTH_USER_MODEL)),
                ('clinica', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='clinica.clinica')),
            ],
            options={
                'verbose_name': 'Atividade do Aluno',
                'verbose_name_plural': 'Atividades dos Alunos',
                'ordering': ['-data_atividade'],
            },
        ),
    ]
