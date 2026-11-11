
from decimal import Decimal


HORAS_SOL_PLENO = Decimal("5")
FATOR_DESEMPENHO = Decimal("0.80")
DIAS_MES = Decimal("30")


def calcular_potencia_solar(consumo_mensal):
    potencia = consumo_mensal / (
        HORAS_SOL_PLENO * DIAS_MES * FATOR_DESEMPENHO
    )

    return potencia


def simular_energia_solar(consumo_mensal):
    potencia = calcular_potencia_solar(consumo_mensal)

    geracao_mensal = (
        potencia
        * HORAS_SOL_PLENO
        * DIAS_MES
        * FATOR_DESEMPENHO
    )

    geracao_anual = geracao_mensal * 12

    return {
        "consumo_mensal": consumo_mensal,
        "potencia_kwp": potencia,
        "geracao_mensal": geracao_mensal,
        "geracao_anual": geracao_anual
    }
