
from decimal import Decimal


PERCENTUAIS_REDUCAO = (
    Decimal("0.05"),
    Decimal("0.10"),
    Decimal("0.15")
)


def calcular_cenarios_eficiencia(consumo_mensal, tarifa_total):
    resultados = []

    for percentual in PERCENTUAIS_REDUCAO:
        consumo_economizado = consumo_mensal * percentual
        novo_consumo = consumo_mensal - consumo_economizado

        economia = consumo_economizado * tarifa_total
        novo_custo = novo_consumo * tarifa_total

        resultados.append({
            "percentual": percentual,
            "consumo_economizado": consumo_economizado,
            "novo_consumo": novo_consumo,
            "novo_custo": novo_custo,
            "economia": economia
        })

    return resultados


def simular_eficiencia(consumo_mensal, tarifa_total):
    custo_atual = consumo_mensal * tarifa_total
    resultados = calcular_cenarios_eficiencia(
        consumo_mensal,
        tarifa_total
    )

    print("\n=== SIMULAÇÃO DE EFICIÊNCIA ENERGÉTICA ===")
    print(f"Consumo atual: {consumo_mensal:.2f} kWh")
    print(f"Custo atual estimado: R$ {custo_atual:.2f}")

    for resultado in resultados:
        percentual = resultado["percentual"]

        print(f"\nRedução de {percentual * 100:.0f}%")
        print(
            f"Consumo economizado: "
            f"{resultado['consumo_economizado']:.2f} kWh"
        )
        print(f"Novo consumo: {resultado['novo_consumo']:.2f} kWh")
        print(f"Novo custo estimado: R$ {resultado['novo_custo']:.2f}")
        print(f"Economia estimada: R$ {resultado['economia']:.2f}")

    print("\nObservação:")
    print("Os percentuais são cenários hipotéticos de redução.")
    print("A economia considera apenas TE e TUSD.")
    print("O projeto não estima o custo das medidas de eficiência.")

    return resultados
