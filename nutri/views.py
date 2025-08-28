from django.urls import reverse_lazy
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from django.db.models import Q
from django.views import View
from django.shortcuts import get_object_or_404, redirect

from .models import Consulta, Paciente, Avaliacao
from .forms import PacienteForm, ConsultaForm, AvaliacaoForm
from django.views.generic import CreateView, DeleteView, UpdateView, DetailView, ListView, View
## --------------------------- PACIENTES ------------------------------------

class PacienteList(ListView):
    model = Paciente
    template_name = "pacientes/lista_pacientes.html"
    context_object_name = 'pacientes'
    paginate_by = 20

    def get_queryset(self):
        queryset = Paciente.objects.all().order_by('nome')  # ordena por nome

        q = self.request.GET.get("q")
        if q:
            queryset = queryset.filter(
                Q(nome__icontains=q) |
                Q(cpf__icontains=q) |
                Q(telefone__icontains=q) 
                
            ).distinct()
        
        return queryset
    
class PacienteCreate(CreateView):
    model = Paciente
    template_name = "pacientes/adicionar_paciente.html"
    form_class = PacienteForm
    success_url = reverse_lazy('pacientes')

class PacienteDelete(DeleteView):
    model = Paciente
    template_name = "pacientes/excluir_paciente.html"
    success_url = reverse_lazy('pacientes')

class PacienteUpdate(UpdateView):
    model = Paciente
    form_class = PacienteForm
    template_name = "pacientes/editar_paciente.html"
    success_url = reverse_lazy('pacientes')

class PacienteDetail(DetailView):
    model = Paciente
    template_name = "pacientes/detalhes_paciente.html"
    
# ------------------------------ CONSULTAS -----------------------------------

class ConsultaList(ListView):
    model = Consulta
    template_name = "consultas/lista_consultas.html"
    context_object_name = 'consultas'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Consulta.objects.all()
        queryset = queryset.order_by('consulta_feita', '-data_consulta')
        
        q = self.request.GET.get("q")
        if q:
            queryset = queryset.filter(
                Q(paciente__nome__icontains=q) |
                Q(data_consulta__date__icontains=q)
            )
        return queryset

class ConsultaCreate(CreateView):
    model = Consulta
    template_name = "consultas/adicionar_consulta.html"
    form_class = ConsultaForm
    success_url = reverse_lazy('consultas')

class ConsultaDetail(DetailView):
    model = Consulta
    template_name = "consultas/detalhes_consulta.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        consulta = self.get_object()
        # traz todas as consultas do mesmo paciente ordenadas por data
        context["consultas"] = consulta.paciente.consultas.order_by("data_consulta") 
        return context

class ConsultaDelete(DeleteView):
    model = Consulta
    template_name = "consultas/excluir_consulta.html"
    success_url = reverse_lazy('consultas')

class ConsultaUpdate(UpdateView):
    model = Consulta
    template_name = "consultas/editar_consulta.html"
    fields = ['data_consulta','peso', 'altura', 'valor_consulta', 'observacoes',]
    success_url = reverse_lazy('consultas')

class MarcarComoFeita(View): 
    def post(self, request, consulta_id):
        consulta = get_object_or_404(Consulta, id=consulta_id)
        consulta.consulta_feita = True
        consulta.save()
        return redirect('consultas')

# ------------------------------ AVALIAÇÃO -----------------------------------

class AvaliacaoCreateView(CreateView):
    model = Avaliacao
    form_class = AvaliacaoForm
    template_name = 'avaliacao/criar_avaliacao.html'
    success_url = reverse_lazy('consultas')

    def dispatch(self, request, *args, **kwargs):
        # Pega a consulta
        self.consulta = get_object_or_404(Consulta, id=kwargs['consulta_id'])

        # Verifica se já existe avaliação para essa consulta
        if self.consulta.avaliacoes.exists():
            return redirect('detalhes_consulta', pk=self.consulta.id)

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Listas de campos para o template
        context['campos_dobras'] = [
            "peito", "abdomen", "iliaca", "axilar_media",
            "coxas", "triceps", "escapula"
        ]
        context['campos_circunferencias'] = [
            "circunf_peitoral", "circunf_cintura", "circunf_abdomen",
            "circunf_biceps_dir", "circunf_biceps_esq",
            "circunf_antebraco_dir", "circunf_antebraco_esq",
            "circunf_quadril", "circunf_coxa_dir", "circunf_coxa_esq",
            "circunf_pant_dir", "circunf_pant_esq"
        ]
        return context

    def form_valid(self, form):
        form.instance.consulta_avaliacao = self.consulta
        response = super().form_valid(form)
        print(f"Avaliação salva com ID {form.instance.id}")  # Debug
        return response

    def form_invalid(self, form):
        print(form.errors)  # mostra erros se houver
        return super().form_invalid(form)
    
    
class AvaliacaoDetail(DetailView):
    model = Avaliacao
    template_name = "avaliacao/detalhes_avaliacao.html"

    def get_object(self, queryset=None):
        consulta_id = self.kwargs.get('consulta_id')
        # Usando o nome real do campo ForeignKey no model
        return get_object_or_404(Avaliacao, consulta_avaliacao_id=consulta_id)
    
