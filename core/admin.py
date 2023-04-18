from django.contrib import admin
from .models import Cliente, Proprietario

# Register your models here.
@admin.register(Cliente)
class ClienteModelAdmin(admin.ModelAdmin):
    list_display = ('nome_completo', 'username', 'email')

    def username(self, obj):
        return obj.user.username

    def email(self, obj):
        return obj.user.email
    
    username.short_description = 'Username'
    email.short_description = 'Email'

@admin.register(Proprietario)
class ProprietarioModelAdmin(admin.ModelAdmin):
    list_display = ('nome_completo', 'username', 'email', 'cnpj')

    def username(self, obj):
        return obj.user.username

    def email(self, obj):
        return obj.user.email
    
    username.short_description = 'Username'
    email.short_description = 'Email'

