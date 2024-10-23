from django.contrib import admin
from .models import Marca, Categoria, Produto
# Register your models here.

admin.site.register(Marca)
admin.site.register(Categoria)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'descriçao', 'preço')  # Adicione 'id' aqui
    search_fields = ('nome',)  # Você pode adicionar outros campos que deseja pesquisar

# Registra o modelo no admin com as configurações personalizadas
admin.site.register(Produto, ProdutoAdmin)