from django.contrib import admin
from api_cadastro.models import Instrutor, Sala,Imagem, Evento

# Register your models here.

class ImagemInline(admin.TabularInline):
    model = Imagem

@admin.register(Sala)
class SalaAdmin(admin.ModelAdmin):
    inlines = [ImagemInline]

admin.site.register(Imagem)
admin.site.register(Instrutor)

admin.site.register(Evento)