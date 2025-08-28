from django import forms
from .models import Paciente, Consulta, Avaliacao

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['nome', 'cpf', 'data_nascimento', 'sexo', 'telefone', 'email', 'endereco', 'informacoes_adicionais',]
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Nome completo'}),
            'cpf': forms.TextInput(attrs={'placeholder': '000.000.000-00'}),
            'data_nascimento': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'sexo': forms.Select(),
            'telefone': forms.TextInput(attrs={'placeholder': '(00) 00000-0000'}),
            'email': forms.EmailInput(attrs={'placeholder': 'email@exemplo.com'}),
            'endereco': forms.TextInput(attrs={'placeholder': 'Rua, número, bairro, cidade'}),
            'informacoes_adicionais': forms.Textarea(attrs={'placeholder': 'Informações Adicionais do Paciente'}),
        }

class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = ['paciente', 'data_consulta', 'peso', 'altura', 'observacoes', 'valor_consulta',]
        widgets = {
            'paciente': forms.Select(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-400'}),
            'data_consulta': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-400'}),
            'peso': forms.NumberInput(attrs={'placeholder': 'Ex: 70.5', 'step': '0.01', 'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-400'}),
            'altura': forms.NumberInput(attrs={'placeholder': 'Ex: 1.75', 'step': '0.01', 'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-400'}),
            'observacoes': forms.Textarea(attrs={'rows': 3, 'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-400'}),
            'valor_consulta': forms.NumberInput(attrs={'placeholder': 'R$ 0.00', 'step': '0.01', 'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-400'}),
    
        }


    def clean_valor_consulta(self):
        valor = self.cleaned_data.get('valor_consulta')
        if valor is None or valor < 0:
            raise forms.ValidationError("O valor da consulta deve ser maior ou igual a 0.")
        return valor

class AvaliacaoForm(forms.ModelForm):
    class Meta:
        model = Avaliacao
        fields = '__all__'
        