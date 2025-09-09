from django.views import View
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from .forms import BarcodeForm
from .models import Produto, Movimentacao
from django.contrib import messages


class Menu(TemplateView):
    template_name = "menu.html"


class LeituraCodigoView(View):
    template_name = "leitura.html"

    def get(self, request, tipo="entrada", *args, **kwargs):
        form = BarcodeForm()
        movimentos = request.session.get("movimentos", [])

        itens = [
            {
                "produto": Produto.objects.get(id=m["produto_id"]),
                "quantidade": m["quantidade"],
                "tipo": m["tipo"],
            }
            for m in movimentos
        ]

        return render(request, self.template_name, {
            "form": form,
            "itens": itens,
            "tipo": tipo,
        })

    def post(self, request, tipo="entrada", *args, **kwargs):
        form = BarcodeForm(request.POST)
        if form.is_valid():
            codigo = form.cleaned_data["codigo"]
            quantidade = form.cleaned_data["quantidade"]

            produto = Produto.objects.filter(codigo_barras=codigo).first()

            if produto:
                item = {
                    "produto_id": produto.id,
                    "quantidade": quantidade,
                    "tipo": tipo,
                }

                if "movimentos" not in request.session:
                    request.session["movimentos"] = []
                request.session["movimentos"].append(item)
                request.session.modified = True

                messages.success(request, f"{produto.nome} adicionado com sucesso.")
            else:
                messages.error(request, f"Código {codigo} não encontrado.")

            return redirect("leitura_codigo", tipo=tipo)

        # Se o form não for válido, renderiza igual ao GET
        return self.get(request, tipo, *args, **kwargs)


class FinalizarMovimentacaoView(View):

    def post(self, request, tipo="entrada", *args, **kwargs):
        movimentos = request.session.get("movimentos", [])
        for m in movimentos:
            produto = Produto.objects.get(id=m["produto_id"])
            quantidade = int(m["quantidade"])
            tipo_mov = m["tipo"]

            # Atualiza estoque
            if tipo_mov == "entrada":
                produto.estoque += quantidade
            else:
                produto.estoque -= quantidade
            produto.save()

            # Salva movimentação
            Movimentacao.objects.create(
                produto=produto,
                quantidade=quantidade,
                tipo=tipo_mov,
            )

        # Limpa sessão
        request.session["movimentos"] = []
        request.session.modified = True
        messages.success(request, "Movimentação finalizada com sucesso!")

        return redirect("leitura_codigo", tipo=tipo)


class RemoverItemView(View):

    def post(self, request, index, tipo="entrada", *args, **kwargs):
        movimentos = request.session.get("movimentos", [])
        if 0 <= index < len(movimentos):
            movimentos.pop(index)
            request.session["movimentos"] = movimentos
            request.session.modified = True
            messages.success(request, "Item removido da lista.")
        return redirect("leitura_codigo", tipo=tipo)


class LimparMovimentosView(View):

    def post(self, request, tipo="entrada", *args, **kwargs):
        request.session["movimentos"] = []
        request.session.modified = True
        messages.success(request, "Todos os produtos foram removidos.")
        return redirect("leitura_codigo", tipo=tipo)
