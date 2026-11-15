
def gerar_recomendacoes(comparacao):
    cenario_minimo = comparacao["cenarios_eficiencia"][0]
    cenario_maximo = comparacao["cenarios_eficiencia"][-1]
    solar = comparacao["solar"]

    return {
        "eficiencia": {
            "titulo": "Eficiência energética",
            "justificativa": (
                "Os cenários de redução indicam economia estimada entre "
                f"R$ {cenario_minimo['economia']:.2f} e "
                f"R$ {cenario_maximo['economia']:.2f} por mês, "
                "condicionada à redução efetiva do consumo."
            ),
            "vantagens": (
                "Pode ser adotada aos poucos e não depende de geração "
                "de energia no local. O projeto não calcula o custo das "
                "medidas, portanto não é possível afirmar qual será o "
                "investimento necessário."
            ),
            "limitacoes": (
                "Os percentuais de 5%, 10% e 15% são hipóteses. A economia "
                "depende dos equipamentos, dos hábitos e da viabilidade "
                "de cada medida."
            ),
            "economia_minima": cenario_minimo["economia"],
            "economia_maxima": cenario_maximo["economia"],
            "investimento": None
        },
        "solar": {
            "titulo": "Energia solar fotovoltaica",
            "justificativa": (
                f"O dimensionamento estimado é de "
                f"{solar['potencia_kwp']:.2f} kWp, com investimento "
                f"inicial de referência de "
                f"R$ {solar['investimento_estimado']:.2f} e economia "
                f"potencial máxima de "
                f"R$ {solar['economia_potencial_mensal']:.2f} por mês."
            ),
            "vantagens": (
                "Gera energia renovável no próprio imóvel e pode reduzir "
                "a dependência da rede elétrica. As emissões "
                "potencialmente evitadas foram estimadas em "
                f"{solar['emissao_evitada']:.2f} kg de CO₂ por mês."
            ),
            "limitacoes": (
                "A economia potencial considera compensação integral de "
                "TE + TUSD e não é garantida. O investimento usa uma "
                "referência histórica de 2024 e o dimensionamento não "
                "substitui um projeto técnico."
            ),
            "investimento": solar["investimento_estimado"],
            "economia_potencial": solar["economia_potencial_mensal"]
        },
        "combinacao": {
            "titulo": "Eficiência energética + energia solar",
            "justificativa": (
                "As duas alternativas podem ser combinadas. Reduzir o "
                "consumo primeiro pode diminuir a potência necessária do "
                "sistema solar, mas esse novo dimensionamento não é "
                "calculado pelo projeto."
            ),
            "vantagens": (
                "A combinação pode reunir a redução do consumo com a "
                "geração renovável no local."
            ),
            "limitacoes": (
                "A combinação exigiria uma nova simulação com o consumo "
                "reduzido e uma avaliação técnica e financeira específica."
            )
        },
        "conclusao": (
            "Não há dados suficientes para afirmar qual alternativa terá "
            "melhor retorno financeiro. A escolha depende do objetivo do "
            "usuário: reduzir a conta com medidas de eficiência, investir "
            "em geração solar ou combinar as duas. Custos reais, regras "
            "de compensação e condições do imóvel precisam ser avaliados."
        )
    }
