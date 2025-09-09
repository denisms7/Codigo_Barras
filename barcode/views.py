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

    def get(self, request, *args, **kwargs):
        form = BarcodeForm()
        movimentos = request.session.get("movimentos", [])

        itens = [
            {
                "produto": Produto.objects.get(id=m["produto_id"]),
                "quantidade": m["quantidade"],
            }
            for m in movimentos
        ]

        return render(request, self.template_name, {
            "form": form,
            "itens": itens,
        })

    def post(self, request, *args, **kwargs):
        form = BarcodeForm(request.POST)
        if form.is_valid():
            codigo = form.cleaned_data["codigo"]
            quantidade = form.cleaned_data["quantidade"]

            produto = Produto.objects.filter(codigo_barras=codigo).first()

            if produto:
                item = {
                    "produto_id": produto.id,
                    "quantidade": quantidade,
                }

                if "movimentos" not in request.session:
                    request.session["movimentos"] = []

                movimentos = request.session["movimentos"]

                # Procura se já existe o produto na lista
                for movimento in movimentos:
                    if movimento["produto_id"] == produto.id:
                        movimento["quantidade"] += quantidade
                        break
                else:
                    movimentos.append(item)

                request.session["movimentos"] = movimentos
                request.session.modified = True

                messages.success(request, f"{produto.nome} adicionado com sucesso.")
            else:
                messages.error(request, f"Código {codigo} não encontrado.")

            return redirect("leitura_codigo")

        # Se o form não for válido, renderiza igual ao GET
        return self.get(request, *args, **kwargs)


class FinalizarMovimentacaoView(View):

    def post(self, request, tipo="entrada", *args, **kwargs):
        movimentos = request.session.get("movimentos", [])
        print(movimentos)
        for m in movimentos:
            produto = Produto.objects.get(id=m["produto_id"])
            quantidade = int(m["quantidade"])

            # Salva movimentação
            Movimentacao.objects.create(
                produto=produto,
                quantidade=quantidade,
            )

        # Limpa sessão
        request.session["movimentos"] = []
        request.session.modified = True
        messages.success(request, "Movimentação finalizada com sucesso!")

        return redirect("leitura_codigo")


class RemoverItemView(View):

    def post(self, request, index, *args, **kwargs):
        movimentos = request.session.get("movimentos", [])
        if 0 <= index < len(movimentos):
            movimentos.pop(index)
            request.session["movimentos"] = movimentos
            request.session.modified = True
            messages.success(request, "Item removido da lista.")
        return redirect("leitura_codigo")


class LimparMovimentosView(View):

    def post(self, request, *args, **kwargs):
        request.session["movimentos"] = []
        request.session.modified = True
        messages.success(request, "Todos os produtos foram removidos.")
        return redirect("leitura_codigo")
