# urls.py
from django.urls import path
from . import views


urlpatterns = [
    path("estoque/<str:tipo>/", views.leitura_codigo, name="leitura_codigo"),
    path("estoque/finalizar/<str:tipo>/", views.finalizar_movimentacao, name="finalizar_movimentacao"),
    path("estoque/remover/<int:index>/<str:tipo>/", views.remover_item, name="remover_item"),
]
