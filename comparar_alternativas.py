
from decimal import Decimal


FATOR_EMISSAO_KG_CO2_KWH = Decimal("0.0461")


def calcular_comparacao_alternativas(
    consumo_mensal,
    tarifa_total,
    cenarios_eficiencia,
    resultado_solar
):
    custo_atual = consumo_mensal * tarifa_total
    emissao_atual = consumo_mensal * FATOR_EMISSAO_KG_CO2_KWH

    cenarios_comparados = []

    for cenario in cenarios_eficiencia:
        energia_economizada = cenario["consumo_economizado"]
        emissao_evitada = energia_economizada * FATOR_EMISSAO_KG_CO2_KWH

        cenarios_comparados.append({
            **cenario,
            "emissao_evitada": emissao_evitada,
            "emissao_evitada_anual": emissao_evitada * 12
        })

    geracao_mensal = resultado_solar["geracao_mensal"]
    emissao_evitada_solar = (
        geracao_mensal * FATOR_EMISSAO_KG_CO2_KWH
    )

    return {
        "custo_atual": custo_atual,
        "emissao_atual": emissao_atual,
        "cenarios_eficiencia": cenarios_comparados,
        "solar": {
            "potencia_kwp": resultado_solar["potencia_kwp"],
            "geracao_mensal": geracao_mensal,
            "geracao_anual": resultado_solar["geracao_anual"],
            "investimento_estimado": (
                resultado_solar["investimento_estimado"]
            ),
            "economia_potencial_mensal": (
                geracao_mensal * tarifa_total
            ),
            "emissao_evitada": emissao_evitada_solar,
            "emissao_evitada_anual": emissao_evitada_solar * 12
        }
    }


def comparar_alternativas(
    consumo_mensal,
    tarifa_total,
    cenarios_eficiencia,
    resultado_solar
):
    comparacao = calcular_comparacao_alternativas(
        consumo_mensal,
        tarifa_total,
        cenarios_eficiencia,
        resultado_solar
    )

    custo_atual = comparacao["custo_atual"]
    emissao_atual = comparacao["emissao_atual"]

    print("\n=== COMPARAÇÃO DE ALTERNATIVAS ===")

    print("\n1. SITUAÇÃO ATUAL")
    print(f"Consumo mensal: {consumo_mensal:.2f} kWh")
    print(f"Custo estimado de TE + TUSD: R$ {custo_atual:.2f}")
    print(
        f"Emissões estimadas: "
        f"{emissao_atual:.2f} kg de CO₂ por mês"
    )
    print(
        "Observação: o custo de TE + TUSD não representa o valor "
        "integral da conta."
    )

    print("\n2. EFICIÊNCIA ENERGÉTICA")
    print(
        "Os cenários de 5%, 10% e 15% são hipóteses de redução, "
        "não resultados garantidos."
    )
    print("Investimento em eficiência energética: não estimado pelo projeto.")

    for cenario in comparacao["cenarios_eficiencia"]:
        percentual = cenario["percentual"] * 100

        print(f"\nRedução de {percentual:.0f}%")
        print(f"Consumo mensal: {cenario['novo_consumo']:.2f} kWh")
        print(f"Custo estimado: R$ {cenario['novo_custo']:.2f}")
        print(f"Economia mensal estimada: R$ {cenario['economia']:.2f}")
        print(
            f"Emissões evitadas: "
            f"{cenario['emissao_evitada']:.2f} kg de CO₂ por mês"
        )
        print(
            f"Emissões evitadas por ano: "
            f"{cenario['emissao_evitada_anual']:.2f} kg de CO₂"
        )

    solar = comparacao["solar"]

    print("\n3. ENERGIA SOLAR FOTOVOLTAICA")
    print(
        f"Potência estimada: "
        f"{solar['potencia_kwp']:.2f} kWp"
    )
    print(
        f"Geração mensal estimada: "
        f"{solar['geracao_mensal']:.2f} kWh"
    )
    print(
        f"Geração anual estimada: "
        f"{solar['geracao_anual']:.2f} kWh"
    )
    print(
        f"Investimento inicial estimado: "
        f"R$ {solar['investimento_estimado']:.2f}"
    )
    print(
        f"Economia potencial máxima teórica: "
        f"R$ {solar['economia_potencial_mensal']:.2f} por mês"
    )
    print(
        "Essa economia potencial considera que toda a geração seria "
        "compensada integralmente pela tarifa TE + TUSD."
    )
    print(
        "Ela não é uma economia garantida e não representa uma "
        "previsão de retorno financeiro."
    )
    print(
        f"Emissões potencialmente evitadas: "
        f"{solar['emissao_evitada']:.2f} kg de CO₂ por mês"
    )
    print(
        f"Emissões potencialmente evitadas por ano: "
        f"{solar['emissao_evitada_anual']:.2f} kg de CO₂"
    )

    print("\n=== LIMITAÇÕES DO RETORNO FINANCEIRO ===")
    print("Não é apresentado um prazo de retorno (payback) numérico.")
    print(
        "O projeto não possui dados suficientes sobre autoconsumo, "
        "regras de compensação, tarifas futuras, manutenção e "
        "disponibilidade do sistema."
    )
    print(
        "Por isso, a economia potencial e o investimento inicial são "
        "referências para comparação, não uma previsão de retorno."
    )

    print("\n=== CONSIDERAÇÕES AMBIENTAIS E DA COMPARAÇÃO ===")
    print("A eficiência energética reduz o consumo de eletricidade.")
    print("A energia solar pode reduzir a dependência da rede elétrica.")
    print("As emissões evitadas são estimativas baseadas no fator médio")
    print("de emissão da eletricidade brasileira em 2025.")
    print("Não são contabilizadas as emissões da fabricação,")
    print("transporte, instalação ou descarte dos painéis solares.")
    print("O dimensionamento solar é uma estimativa técnica.")
    print("O investimento solar utiliza uma referência histórica da EPE.")
    print("Os valores reais podem ser diferentes das estimativas.")
