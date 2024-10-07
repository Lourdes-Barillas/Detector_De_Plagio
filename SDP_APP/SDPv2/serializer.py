from rest_framework import routers, serializers, viewsets
from .models import documento


""" 
nombreDoc 
estado 
fechaAprobado
enlaceDOI 
fechaPublicado
autor
"""
class docSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = documento
        field = '__all__'