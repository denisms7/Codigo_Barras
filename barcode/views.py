# views.py
from django.shortcuts import render, redirect
from .forms import BarcodeForm
from .models import Produto, Movimentacao
from django.contrib import messages


def leitura_codigo(request, tipo="entrada"):
    if request.method == "POST":
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
    else:
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

    return render(request, "leitura.html", {
        "form": form,
        "itens": itens,
        "tipo": tipo,
    })


def finalizar_movimentacao(request, tipo="entrada"):
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
        Movimentacao.objects.create(produto=produto, quantidade=quantidade, tipo=tipo_mov)

    # Limpa sessão
    request.session["movimentos"] = []
    request.session.modified = True
    messages.success(request, "Movimentação finalizada com sucesso!")

    return redirect("leitura_codigo", tipo=tipo)


def remover_item(request, index, tipo="entrada"):
    movimentos = request.session.get("movimentos", [])
    if 0 <= index < len(movimentos):
        movimentos.pop(index)
        request.session["movimentos"] = movimentos
        request.session.modified = True
        messages.success(request, "Item removido da lista.")
    return redirect("leitura_codigo", tipo=tipo)
