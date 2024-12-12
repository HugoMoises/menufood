from django.contrib import admin
from .models import Marca, Categoria, Produto
# Register your models here.

admin.site.register(Marca)
admin.site.register(Categoria)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'preço')  
    search_fields = ('nome',) 


admin.site.register(Produto, ProdutoAdmin)