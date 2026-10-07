from django.db import models


class CalculoIMC(models.Model):
    """Modelo para armazenar o histórico de cálculos de IMC."""

    peso = models.FloatField(help_text="Peso em kg")
    altura = models.FloatField(help_text="Altura em metros")
    imc = models.FloatField(help_text="Valor do IMC calculado")
    classificacao = models.CharField(max_length=50, help_text="Classificação do IMC")
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-criado_em']
        verbose_name = 'Cálculo de IMC'
        verbose_name_plural = 'Cálculos de IMC'

    def __str__(self):
        return f"IMC: {self.imc:.1f} - {self.classificacao} ({self.criado_em:%d/%m/%Y %H:%M})"

    @staticmethod
    def calcular_imc(peso: float, altura: float) -> tuple[float, str]:
        """Calcula o IMC e retorna o valor e a classificação."""
        imc = peso / (altura ** 2)
        imc = round(imc, 2)

        if imc < 18.5:
            classificacao = "Abaixo do peso"
        elif imc < 25:
            classificacao = "Peso normal"
        elif imc < 30:
            classificacao = "Sobrepeso"
        elif imc < 35:
            classificacao = "Obesidade Grau I"
        elif imc < 40:
            classificacao = "Obesidade Grau II"
        else:
            classificacao = "Obesidade Grau III"

        return imc, classificacao
