
from decimal import Decimal, InvalidOperation
from datetime import datetime

from consultar_tarifa import buscar_tarifa
from eficiencia_energetica import simular_eficiencia
from energia_solar import simular_energia_solar
from comparar_alternativas import comparar_alternativas


def coletar_dados():
    print("\n=== DIAGNÓSTICO ENERGÉTICO RESIDENCIAL ===")

    distribuidora = input("Distribuidora de energia: ").strip()

    try:
        consumo = Decimal(
            input("Consumo mensal (kWh): ").replace(",", ".")
        )

        valor_conta = Decimal(
            input("Valor total da conta (R$): ").replace(",", ".")
        )

    except InvalidOperation:
        print("\nErro: informe valores numéricos válidos.")
        return None

    mes_referencia = input("Mês de referência (MM/AAAA): ").strip()

    if not distribuidora or consumo <= 0 or valor_conta <= 0:
        print("\nErro: preencha os campos corretamente.")
        return None

    try:
        datetime.strptime(mes_referencia, "%m/%Y")
    except ValueError:
        print("\nErro: utilize o formato MM/AAAA.")
        return None

    return {
        "distribuidora": distribuidora,
        "consumo_kwh": consumo,
        "valor_conta": valor_conta,
        "mes_referencia": mes_referencia
    }


def realizar_diagnostico(dados):
    tarifa = buscar_tarifa(dados["distribuidora"])

    if tarifa is None:
        print("\nDistribuidora não encontrada na base de tarifas.")
        return

    consumo = dados["consumo_kwh"]
    tarifa_total = tarifa["tarifa_total"]

    custo_estimado = consumo * tarifa_total

    print("\n=== RESULTADO DO DIAGNÓSTICO ===")
    print(f"Distribuidora: {tarifa['distribuidora']}")
    print(f"Referência: {dados['mes_referencia']}")
    print(f"Consumo mensal: {consumo:.2f} kWh")
    print(f"Valor total da conta: R$ {dados['valor_conta']:.2f}")

    print("\n=== TARIFA DE ENERGIA ===")
    print(f"TE: R$ {tarifa['tarifa_te']:.5f}/kWh")
    print(f"TUSD: R$ {tarifa['tarifa_tusd']:.5f}/kWh")
    print(f"TE + TUSD: R$ {tarifa_total:.5f}/kWh")
    print(
        f"Vigência: {tarifa['vigencia_inicio']} "
        f"até {tarifa['vigencia_fim']}"
    )

    print("\n=== ESTIMATIVA DE CUSTO ===")
    print(f"Custo estimado de TE + TUSD: R$ {custo_estimado:.2f}")

    print("\nObservação:")
    print("O custo estimado considera apenas TE e TUSD.")
    print("O valor total da conta pode incluir impostos,")
    print("bandeiras tarifárias, encargos e outros componentes.")

    cenarios_eficiencia = simular_eficiencia(
        consumo,
        tarifa_total
    )

    print("\n=== ENERGIA SOLAR FOTOVOLTAICA ===")

    resultado_solar = simular_energia_solar(consumo)

    print(
        f"Potência estimada do sistema: "
        f"{resultado_solar['potencia_kwp']:.2f} kWp"
    )
    print(
        f"Geração mensal estimada: "
        f"{resultado_solar['geracao_mensal']:.2f} kWh"
    )
    print(
        f"Geração anual estimada: "
        f"{resultado_solar['geracao_anual']:.2f} kWh"
    )

    print("\nObservação:")
    print("O dimensionamento solar utiliza parâmetros estimados.")
    print("A geração real depende das condições de instalação.")
    print("A geração estimada não representa economia financeira integral.")

    comparar_alternativas(
        consumo,
        tarifa_total,
        cenarios_eficiencia,
        resultado_solar
    )


def main():
    dados = coletar_dados()

    if dados:
        realizar_diagnostico(dados)


if __name__ == "__main__":
    main()
