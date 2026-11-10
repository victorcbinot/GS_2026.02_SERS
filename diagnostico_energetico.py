
from decimal import Decimal, InvalidOperation
from datetime import datetime
from eficiencia_energetica import simular_eficiencia

from consultar_tarifa import buscar_tarifa


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

    if not distribuidora:
        print("\nErro: informe a distribuidora.")
        return None

    if consumo <= 0 or valor_conta <= 0:
        print("\nErro: consumo e valor da conta devem ser maiores que zero.")
        return None

    try:
        datetime.strptime(mes_referencia, "%m/%Y")
    except ValueError:
        print("\nErro: informe o mês no formato MM/AAAA.")
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

    custo_estimado = dados["consumo_kwh"] * tarifa["tarifa_total"]

    print("\n=== RESULTADO DO DIAGNÓSTICO ===")

    print(f"Distribuidora: {tarifa['distribuidora']}")
    print(f"Referência: {dados['mes_referencia']}")
    print(f"Consumo mensal: {dados['consumo_kwh']} kWh")
    print(f"Valor total da conta: R$ {dados['valor_conta']:.2f}")

    print("\n=== TARIFA DE ENERGIA ===")

    print(f"TE: R$ {tarifa['tarifa_te']:.5f}/kWh")
    print(f"TUSD: R$ {tarifa['tarifa_tusd']:.5f}/kWh")
    print(f"TE + TUSD: R$ {tarifa['tarifa_total']:.5f}/kWh")

    print("\n=== ESTIMATIVA DE CUSTO ===")

    print(f"Custo estimado de TE + TUSD: R$ {custo_estimado:.2f}")

    print("\nObservação:")
    print("O custo estimado considera apenas TE e TUSD.")
    print("O valor total da conta pode incluir impostos,")
    print("bandeiras tarifárias, encargos e outros componentes.")

    simular_eficiencia(
        dados["consumo_kwh"],
        tarifa["tarifa_total"]
    )

def main():
    dados = coletar_dados()

    if dados:
        realizar_diagnostico(dados)


if __name__ == "__main__":
    main()
