from rest_framework import viewsets
from api_cadastro.serializers import *
from api_cadastro.models import *
from rest_framework.response import Response
from dateutil.rrule import rrule, DAILY, MONTHLY, WEEKLY
from dateutil.parser import parse
from datetime import datetime
from rest_framework import views, parsers
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
import os
#Criando autenticação com BasicAuthentication do rest_framework

# Create your views here.

def extract_url(image_record):
    return image_record['Imagem']

class MateriaViewset(viewsets.ModelViewSet):
    queryset = Materia.objects.all() #Exibindo todas as matérias
    serializer_class = MateriaSerializer #Código para pegar todas as materias do banco de dados, por causa da linha acima


class InstrutorViewset(viewsets.ModelViewSet):
    queryset = Instrutor.objects.all()  #Exibindo todos os instrutores
    serializer_class = InstrutorSerializer #Código para pegar todas as materias do banco de dados, por causa da linha acima

    def list(self, request):
        queryset = Instrutor.objects.all()

        instrutores = {}

        for instrutor in queryset:
            key = str(instrutor.id_instrutor)
            instrutores[key] = InstrutorSerializer(instrutor).data
            materias_qset = Materia.objects.filter(instrutor=instrutor)
            instrutores[key]['materias'] = MateriaSerializer(materias_qset, many=True).data
        
        return Response(list(instrutores.values()))

    def create(self, request, *args, **kwargs):
        materias = request.data['materias']
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instrutor = serializer.save()
        for materia in materias:
            Materia.objects.create(nome=materia, instrutor=instrutor)
        return Response(serializer.data, status=201)

class SalaViewset(viewsets.ModelViewSet):
    queryset = Sala.objects.all()
    serializer_class = SalaSerializer

    def list(self, request):
        queryset = Sala.objects.all()

        salas = {}

        for sala in queryset:
            key = str(sala.id_sala)
            salas[key] = SalaSerializer(sala).data
            imgs_queryset = Imagem.objects.filter(sala=sala)
            salas[key]['images'] = map(extract_url, ImagemSerializer(imgs_queryset, many=True).data)
            
        return Response(list(salas.values()))


class EventoViewset(viewsets.ModelViewSet):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer

    def list(self, request):
        day = request.query_params.get('day')
        if day == None:
            queryset = Evento.objects.all().order_by('-historico')
        else:
            queryset = Evento.objects.filter(data_inicio=day, data_fim=day)

        eventos = []

        for idx, evt in enumerate(queryset):
            data = EventoSerializer(evt).data
            data['instrutor_data'] = InstrutorSerializer(Instrutor.objects.get(pk=data['instrutor'])).data
            data['materia_data'] = MateriaSerializer(Materia.objects.get(pk=data['materia'])).data
            eventos.append(data)

        return Response(eventos)

    def create(self, request, *args, **kwargs):
        try:
            if request.data['recorrencia']:
                try:
                    tipo_recorrencia_str = request.data['tipo_recorrencia']
                    data_inicial_str = request.data['data_inicio']
                    data_final_str = request.data['data_fim']
        
                    data_inicial = parse(data_inicial_str)
                    data_final = parse(data_final_str)
        
                    if tipo_recorrencia_str == 'diaria':
                        regra_recorrente = rrule(DAILY, dtstart=data_inicial, until=data_final)
        
                    elif tipo_recorrencia_str == 'semanal':
                        regra_recorrente = rrule(WEEKLY, dtstart=data_inicial, until=data_final)
        
                    elif tipo_recorrencia_str == 'mensal':
                        regra_recorrente = rrule(MONTHLY, dtstart=data_inicial, until=data_final)
        
                    else:
                        return Response(
                            status=400,
                            data={ "error": "TIPO_RECORRENCIA errado!!" }
                        )
            
                    for data in regra_recorrente:
                        instrutor = Instrutor.objects.get(pk=request.data['instrutor'])
                        materia = Materia.objects.get(pk=request.data['materia'])
                        print("REQUEST DATA", request.data)
                        Evento(
                            instrutor=instrutor,
                            materia=materia,
                            descricao=request.data['descricao'],
                            data_inicio=data,
                            data_fim=data,
                            hora_inicio=datetime.strptime(request.data['hora_inicio'], '%H:%M').time(),
                            hora_fim=datetime.strptime(request.data['hora_fim'], '%H:%M').time(),
                            local=request.data['local'],
                            nome_sala=request.data['nome_sala'],
                        ).save()
        
                    return Response(data={'msg': 'criado com sucesso'})
                except KeyError:
                    return Response(status=400, data={
                        "error": "Os parâmetros 'data_inicial', 'data_final' e 'tipo_recorrencia' são obrigatórios."
                        })
                except Exception as e:
                    print(e)
                    return Response(
                        status=500,
                        data=request.data
                    )
            
            instrutor = Instrutor.objects.get(pk=request.data['instrutor'])
            if instrutor.edv != request.data['edv']:
                return Response({"error": "Edv incorreto"}, status=403)
            
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=201, headers=headers)
        except DateTakenError as e:
            return Response({"error": str(e)}, status=400)



class ImagemViewset(viewsets.ModelViewSet):
    queryset = Imagem.objects.all()
    serializer_class = ImagemSerializer

class UploadView(views.APIView):
    parser_classes = (parsers.MultiPartParser, )

    def post(self, request, format=None):
        sala_id = request.data['sala_id']
        up_file = request.FILES['file']

        sala = Sala.objects.get(pk=sala_id)

        Imagem.objects.create(
            sala=sala,
            Imagem=up_file
        ).save()

        return Response(status=201)

class AdminViewset(viewsets.ModelViewSet):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer