from django.contrib import admin
from .models import Produto, Movimentacao


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    search_fields = ('nome',)


@admin.register(Movimentacao)
class MovimentacaoAdmin(admin.ModelAdmin):
    search_fields = ('produto',)
