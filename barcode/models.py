# models.py
from django.db import models


class Produto(models.Model):
    nome = models.CharField(max_length=100)
    codigo_barras = models.CharField(max_length=50, unique=True)
    estoque = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.nome} ({self.codigo_barras})"


class Movimentacao(models.Model):
    TIPO_CHOICES = (
        ("entrada", "Entrada"),
        ("saida", "Saída"),
    )
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tipo} - {self.produto.nome} ({self.quantidade})"
