# forms.py
from django import forms


class BarcodeForm(forms.Form):
    codigo = forms.CharField(
        label="Escaneie o código de barras",
        widget=forms.TextInput(attrs={
            "autofocus": "autofocus",
        })
    )
    quantidade = forms.IntegerField(
        initial=1,
        min_value=1,
    )
