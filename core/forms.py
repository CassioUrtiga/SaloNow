from django import forms
from .models import Cliente, Proprietario, Salon


class FormularioCliente(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ('nome_completo', 'username' ,'email', 'senha', 'foto_perfil', 'cep', 'cidade', 'uf')

    nome_completo = forms.CharField(required=True, max_length=100, widget=forms.TextInput(attrs={
        'id': 'nome',
        'class': 'form-control',
        'name': 'nome',
        'placeholder': 'Nome completo',
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

    cep = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'id': 'cep',
        'class': 'form-control',
        'name': 'cep',
        'placeholder': 'CEP',
        'data-mask': '00000-000'
    }))

    cidade = forms.CharField(required=False, widget=forms.HiddenInput(attrs={
        'name': 'cidade',
        'value': '',
    }))

    uf = forms.CharField(required=False, widget=forms.HiddenInput(attrs={
        'name': 'uf',
        'value': '',
    }))


class FormularioProprietario(forms.ModelForm):
    class Meta:
        model = Proprietario
        fields = ('nome_completo', 'cnpj', 'username', 'email', 'senha', 'foto_perfil')

    nome_completo = forms.CharField(required=True, max_length=100, widget=forms.TextInput(attrs={
        'id': 'nome',
        'class': 'form-control',
        'name': 'nome',
        'placeholder': 'Nome completo',
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

class FormularioSalao(forms.ModelForm):
    class Meta:
        model = Salon
        fields = ('nome_salao', 'descricao', 'salao_image', 'cidade', 'rua', 'pais', 'bairro', 'numero')
    
    nome_salao = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'id': 'salon-name',
        'class': 'form-control',
        'name': 'salon-name',
        'placeholder': 'Nome do salão',
    }))

    descricao = forms.CharField(widget=forms.Textarea(attrs={
        'id': 'desc-salon',
        'class': 'form-control',
        'name': 'desc-salon',
        'placeholder': 'Informe a descrição e caracteríticas do seu salão',
        'rows': 4,
        'cols': 40,
        'style': 'resize: none;'
    }))

    cidade = forms.CharField(max_length=30, widget=forms.TextInput(attrs={
        'id': 'city',
        'class': 'form-control',
        'name': 'city',
        'placeholder': 'Cidade',
    }))

    pais = forms.CharField(max_length=30, widget=forms.TextInput(attrs={
        'id': 'pais',
        'class': 'form-control',
        'name': 'pais',
        'placeholder': 'País',
    }))

    rua = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'id': 'rua',
        'class': 'form-control',
        'name': 'rua',
        'placeholder': 'Rua',
    }))

    bairro = forms.CharField(max_length=30, widget=forms.TextInput(attrs={
        'id': 'bairro',
        'class': 'form-control',
        'name': 'bairro',
        'placeholder': 'Bairro',
    }))

    numero = forms.IntegerField(widget=forms.NumberInput(attrs={
        'id': 'num-salon',
        'class': 'form-control',
        'name': 'num-salon',
        'placeholder': 'Número',
        'min': 0,
        'max': 1000,
        'style': 'width: 6.2em;'
    }))
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['salao_image'].widget.attrs.update({
            'class': 'picture_image',
            'id': 'image'
        })
        