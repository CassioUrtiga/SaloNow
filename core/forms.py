from django import forms
from .models import Cliente,Proprietario

class FormularioCliente(forms.ModelForm): 
   class Meta:
        model = Cliente
        fields = ('nome','sobrenome','cpf','email','senha')


class FormularioProprietario(forms.ModelForm):
    class Meta:
        model = Proprietario
        fields = ('nome','sobrenome','cnpj','email','senha')
    


