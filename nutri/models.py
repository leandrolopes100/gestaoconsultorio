from django.db import models
from datetime import date
from django.core.exceptions import ValidationError
from django.utils import timezone
from validate_docbr import CPF
from django.db.models import SET_NULL 
cpf_validator = CPF()


class Paciente(models.Model):
    nome = models.CharField(max_length=150)
    cpf = models.CharField(max_length=14, unique=True, null=True, blank=True)
    data_nascimento = models.DateField()
    sexo = models.CharField(max_length=10, choices=[('M', 'Masculino'), ('F', 'Feminino')])
    telefone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    endereco = models.CharField(max_length=255, null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True, editable=False)
    informacoes_adicionais = models.TextField(blank=True, null=True)

    @property
    def idade(self):
        today = date.today()
        idade = today.year - self.data_nascimento.year
        if (today.month, today.day) < (self.data_nascimento.month, self.data_nascimento.day):
            idade -= 1
        return idade

    # def clean(self):
    #     if self.cpf:
    #         cpf_num = str(self.cpf)
    #         if not cpf_validator.validate(cpf_num):
    #             raise ValidationError("CPF inválido")
    #         self.cpf = cpf_validator.mask(cpf_num)  # formata o CPF

    # def save(self, *args, **kwargs):
    #     self.full_clean()
    #     super().save(*args, **kwargs)

    def __str__(self):
        return self.nome


class Consulta(models.Model): #Apenas criar a consulta
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name="consultas")
    data_consulta = models.DateTimeField()
    peso = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    altura = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)  # metros
    imc = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    tmb = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    observacoes = models.TextField(blank=True, null=True)
    valor_consulta = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, verbose_name="Valor")
    consulta_feita = models.BooleanField(default=False)

    class Meta:
        ordering = ["-data_consulta"] 

    def clean(self):
      if Consulta.objects.filter(paciente=self.paciente, data_consulta=self.data_consulta).exists():
        raise ValidationError("Já existe uma consulta marcada para este paciente neste horário.")

    def calcular_imc(self):
            if self.peso and self.altura:
                return round(float(self.peso) / (float(self.altura) ** 2), 2)
            return None

    def calcular_tmb(self):
        if not self.peso or not self.altura:
            return None

        altura_cm = float(self.altura) * 100
        idade = (timezone.now().date() - self.paciente.data_nascimento).days // 365

        if self.paciente.sexo == 'M':
            return round(88.36 + (13.4 * float(self.peso)) + (4.8 * altura_cm) - (5.7 * idade), 2)
        elif self.paciente.sexo == 'F':
            return round(447.6 + (9.2 * float(self.peso)) + (3.1 * altura_cm) - (4.3 * idade), 2)
        return None

    def save(self, *args, **kwargs):
        self.imc = self.calcular_imc()
        self.tmb = self.calcular_tmb()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Consulta de {self.paciente.nome} - {self.data_consulta.strftime('%d/%m/%Y')}"

class Avaliacao(models.Model):
    consulta_avaliacao = models.ForeignKey(Consulta, on_delete=models.CASCADE, related_name='avaliacoes')
    data_avaliacao = models.DateTimeField(auto_now_add=True)
    #Dobras (mm)
    peito = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Medida Peito")
    abdomen = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Medida Abdomen")
    iliaca = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Medida Ilíaca")
    axilar_media = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Medida Axiliar Média")
    coxas = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Medida Coxas")
    triceps = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Medida Tríceps")
    escapula = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Medida Escápula")

    #circunferencia
    circunf_peitoral = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Circunf Peitoral")
    circunf_cintura = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Circunf Cintura")
    circunf_abdomen = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Circunf Abdomen")
    circunf_biceps_dir = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Circunf Bíceps (Dir.)")
    circunf_biceps_esq = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Circunf Bíceps (Esq.)")
    circunf_antebraco_dir = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Circunf Antebraço (Dir.)")
    circunf_antebraco_esq = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Circunf Antebraço (Esq.)")    
    circunf_quadril  = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Circunf Quadril")
    circunf_coxa_dir = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Circunf Coxa (Dir.)")
    circunf_coxa_esq = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Circunf Coxa (Esq.)")
    circunf_pant_dir = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Circunf Panturrilha (Dir.)")
    circunf_pant_esq = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Circunf Panturrilha (Esq.)")

    observacao_avaliacao = models.TextField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True, editable=False)
    atualizado_em = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return f"Avaliação de {self.consulta_avaliacao}" 