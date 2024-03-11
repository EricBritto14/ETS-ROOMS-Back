from django.urls import path, include
from rest_framework import routers
from django.contrib import admin
from api_cadastro.models import *
from api_cadastro.views import *
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()
router.register('instrutor', InstrutorViewset, basename='instrutor')
router.register('sala', SalaViewset, basename='sala')
router.register('evento', EventoViewset, basename='evento')
router.register('imagens', ImagemViewset, basename='imagens')
router.register('materia', MateriaViewset, basename='materia')
router.register('admins', AdminViewset, basename='adminsApp')

urlpatterns = [
                  path('', include(router.urls)),
                  path('admin/', admin.site.urls),
                  path('upload/', UploadView.as_view()),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
