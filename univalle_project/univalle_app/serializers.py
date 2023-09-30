from rest_framework import serializers
from .models import Univalluno, ArticuloDeportivo, Prestamo, Multa


class UnivallunoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Univalluno
        fields = '__all__'
        
class ArticuloDeportivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticuloDeportivo
        fields = ('nombre', 'deporte', 'descripcion')

class UnivallunoFullnameSerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField()

    class Meta:
        model = Univalluno
        fields = ('fullname', 'tipo', 'correo')

    def get_fullname(self, obj):
        return f"{obj.nombres} {obj.apellidos}"


class PrestamoSerializer(serializers.ModelSerializer):
    univalluno = UnivallunoSerializer()

    class Meta:
        model = Prestamo
        fields = '__all__'

    def create(self, validated_data):
        univalluno_data = validated_data.pop('univalluno')
        univalluno_instance = Univalluno.objects.create(**univalluno_data)
        
        prestamo = Prestamo.objects.create(univalluno=univalluno_instance, **validated_data)
        return prestamo
        
class MultaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Multa
        fields = '__all__'