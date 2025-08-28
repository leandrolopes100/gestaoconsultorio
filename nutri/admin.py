from django.contrib import admin
from .models import Consulta, Paciente, Avaliacao

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ("nome", "data_nascimento", "sexo")
    search_fields = ("nome", "sexo")
    list_filter = ("sexo",)
    ordering = ("nome",)


@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    list_display = (
        "paciente",
        "data_consulta",
        "peso",
        "altura",
        "imc",
        "tmb",
        "valor_consulta",
        "consulta_feita"
    )
    list_filter = ("data_consulta",)
    search_fields = ("paciente__nome",)
    ordering = ("-data_consulta",)
    
    # Campos que não podem ser editados
    readonly_fields = ("imc", "tmb", "data_consulta",)

    # Estrutura do formulário no admin
    fieldsets = (
        ("Informações do Paciente", {
            "fields": ("paciente",),
        }),
        ("Dados da Consulta", {
            "fields": ("peso", "altura", "observacoes", "valor_consulta", "consulta_feita"),
        }),
        ("Resultados Automáticos", {
            "fields": ("imc", "tmb"),
        }),
        ("Auditoria", {
            "fields": ("data_consulta",),
        }),
    )

@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    pass