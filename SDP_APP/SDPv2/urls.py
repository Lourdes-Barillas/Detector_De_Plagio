from django.urls import path,include
from rest_framework import routers
from SDPv2 import views

router=routers.DefaultRouter()
router.register(r'documentos',views.DocumentoViewSet)

urlpatterns = [
    #path('',include(router.urls))
]