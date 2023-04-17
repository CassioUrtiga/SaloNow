from django import forms
from .models import Cliente,Proprietario

class FormularioCliente(forms.ModelForm):
    nome_completo = forms.CharField(required=True, max_length=100, widget=forms.TextInput(attrs={
        'id': 'nome',
        'class': 'form-control',
        'name': 'nome',
        'placeholder': 'Nome completo',
    }))

    sobrenome = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'id': 'sobrenome',
        'class': 'form-control',
        'name': 'sobrenome',
        'placeholder': 'Sobrenome'
    }))

    username = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={
        'id': 'username',
        'class': 'form-control',
        'name': 'username',
        'placeholder': 'Username'
    }))

    email = forms.EmailField(required=True,widget=forms.TextInput(attrs={
        'id': 'email',
        'class': 'form-control',
        'name': 'email',
        'placeholder': 'E-mail'
    }))

    senha = forms.CharField(min_length=8, max_length=12, required=True ,widget=forms.PasswordInput(attrs={
        'id': 'senha',
        'type': 'password',
        'class': 'form-control',
        'name': 'senha',
        'placeholder': 'Senha'
    }))

    class Meta:
        model = Cliente
        fields = ('nome_completo', 'sobrenome', 'username' ,'email', 'senha')



class FormularioProprietario(forms.ModelForm):
    nome_completo = forms.CharField(required=True, max_length=100, widget=forms.TextInput(attrs={
        'id': 'nome',
        'class': 'form-control',
        'name': 'nome',
        'placeholder': 'Nome completo',
    }))

    sobrenome = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'id': 'sobrenome',
        'class': 'form-control',
        'name': 'sobrenome',
        'placeholder': 'Sobrenome'
    }))

    cnpj = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'id': 'cnpj',
        'class': 'form-control',
        'name': 'cnpj',
        'placeholder': 'CNPJ',
        'data-mask': '00.000.000/0000-00'
    }))

    username = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={
        'id': 'username',
        'class': 'form-control',
        'name': 'username',
        'placeholder': 'Username'
    }))

    email = forms.EmailField(required=True,widget=forms.TextInput(attrs={
        'id': 'email',
        'class': 'form-control',
        'name': 'email',
        'placeholder': 'E-mail'
    }))

    senha = forms.CharField(min_length=8, max_length=12, required=True ,widget=forms.PasswordInput(attrs={
        'id': 'senha',
        'type': 'password',
        'class': 'form-control',
        'name': 'senha',
        'placeholder': 'Senha'
    }))

    class Meta:
        model = Proprietario
        fields = ('nome_completo', 'sobrenome', 'cnpj', 'username', 'email', 'senha')
    


