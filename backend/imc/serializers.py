from rest_framework import serializers
from .models import CalculoIMC


class CalculoIMCSerializer(serializers.ModelSerializer):
    """Serializer para o modelo CalculoIMC."""

    class Meta:
        model = CalculoIMC
        fields = ['id', 'peso', 'altura', 'imc', 'classificacao', 'criado_em']
        read_only_fields = ['imc', 'classificacao', 'criado_em']


class CalcularIMCSerializer(serializers.Serializer):
    """Serializer para receber os dados de entrada do cálculo."""

    peso = serializers.FloatField(
        min_value=1,
        max_value=500,
        help_text="Peso em kg (1-500)"
    )
    altura = serializers.FloatField(
        min_value=0.3,
        max_value=3.0,
        help_text="Altura em metros (0.3-3.0)"
    )
