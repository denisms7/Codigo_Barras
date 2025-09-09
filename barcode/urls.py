# urls.py
from django.urls import path
from . import views


urlpatterns = [
    path("", views.Menu.as_view(), name="home"),
    path("leitura/<str:tipo>/", views.LeituraCodigoView.as_view(), name="leitura_codigo"),
    path("finalizar/<str:tipo>/", views.FinalizarMovimentacaoView.as_view(), name="finalizar_movimentacao"),
    path("remover/<int:index>/<str:tipo>/", views.RemoverItemView.as_view(), name="remover_item"),
    path("limpar/<str:tipo>/", views.LimparMovimentosView.as_view(), name="limpar_movimentos"),
]
