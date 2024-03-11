# <project>/<app>/management/commands/seed.py
from django.core.management.base import BaseCommand
from api_cadastro.models import Sala, Imagem, Instrutor, Materia
from django.core.files.images import ImageFile
from django.core.files import File

# python manage.py seed --mode=refresh

""" Clear all data and creates addresses """
MODE_REFRESH = 'refresh'

""" Clear all data and do not create any object """
MODE_CLEAR = 'clear'

class Command(BaseCommand):
    help = "seed database for testing and development."

    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help="Mode")

    def handle(self, *args, **options):
        self.stdout.write('seeding data...')
        run_seed(self, options['mode'])
        self.stdout.write('done.')


def clear_data():
    """Deletes all the table data"""
    print("Delete Sala instances")
    Sala.objects.all().delete()


def seed_db():
    print("Creating default salas")

    img_prefix = "seed_files"
    
    ca_600 = "Ca600"
    ca_170 = "Ca170"
    ca_140 = "Ca140"

    sala_data_list = [
        {
            "nome_sala": "Lab. DS 1",
            "predio_sala": ca_600,
            "localizacao_sala": "Térreo",
            "capacidade": 19,
            "computador": 18,
            "quadro_branco": 0,
            "projetor": 0,
            "televisao": 1,
            "image_files": ["lab_DS1.1.jpg", "lab_DS1.2.jpg"]
        },
        {
            "nome_sala": "Lab. DS 2",
            "predio_sala": ca_600,
            "localizacao_sala": "Térreo",
            "capacidade": 19,
            "computador": 18,
            "quadro_branco": 0,
            "projetor": 0,
            "televisao": 1,
            "image_files": ["lab_DS2.1.jpg", "lab_DS2.2.jpg"]
        },
        {
            "nome_sala": "Lab. DS 3",
            "predio_sala": ca_600,
            "localizacao_sala": "Térreo",
            "capacidade": 25,
            "computador": 18,
            "quadro_branco": 0,
            "projetor": 0,
            "televisao": 1,
            "image_files": ["lab_DS3.1.jpg", "lab_DS3.2.png"]
        },
        {
            "nome_sala": "Lab. DS ETS",
            "predio_sala": ca_170,
            "localizacao_sala": "Sub solo",
            "capacidade": 19,
            "computador": 18,
            "quadro_branco": 1,
            "projetor": 0,
            "televisao": 1,
            "image_files": ["lab_ets1.jpg", "lab_ets2.jpg"]
        },
        {
            "nome_sala": "Lab. Eletrônica",
            "predio_sala": ca_170,
            "localizacao_sala": "Sub solo",
            "capacidade": 17,
            "computador": 16,
            "quadro_branco": 0,
            "projetor": 0,
            "televisao": 1,
            "image_files": ["lab_eletronica1.jpg", "lab_eletronica2.jpg"]
        },
        {
            "nome_sala": "Sala de Reunião",
            "predio_sala": ca_170,
            "localizacao_sala": "Sub solo",
            "capacidade": 8,
            "computador": 0,
            "quadro_branco": 0,
            "projetor": 0,
            "televisao": 1,
            "image_files": ["sala_reuniao1.jpg", "sala_reuniao2.jpg"]
        },
        {
            "nome_sala": "Sala Verde",
            "predio_sala": ca_140,
            "localizacao_sala": "Sub solo",
            "capacidade": 19,
            "computador": 0,
            "quadro_branco": 1,
            "projetor": 4,
            "televisao": 1,
            "image_files": ["sala_verde1.jpg", "sala_verde2.jpg"]
        },
        {
            "nome_sala": "Sala Amarela",
            "predio_sala": ca_140,
            "localizacao_sala": "Sub solo",
            "capacidade": 19,
            "computador": 0,
            "quadro_branco": 1,
            "projetor": 0,
            "televisao": 1,
            "image_files": ["sala_amarela1.jpg", "sala_amarela2.jpg"]
        }
    ]

    for sala_data in sala_data_list:
        sala = Sala(
            nome_sala=sala_data["nome_sala"],
            predio_sala=sala_data["predio_sala"],
            localizacao_sala=sala_data["localizacao_sala"],
            capacidade=sala_data["capacidade"],
            computador=sala_data["computador"],
            quadro_branco=sala_data["quadro_branco"],
            projetor=sala_data["projetor"],
            televisao=sala_data["televisao"]
        )
        sala.save()
        
        for image_file in sala_data["image_files"]:
            img = Imagem(
                sala=sala,
                Imagem=ImageFile(open(f'{img_prefix}/{image_file}', "rb"), name=image_file)
            )
            img.save()

        print("{} sala created.".format(sala))


    
    # -- Instrutores seed

    instructors = {
        "Agatha": {
            "EDV": "92900903",
            "Color": "#E552DA",
            "Disciplines": [
                "Java",
                "Office",
                "fundamentos de programação",
                "Redes",
                "versionamento"
            ],
            "Email": "agatha.freitas@br.bosch.com"
        },
        "Camilla": {
            "EDV": "92902256",
            "Color": "#C1C7CC",
            "Disciplines": [
                "Angular",
                "typescript",
                "inglês",
                "QA",
                "SolidWorks",
                "power Bi",
                "office",
                "excel",
                "VBA"
            ],
            "Email": "camila.gomes@br.bosch.com"
        },
        "Cleber": {
            "EDV": "92896142",
            "Color": "#000000",
            "Disciplines": [
                "Python",
                "RestAPI",
                "Projetos de área",
                "DevOps (DTA)",
                "DataScience Python (DTA)",
                "API",
                "Linux",
                "Bosch Values",
                "desenvolvimento web",
                "Introdução à TI",
                "Mapeamento de processos",
                "business overview",
                "data ingestion"
            ],
            "Email": "cleber.augusto@br.bosch.com"
        },
        "Croda": {
            "EDV": "92686259",
            "Color": "#FF9254",
            "Disciplines": ["oficina"],
            "Email": "tiago.croda@br.bosch.com"
        },
        "Dani": {
            "EDV": "92898522",
            "Color": "#FFCF00",
            "Disciplines": [
                "SAP",
                "Rotina bosch",
                "office",
                "power Bi",
                "My-BUY",
                "I-Star",
                "Justificação de corporate",
                "Entrevista"
            ],
            "Email": "daniele.paz@br.bosch.com"
        },
        "Dona": {
            "EDV": "92882773",
            "Color": "#0096E8",
            "Disciplines": ["reunião", "ferramentas de qualidade"],
            "Email": "henrique.dona@br.bosch.com"
        },
        "Francis": {
            "EDV": "92679258",
            "Color": "#00884A",
            "Disciplines": [
                "SolidWorks",
                "power Bi",
                "VBA",
                "QA",
                "Data Science (DTA)",
                "SAP",
                "NoSQL",
                "SQL advanced",
                "banco de dados",
                "Data Lake",
                "excel",
                "mapeamento de processos",
                "projetos de área",
                "desenho técnico"
            ],
            "Email": "francis.franquini@br.bosch.com"
        },
        "Ianella": {
            "EDV": "92681423",
            "Color": "#ED0007",
            "Disciplines": [
                "comunicação e expressão",
                "eletroeletrônica"
            ],
            "Email": "edmar.ianella@br.bosch.com"
        },
        "Leonardo": {
            "EDV": "92897634",
            "Color": "#791D73",
            "Disciplines": [
                "Java",
                "Projetos de área",
                "java Spring",
                "mobile android",
                "android flutter",
                "qualidade",
                "service now (DTA)",
                "CI/CD",
                "Java hibernate",
                "spring boot",
                "versionamento"
            ],
            "Email": "leonardo.oliveira3@br.bosch.com"
        },
        "Luca": {
            "EDV": "92900978",
            "Color": "#00629A",
            "Disciplines": [
                "IoT",
                "inglês",
                "Office",
                "fundamentos de programação",
                "5S",
                "introdução à TI",
                "projetos de área",
                "indústria 4.0"
            ],
            "Email": "luca.dias@br.bosch.com"
        },
        "Roberta": {
            "EDV": "92890918",
            "Color": "#FFD9D9",
            "Disciplines": ["5S", "comunicação e expressão"],
            "Email": "roberta.costa@br.bosch.com"
        },
        "Vanessa": {
            "EDV": "92898970",
            "Color": "#71767C",
            "Disciplines": [
                "Inglês",
                "design thinking",
                "UI/UX (DTA)",
                "fundamentos ágeis",
                "projeto de área",
                "Fundamentos UX",
                "Bosch values",
                "business overview"
            ],
            "Email": "vanessa.silva@br.bosch.com"
        },
        "Wilson": {
            "EDV": "92898478",
            "Color": "#66B8B2",
            "Disciplines": [
                "Office",
                "networking overviwer",
                "data security",
                "cyber security (DTA)",
                "python",
                "inglês",
                "fundamentos de programação",
                "matemática",
                "física",
                "ferramentas da qualidade"
            ],
            "Email": "vinicius.ferreira@br.bosch.com"
        }
    }


    for name, data in instructors.items():
        ins = Instrutor(
            nome=name,
            edv=data["EDV"],
            email=data["Email"],
            cor=data["Color"]
        )
        ins.save()
        for discipline in data["Disciplines"]:
            Materia(
                nome=discipline,
                instrutor=ins
            ).save()
    

def run_seed(self, mode):
    """ Seed database based on mode

    :param mode: refresh / clear 
    :return:
    """
    # Clear data from tables
    clear_data()
    if mode == MODE_CLEAR:
        return

    seed_db()