class AvaliacaoUpdate(UpdateView):
    model = Avaliacao
    template_name = "avaliacao/editar_avaliacao.html"
    form_class = AvaliacaoForm
    success_url = reverse_lazy('consultas')
    
class AvaliacaoDelete(DeleteView):
    model = Avaliacao
    template_name = "avaliacao/excluir_avaliacao.html"
    def get_success_url(self):
        return reverse_lazy('detalhes_consulta', args=[self.object.consulta_avaliacao.id])

def exportar_avaliacao(request, pk):
    avaliacao = get_object_or_404(Avaliacao, pk=pk)
    consulta = avaliacao.consulta_avaliacao
    paciente = consulta.paciente

    # Cria a resposta HTTP
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="avaliacao_{avaliacao.id}.pdf"'
       # ---------- AQUI DEFINE O NOME DO ARQUIVO ----------
    nome_paciente = paciente.nome.replace(" ", "_")
    data_consulta = consulta.data_consulta.strftime("%d-%m-%Y_%H-%M")
    nome_arquivo = f"avaliacao-consulta-{nome_paciente}-{data_consulta}.pdf"
    response['Content-Disposition'] = f'attachment; filename="{nome_arquivo}"'

    # Criando o PDF
    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4
    y = height - 50

    def escrever_linha(texto, salto=15):
        nonlocal y
        p.drawString(2*cm, y, texto)
        y -= salto

    # Cabeçalho
    p.setFont("Helvetica-Bold", 16)
    escrever_linha("Relatório de Avaliação Física", 30)

    # Dados do paciente
    p.setFont("Helvetica-Bold", 12)
    escrever_linha("Dados do Paciente", 20)
    p.setFont("Helvetica", 11)
    escrever_linha(f"Nome: {paciente.nome}")
    escrever_linha(f"Idade: {paciente.idade} anos")
    escrever_linha(f"Sexo: {paciente.sexo}")
    escrever_linha(f"CPF: {paciente.cpf if paciente.cpf else 'Não informado'}")
    escrever_linha(f"Telefone: {paciente.telefone if paciente.telefone else 'Não informado'}")
    escrever_linha(f"E-mail: {paciente.email if paciente.email else 'Não informado'}")
    escrever_linha(f"Endereço: {paciente.endereco if paciente.endereco else 'Não informado'}")
    escrever_linha(f"Informações adicionais: {paciente.informacoes_adicionais if paciente.informacoes_adicionais else '-'}", 20)

    # Dados da consulta
    p.setFont("Helvetica-Bold", 12)
    escrever_linha("Dados da Consulta", 20)
    p.setFont("Helvetica", 11)
    escrever_linha(f"Data: {consulta.data_consulta.strftime('%d/%m/%Y %H:%M')}")
    escrever_linha(f"Peso: {consulta.peso} kg")
    escrever_linha(f"Altura: {consulta.altura} m")
    escrever_linha(f"IMC: {consulta.imc}")
    escrever_linha(f"TMB: {consulta.tmb}")
    escrever_linha(f"Valor: R$ {consulta.valor_consulta}")
    escrever_linha(f"Consulta feita: {'Sim' if consulta.consulta_feita else 'Não'}")
    escrever_linha(f"Observações: {consulta.observacoes if consulta.observacoes else '-'}", 20)

    # Dobras Cutâneas
    p.setFont("Helvetica-Bold", 12)
    escrever_linha("Dobras Cutâneas (mm)", 20)
    p.setFont("Helvetica", 11)
    for campo in ["peito", "abdomen", "iliaca", "axilar_media", "coxas", "triceps", "escapula"]:
        valor = getattr(avaliacao, campo)
        escrever_linha(f"{campo.replace('_',' ').title()}: {valor if valor is not None else '-'}")

    escrever_linha("", 10)

    # Circunferências
    p.setFont("Helvetica-Bold", 12)
    escrever_linha("Circunferências (cm)", 20)
    p.setFont("Helvetica", 11)
    for campo in [
        "circunf_peitoral", "circunf_cintura", "circunf_abdomen",
        "circunf_biceps_dir", "circunf_biceps_esq",
        "circunf_antebraco_dir", "circunf_antebraco_esq",
        "circunf_quadril", "circunf_coxa_dir", "circunf_coxa_esq",
        "circunf_pant_dir", "circunf_pant_esq"
    ]:
        valor = getattr(avaliacao, campo)
        escrever_linha(f"{campo.replace('_',' ').title()}: {valor if valor is not None else '-'}")

    escrever_linha("", 10)

    # Observações da avaliação
    p.setFont("Helvetica-Bold", 12)
    escrever_linha("Observações da Avaliação", 20)
    p.setFont("Helvetica", 11)
    escrever_linha(avaliacao.observacao_avaliacao if avaliacao.observacao_avaliacao else "-", 15)

    # Finaliza PDF
    p.showPage()
    p.save()

    return response