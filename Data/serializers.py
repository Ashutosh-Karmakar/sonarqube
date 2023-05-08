from .models import Names
from rest_framework import serializers

#this class helps in converting the attributes in database so that they can be accessed in json format
class NameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Names
        fields = ['name','age']
