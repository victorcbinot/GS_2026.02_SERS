
from decimal import Decimal


FATOR_EMISSAO_KG_CO2_KWH = Decimal("0.0461")


def comparar_alternativas(
    consumo_mensal,
    tarifa_total,
    cenarios_eficiencia,
    resultado_solar
):
    custo_atual = consumo_mensal * tarifa_total

    print("\n=== COMPARAÇÃO DE ALTERNATIVAS ===")

    print("\n1. SITUAÇÃO ATUAL")
    print(f"Consumo mensal: {consumo_mensal:.2f} kWh")
    print(f"Custo estimado: R$ {custo_atual:.2f}")

    emissao_atual = consumo_mensal * FATOR_EMISSAO_KG_CO2_KWH

    print(
        f"Emissões estimadas: "
        f"{emissao_atual:.2f} kg de CO2 por mês"
    )

    print("\n2. EFICIÊNCIA ENERGÉTICA")

    for cenario in cenarios_eficiencia:
        percentual = cenario["percentual"] * 100

        energia_economizada = cenario["consumo_economizado"]
        emissao_evitada = (
            energia_economizada * FATOR_EMISSAO_KG_CO2_KWH
        )

        print(f"\nRedução de {percentual:.0f}%")
        print(f"Consumo mensal: {cenario['novo_consumo']:.2f} kWh")
        print(f"Custo estimado: R$ {cenario['novo_custo']:.2f}")
        print(f"Economia mensal: R$ {cenario['economia']:.2f}")
        print(
            f"Emissões evitadas: "
            f"{emissao_evitada:.2f} kg de CO2 por mês"
        )
        print(
            f"Emissões evitadas por ano: "
            f"{emissao_evitada * 12:.2f} kg de CO2"
        )

    print("\n3. ENERGIA SOLAR FOTOVOLTAICA")

    investimento = resultado_solar["investimento_estimado"]
    geracao_mensal = resultado_solar["geracao_mensal"]

    emissao_evitada_solar = (
        geracao_mensal * FATOR_EMISSAO_KG_CO2_KWH
    )

    print(
        f"Potência estimada: "
        f"{resultado_solar['potencia_kwp']:.2f} kWp"
    )
    print(
        f"Geração mensal estimada: "
        f"{geracao_mensal:.2f} kWh"
    )
    print(
        f"Geração anual estimada: "
        f"{resultado_solar['geracao_anual']:.2f} kWh"
    )
    print(f"Investimento estimado: R$ {investimento:.2f}")
    print(
        f"Emissões potencialmente evitadas: "
        f"{emissao_evitada_solar:.2f} kg de CO2 por mês"
    )
    print(
        f"Emissões potencialmente evitadas por ano: "
        f"{emissao_evitada_solar * 12:.2f} kg de CO2"
    )

    print("\n=== RETORNO FINANCEIRO ESTIMADO ===")

    economia_mensal = custo_atual

    if economia_mensal > 0:
        economia_anual = economia_mensal * 12
        meses_retorno = investimento / economia_mensal
        anos_retorno = meses_retorno / 12

        print(f"Economia mensal teórica: R$ {economia_mensal:.2f}")
        print(f"Economia anual teórica: R$ {economia_anual:.2f}")
        print(f"Retorno estimado: {meses_retorno:.1f} meses")
        print(f"Equivalente a: {anos_retorno:.1f} anos")
    else:
        print("Não foi possível calcular o retorno financeiro.")

    print("\n=== CONSIDERAÇÕES AMBIENTAIS E DA COMPARAÇÃO ===")
    print("A eficiência energética reduz o consumo de eletricidade.")
    print("A energia solar pode reduzir a dependência da rede elétrica.")
    print("As emissões evitadas são estimativas baseadas no fator médio")
    print("de emissão da eletricidade brasileira em 2025.")
    print("Não são contabilizadas as emissões da fabricação,")
    print("transporte, instalação ou descarte dos painéis solares.")
    print("O dimensionamento solar é uma estimativa técnica.")
    print("O investimento solar utiliza uma referência histórica da EPE.")
    print("O retorno financeiro considera a compensação integral")
    print("da tarifa TE + TUSD sobre a energia gerada.")
    print("O retorno real e os impactos ambientais podem ser diferentes.")
