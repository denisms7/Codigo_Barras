# forms.py
from django import forms


class BarcodeForm(forms.Form):
    codigo = forms.CharField(
        required=True,
    )
    quantidade = forms.IntegerField(
        initial=1,
        min_value=1,
        required=True,
    )
