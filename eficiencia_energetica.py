
from decimal import Decimal


def simular_eficiencia(consumo_mensal, tarifa_total):
    cenarios = [
        Decimal("0.05"),
        Decimal("0.10"),
        Decimal("0.15")
    ]

    custo_atual = consumo_mensal * tarifa_total
    resultados = []

    print("\n=== SIMULAÇÃO DE EFICIÊNCIA ENERGÉTICA ===")
    print(f"Consumo atual: {consumo_mensal:.2f} kWh")
    print(f"Custo atual estimado: R$ {custo_atual:.2f}")

    for percentual in cenarios:
        consumo_economizado = consumo_mensal * percentual
        novo_consumo = consumo_mensal - consumo_economizado

        economia = consumo_economizado * tarifa_total
        novo_custo = novo_consumo * tarifa_total

        resultado = {
            "percentual": percentual,
            "consumo_economizado": consumo_economizado,
            "novo_consumo": novo_consumo,
            "novo_custo": novo_custo,
            "economia": economia
        }

        resultados.append(resultado)

        print(f"\nRedução de {percentual * 100:.0f}%")
        print(f"Consumo economizado: {consumo_economizado:.2f} kWh")
        print(f"Novo consumo: {novo_consumo:.2f} kWh")
        print(f"Novo custo estimado: R$ {novo_custo:.2f}")
        print(f"Economia estimada: R$ {economia:.2f}")

    print("\nObservação:")
    print("Os percentuais são cenários hipotéticos de redução.")
    print("A economia considera apenas TE e TUSD.")

    return resultados
