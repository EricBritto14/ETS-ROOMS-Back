from django.db import models
from django.core.exceptions import ValidationError
from uuid import uuid4

class DateTakenError(Exception):
    def __init__(self, message):
        self.message = message
        
""" Campo de Informações do modelo

-Email removido a pedido da tay todos foram avisados 14/09/2023 **
-Criei o campo historico para registrar o momento em que foi solicitado 14/09/2023
-Criação do metodo clean e save no modelo Evento para evitar horarios conflitantes entre eventos 26/09/2023

"""

class Instrutor(models.Model):
    id_instrutor = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    nome = models.CharField(max_length=100) 
    edv = models.CharField(max_length=8)
    email = models.CharField(max_length=150)
    cor = models.CharField(max_length=20)

    def __str__(self):
        return "{} {}".format(self.nome, self.cor)

#Classe Materia, mostrando o que quer que salve, e como deve retornar, no caso "self.nome"
class Materia(models.Model):
    nome = models.CharField(max_length=60)
    instrutor = models.ForeignKey(Instrutor, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

class Admin(models.Model):
    edv = models.CharField(max_length=8)
    senha = models.CharField(max_length=20, blank=False)

    def __self__(self):
        return self.edv
    
class Sala(models.Model):
    id_sala = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    nome_sala = models.CharField(max_length=20)
    PREDIO = (
        ('Ca600', 'Ca600'),
        ('Ca170', 'Ca170'),
        ('Ca140', 'Ca140'),
    )
    predio_sala = models.CharField(max_length=5, choices=PREDIO)
    localizacao_sala = models.CharField(max_length=100)
    capacidade = models.IntegerField(default=0)
    computador = models.IntegerField(default=0)
    quadro_branco = models.IntegerField(default=0)
    projetor = models.IntegerField(default=0)
    televisao = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.nome_sala} {self.predio_sala}'
    
class Imagem(models.Model):
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE)
    Imagem = models.ImageField(upload_to='static/img/')

    def __str__(self):
        return f'Imagem da Sala {self.sala.nome_sala}'


class Evento(models.Model):
    id_Evento = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    instrutor = models.ForeignKey(Instrutor, on_delete=models.CASCADE)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)

    descricao = models.CharField(max_length=500)
    data_inicio = models.DateField()  
    data_fim = models.DateField()  
    hora_inicio = models.TimeField()  
    hora_fim = models.TimeField() 
    local = models.CharField(max_length=20)
    nome_sala = models.CharField(max_length=20)
    historico = models.DateTimeField(auto_now=True, editable=False)

    #Metodo clean(Validações personalizada vos dados do modelo (antes de serem salvos))
    def clean(self):
        if self.hora_inicio >= self.hora_fim:
            raise DateTakenError("A hora de início deve ser anterior à hora de término.")

        # Verificando se há conflito de horário com outros eventos no mesmo local e sala
        eventos_conflitantes = Evento.objects.exclude(id_Evento=self.id_Evento).filter(
            data_inicio=self.data_inicio,
            local=self.local,
            nome_sala=self.nome_sala,
            hora_inicio__lt=self.hora_fim,  # O evento existente termina antes do novo evento começar
            hora_fim__gt=self.hora_inicio,   # O evento existente começa depois do novo evento terminar
        )
        if eventos_conflitantes.exists():
            raise DateTakenError("Existe um conflito de horário com outro evento no mesmo local e sala.")

    # Método save (para garantir que as validações no método clean sejam chamadas antes de salvar)
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
   


#------------------------------------------------------------------------------------------------------------#
