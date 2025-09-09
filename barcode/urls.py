# urls.py
from django.urls import path
from . import views


urlpatterns = [
    path("", views.Menu.as_view(), name="home"),
    path("leitura/", views.LeituraCodigoView.as_view(), name="leitura_codigo"),
    path("finalizar/", views.FinalizarMovimentacaoView.as_view(), name="finalizar_movimentacao"),
    path("remover/<int:index>/", views.RemoverItemView.as_view(), name="remover_item"),
    path("limpar/", views.LimparMovimentosView.as_view(), name="limpar_movimentos"),
]
