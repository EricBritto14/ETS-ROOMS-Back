from django import forms
from .models import Sala, Imagem

class ImagemForm(forms.ModelForm):
    class Meta:
        model = Imagem
        fields = ['imagem']

class SalaForm(forms.ModelForm):
    imagens = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    class Meta:
        model = Sala
        fields = ['nome_sala', 'imagens']