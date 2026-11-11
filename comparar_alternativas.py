
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

    print("\n2. EFICIÊNCIA ENERGÉTICA")

    for cenario in cenarios_eficiencia:
        percentual = cenario["percentual"] * 100

        print(f"\nRedução de {percentual:.0f}%")
        print(f"Consumo mensal: {cenario['novo_consumo']:.2f} kWh")
        print(f"Custo estimado: R$ {cenario['novo_custo']:.2f}")
        print(f"Economia mensal: R$ {cenario['economia']:.2f}")

    print("\n3. ENERGIA SOLAR FOTOVOLTAICA")
    print(
        f"Potência estimada: "
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

    print("\n=== CONSIDERAÇÕES DA COMPARAÇÃO ===")
    print("A eficiência energética reduz o consumo da residência.")
    print("A energia solar pode gerar eletricidade no próprio imóvel.")
    print("O dimensionamento solar é uma estimativa técnica.")
    print("O investimento solar utiliza uma referência histórica da EPE.")
    print("A economia solar depende das condições de instalação,")
    print("das regras de compensação e dos componentes da conta.")
