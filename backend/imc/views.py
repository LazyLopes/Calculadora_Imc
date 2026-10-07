from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import CalculoIMC
from .serializers import CalcularIMCSerializer, CalculoIMCSerializer


@api_view(['POST'])
def calcular_imc(request):
    """
    Calcula o IMC com base no peso e altura fornecidos.
    Salva o resultado no banco de dados.
    """
    serializer = CalcularIMCSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    peso = serializer.validated_data['peso']
    altura = serializer.validated_data['altura']

    imc, classificacao = CalculoIMC.calcular_imc(peso, altura)

    calculo = CalculoIMC.objects.create(
        peso=peso,
        altura=altura,
        imc=imc,
        classificacao=classificacao,
    )

    resultado = CalculoIMCSerializer(calculo)
    return Response(resultado.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def historico_imc(request):
    """Retorna o histórico dos últimos 10 cálculos de IMC."""
    calculos = CalculoIMC.objects.all()[:10]
    serializer = CalculoIMCSerializer(calculos, many=True)
    return Response(serializer.data)


@api_view(['DELETE'])
def limpar_historico(request):
    """Limpa todo o histórico de cálculos."""
    CalculoIMC.objects.all().delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
