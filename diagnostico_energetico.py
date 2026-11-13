
import sys
from decimal import Decimal, InvalidOperation
from datetime import datetime

from consultar_tarifa import (
    buscar_tarifa,
    listar_distribuidoras,
    listar_meses_disponiveis
)
from eficiencia_energetica import simular_eficiencia
from energia_solar import simular_energia_solar
from comparar_alternativas import comparar_alternativas


def coletar_distribuidora():
    distribuidora = input("Distribuidora de energia: ").strip()

    distribuidoras = listar_distribuidoras()

    if not distribuidoras:
        raise RuntimeError(
            "Nenhuma distribuidora disponível na base de tarifas."
        )

    distribuidora_encontrada = next(
        (
            nome for nome in distribuidoras
            if nome.casefold() == distribuidora.casefold()
        ),
        None
    )

    if distribuidora_encontrada:
        return distribuidora_encontrada

    print("\nDistribuidora não encontrada.")
    print("\nDistribuidoras disponíveis:")

    for indice, nome in enumerate(distribuidoras, start=1):
        print(f"{indice}. {nome}")

    while True:
        try:
            escolha = int(
                input("\nEscolha o número da distribuidora: ")
            )

            if 1 <= escolha <= len(distribuidoras):
                return distribuidoras[escolha - 1]

            print("Escolha uma opção válida.")

        except ValueError:
            print("Digite o número de uma das opções.")


def coletar_mes_referencia(distribuidora):
    meses = listar_meses_disponiveis(distribuidora)

    if not meses:
        raise RuntimeError(
            "Nenhum mês disponível para a distribuidora selecionada."
        )

    while True:
        mes = input("Mês de referência (MM/AAAA): ").strip()

        try:
            datetime.strptime(mes, "%m/%Y")
        except ValueError:
            print("\nFormato inválido. Utilize MM/AAAA.")
            continue

        if mes in meses:
            return mes

        print("\nMês não disponível para essa distribuidora.")
        print("\nMeses disponíveis:")

        for indice, mes_disponivel in enumerate(meses, start=1):
            print(f"{indice}. {mes_disponivel}")

        while True:
            try:
                escolha = int(
                    input("\nEscolha o número do mês: ")
                )

                if 1 <= escolha <= len(meses):
                    return meses[escolha - 1]

                print("Escolha uma opção válida.")

            except ValueError:
                print("Digite o número de uma das opções.")


def coletar_valor_positivo(mensagem):
    while True:
        entrada = input(mensagem).strip().replace(",", ".")

        try:
            valor = Decimal(entrada)

            if valor.is_finite() and valor > 0:
                return valor

            print("Informe um valor numérico maior que zero.")

        except InvalidOperation:
            print("Valor inválido. Digite um número, por exemplo: 1500,50.")


def coletar_dados():
    print("\n=== DIAGNÓSTICO ENERGÉTICO RESIDENCIAL ===")

    distribuidora = coletar_distribuidora()

    mes_referencia = coletar_mes_referencia(distribuidora)

    consumo = coletar_valor_positivo(
        "Consumo mensal (kWh): "
    )

    valor_conta = coletar_valor_positivo(
        "Valor total da conta (R$): "
    )

    return {
        "distribuidora": distribuidora,
        "consumo_kwh": consumo,
        "valor_conta": valor_conta,
        "mes_referencia": mes_referencia
    }


def calcular_custo_estimado(consumo, tarifa_total):
    return consumo * tarifa_total


def realizar_diagnostico(dados):
    tarifa = buscar_tarifa(
        dados["distribuidora"],
        dados["mes_referencia"]
    )

    if tarifa is None:
        print("\nNão foi possível encontrar a tarifa para os dados selecionados.")
        return

    consumo = dados["consumo_kwh"]
    tarifa_total = tarifa["tarifa_total"]

    custo_estimado = calcular_custo_estimado(consumo, tarifa_total)

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
    print(
        f"Investimento estimado: "
        f"R$ {resultado_solar['investimento_estimado']:.2f}"
    )

    print("\nObservação:")
    print("O dimensionamento solar utiliza parâmetros estimados.")
    print("O custo de instalação utiliza uma referência histórica da EPE.")
    print("A geração real depende das condições de instalação.")
    print("A geração estimada não representa economia financeira integral.")

    comparar_alternativas(
        consumo,
        tarifa_total,
        cenarios_eficiencia,
        resultado_solar
    )


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    print(
        "O diagnóstico energético agora é realizado pelo chatbot "
        "Citizen Assist AI."
    )
    print("Execute: python citizen_assist_ai.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
