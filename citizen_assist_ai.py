import sys
import unicodedata

from comparar_alternativas import (
    calcular_comparacao_alternativas,
    comparar_alternativas
)
from consultar_tarifa import buscar_tarifa
from diagnostico_energetico import (
    calcular_custo_estimado,
    calcular_diferenca_conta,
    coletar_dados
)
from eficiencia_energetica import calcular_cenarios_eficiencia
from energia_solar import simular_energia_solar
from recomendacoes import gerar_recomendacoes


NOME_ASSISTENTE = "Citizen Assist AI"

PERGUNTAS_FREQUENTES = [
    (
        ("diagnostico", "diagnóstico", "simular", "calcular", "meus dados"),
        "Posso fazer isso! Escolha a opção 1 do menu e informe sua "
        "distribuidora, o mês de referência, o consumo mensal em kWh e o "
        "valor total da sua conta. O diagnóstico usa os dados reais da "
        "base tarifária da ANEEL."
    ),
    (
        ("recomend", "melhor alternativa", "qual alternativa",
         "qual escolher", "devo escolher"),
        "Para receber uma recomendação baseada nos seus dados, faça o "
        "diagnóstico na opção 1. O assistente compara eficiência "
        "energética e energia solar, explica vantagens e limitações e "
        "não afirma qual alternativa terá melhor retorno financeiro sem "
        "custos reais e uma avaliação técnica."
    ),
    (
        ("retorno", "payback", "vale a pena", "se paga"),
        "O projeto não calcula um prazo de retorno (payback) numérico. "
        "Faltam dados sobre autoconsumo, regras de compensação, tarifas "
        "futuras, manutenção e disponibilidade do sistema. O investimento "
        "inicial e a economia potencial são apenas referências para "
        "comparação, não uma previsão de retorno."
    ),
    (
        ("investimento", "preco", "preço", "custo do sistema", "quanto custa"),
        "O investimento solar é estimado com a referência histórica de "
        "R$ 2,66 por Wp, da EPE/Greener (primeiro semestre de 2024). Esse "
        "valor serve para uma estimativa acadêmica e não substitui um "
        "orçamento atualizado de instalação."
    ),
    (
        ("co2", "emisso", "emissao", "carbono", "ambiente", "sustent"),
        "As emissões são estimadas com o fator médio de 0,0461 kgCO₂/kWh, "
        "do MCTI, referente ao Sistema Interligado Nacional em 2025. A "
        "eficiência energética reduz emissões ao economizar eletricidade, "
        "e a geração solar pode evitar emissões ao substituir energia da "
        "rede. O cálculo não inclui o ciclo de vida dos equipamentos."
    ),
    (
        ("tusd", "te e", "tarifa", "conta", "fatura"),
        "A conta de energia pode incluir TE (Tarifa de Energia), TUSD "
        "(Tarifa de Uso do Sistema de Distribuição), impostos, bandeiras "
        "tarifárias e outros encargos. O diagnóstico calcula uma estimativa "
        "somente com TE + TUSD, então o valor pode ser diferente do total "
        "da sua conta."
    ),
    (
        ("solar", "fotovoltaic", "fotovoltaico", "painel", "geracao solar"),
        "A energia solar fotovoltaica transforma a luz do sol em "
        "eletricidade. O simulador estima a potência necessária para "
        "atender ao consumo informado, a geração mensal e anual e uma "
        "referência de investimento. O dimensionamento usa parâmetros "
        "médios e não substitui um projeto técnico no local."
    ),
    (
        ("eficiencia", "eficiência", "economizar", "economia", "reduzir"),
        "Eficiência energética significa usar menos eletricidade para "
        "realizar as mesmas atividades, por exemplo com iluminação LED, "
        "equipamentos mais eficientes e bons hábitos de uso. O simulador "
        "mostra cenários hipotéticos de redução de 5%, 10% e 15% do "
        "consumo, sem garantir que essa economia ocorra na prática."
    ),
    (
        ("consumo", "kwh", "gasto de energia"),
        "O consumo mensal é a quantidade de energia elétrica usada no "
        "período, medida em kWh. Ele aparece na conta de luz e é a base do "
        "diagnóstico. Para uma análise completa, escolha a opção 1 do menu "
        "e informe seus dados."
    )
]

RESPOSTA_PADRAO = (
    "Ainda não tenho uma resposta específica para essa pergunta. Posso "
    "ajudar com consumo, economia de energia, eficiência energética, "
    "energia solar, tarifas, investimento, limitações do retorno "
    "financeiro e emissões de CO₂. Para resultados com seus números, "
    "escolha a opção 1 do menu e "
    "faça o diagnóstico energético."
)


def normalizar_texto(texto):
    sem_acentos = unicodedata.normalize("NFKD", texto)
    sem_acentos = "".join(
        caractere for caractere in sem_acentos
        if not unicodedata.combining(caractere)
    )

    return sem_acentos.casefold().strip()


def encontrar_resposta(pergunta):
    texto = normalizar_texto(pergunta)

    for palavras_chave, resposta in PERGUNTAS_FREQUENTES:
        if any(
            normalizar_texto(palavra) in texto
            for palavra in palavras_chave
        ):
            return resposta

    return RESPOSTA_PADRAO


def exibir_apresentacao():
    print("=" * 64)
    print(f"{NOME_ASSISTENTE:^64}")
    print("=" * 64)
    print(
        "Olá! Eu sou o Citizen Assist AI, um assistente para ajudar você a"
    )
    print(
        "entender seu consumo de energia e avaliar formas de economizar."
    )
    print()
    print("Comigo, você pode:")
    print("- tirar dúvidas sobre consumo, tarifas e economia de energia;")
    print("- fazer um diagnóstico energético com os dados da sua conta;")
    print("- comparar eficiência energética e energia solar fotovoltaica;")
    print("- consultar as fontes e as limitações das estimativas.")
    print()
    print(
        "Importante: as respostas usam os cálculos do projeto e são"
    )
    print(
        "estimativas educacionais, não garantias de economia ou retorno."
    )


def exibir_menu():
    print("\n=== MENU DO CITIZEN ASSIST AI ===")
    print("1. Fazer diagnóstico energético")
    print("2. Tirar dúvidas sobre consumo e economia de energia")
    print("3. Ver fontes de dados e limitações")
    print("4. Encerrar a conversa")


def exibir_fontes_e_limitacoes():
    print("\n=== FONTES DE DADOS ===")
    print(
        "ANEEL: tarifas residenciais (TE e TUSD) das distribuidoras."
    )
    print(
        "EPE/Greener: referência histórica de R$ 2,66/Wp para o"
    )
    print("investimento em sistemas solares de pequeno e médio porte.")
    print(
        "MCTI: fator médio de emissão de 0,0461 kgCO₂/kWh, referente"
    )
    print("ao Sistema Interligado Nacional em 2025.")
    print(
        "Premissas do projeto: 5 horas de sol pleno por dia, fator de "
    )
    print(
        "desempenho de 0,80 e 30 dias por mês. Esses valores são "
    )
    print(
        "hipóteses acadêmicas e não medições do local do usuário."
    )

    print("\n=== LIMITAÇÕES DAS ESTIMATIVAS ===")
    print(
        "- O custo calculado considera apenas TE e TUSD; a conta real"
    )
    print("  pode incluir impostos, bandeiras e outros encargos.")
    print(
        "- Os cenários de eficiência energética são hipóteses de"
    )
    print("  redução de 5%, 10% e 15%, sem garantia de economia.")
    print(
        "- O dimensionamento solar usa parâmetros médios e não"
    )
    print("  substitui um projeto técnico de instalação.")
    print(
        "- O investimento solar usa uma referência histórica de 2024"
    )
    print("  e pode estar diferente dos preços atuais.")
    print(
        "- O retorno financeiro é teórico e não considera todas as"
    )
    print("  regras de compensação de energia.")
    print(
        "- As emissões evitadas são estimativas e não incluem a"
    )
    print("  fabricação, o transporte, a instalação ou o descarte"
    )
    print("  dos equipamentos solares.")


def conversar_sobre_energia():
    print("\n=== DÚVIDAS SOBRE ENERGIA ===")
    print(
        "Digite sua pergunta. Para voltar ao menu, digite 'voltar'."
    )
    print(
        "Exemplo: como posso economizar energia? O que é energia solar?"
    )

    while True:
        try:
            pergunta = input("\nVocê: ").strip()
        except EOFError:
            return

        if not pergunta:
            print(f"{NOME_ASSISTENTE}: Por favor, digite uma pergunta.")
            continue

        if normalizar_texto(pergunta) in {
            "voltar",
            "menu",
            "sair",
            "encerrar"
        }:
            return

        print(f"\n{NOME_ASSISTENTE}: {encontrar_resposta(pergunta)}")


def exibir_resultado_simples(
    dados,
    tarifa,
    custo_estimado,
    diferenca_conta,
    cenarios_eficiencia,
    resultado_solar,
    economia_potencial_solar
):
    consumo = dados["consumo_kwh"]
    tarifa_total = tarifa["tarifa_total"]

    economia_5 = cenarios_eficiencia[0]["economia"]
    economia_10 = cenarios_eficiencia[1]["economia"]
    economia_15 = cenarios_eficiencia[2]["economia"]

    print("\n=== RESUMO EM LINGUAGEM SIMPLES ===")
    print(
        f"Seu consumo é de {consumo:.2f} kWh por mês. Com a tarifa de "
        f"R$ {tarifa_total:.5f}/kWh da {tarifa['distribuidora']},"
    )
    print(
        f"o custo estimado de TE + TUSD é R$ {custo_estimado:.2f} por mês."
    )

    print(f"A conta informada foi R$ {dados['valor_conta']:.2f}.")

    if diferenca_conta > 0:
        print(
            f"Ela é R$ {diferenca_conta:.2f} maior que o custo estimado "
            "de TE + TUSD."
        )
    elif diferenca_conta < 0:
        print(
            f"Ela é R$ {abs(diferenca_conta):.2f} menor que o custo "
            "estimado de TE + TUSD."
        )
    else:
        print("Ela é igual ao custo estimado de TE + TUSD.")

    print(
        "Essa diferença pode decorrer de impostos, bandeiras tarifárias, "
        "encargos e outros componentes da fatura."
    )
    print(
        "A estimativa de TE + TUSD não representa o valor integral da "
        "conta de energia."
    )

    print("\nO que as alternativas podem trazer:")
    print(
        "Os cenários de 5%, 10% e 15% são hipóteses de redução, "
        "não resultados garantidos."
    )
    print(
        f"- Eficiência energética: reduzir 5% do consumo economizaria "
        f"cerca de R$ {economia_5:.2f} por mês."
    )
    print(
        f"  Com 10%, a economia seria de aproximadamente "
        f"R$ {economia_10:.2f}; com 15%, R$ {economia_15:.2f}."
    )
    print(
        "  O projeto não estima o custo das medidas de eficiência "
        "energética."
    )
    print(
        f"- Energia solar: um sistema de "
        f"{resultado_solar['potencia_kwp']:.2f} kWp poderia gerar cerca de "
        f"{resultado_solar['geracao_mensal']:.2f} kWh por mês."
    )
    print(
        f"  O investimento inicial estimado é de "
        f"R$ {resultado_solar['investimento_estimado']:.2f}."
    )
    print(
        f"  A economia potencial máxima teórica é de "
        f"R$ {economia_potencial_solar:.2f} por mês, se toda a geração "
        "fosse compensada."
    )
    print(
        "  Essa economia não é garantida e não há previsão de prazo de "
        "retorno."
    )
    print(
        "  Vantagens: gera energia renovável no próprio imóvel e reduz "
        "a dependência da rede elétrica."
    )
    print(
        "- Combinando as duas: usar a eficiência primeiro pode diminuir "
        "o consumo e, com isso, reduzir o tamanho necessário do sistema "
        "solar."
    )

    print("\nFontes principais: ANEEL (tarifas), EPE/Greener "
          "(investimento solar) e MCTI (emissões).")
    print(
        "As estimativas têm limitações. Use a opção 3 do menu para ver "
        "os detalhes."
    )


def exibir_recomendacoes(recomendacoes):
    print("\n=== RECOMENDAÇÕES DO CITIZEN ASSIST AI ===")

    for chave in ("eficiencia", "solar", "combinacao"):
        recomendacao = recomendacoes[chave]
        print(f"\n{recomendacao['titulo']}:")
        print(f"Justificativa: {recomendacao['justificativa']}")
        print(f"Vantagens: {recomendacao['vantagens']}")
        print(f"Limitações: {recomendacao['limitacoes']}")

    print("\nConclusão:")
    print(recomendacoes["conclusao"])


def executar_diagnostico():
    try:
        dados = coletar_dados()
    except (RuntimeError, EOFError) as erro:
        if isinstance(erro, RuntimeError):
            print(f"\n{NOME_ASSISTENTE}: Não foi possível iniciar o "
                  f"diagnóstico. {erro}")
        return

    tarifa = buscar_tarifa(
        dados["distribuidora"],
        dados["mes_referencia"]
    )

    if tarifa is None:
        print(
            f"\n{NOME_ASSISTENTE}: Não encontrei a tarifa para essa "
            "distribuidora e mês. Tente novamente com outros dados."
        )
        return

    consumo = dados["consumo_kwh"]
    tarifa_total = tarifa["tarifa_total"]
    custo_estimado = calcular_custo_estimado(consumo, tarifa_total)
    diferenca_conta = calcular_diferenca_conta(
        dados["valor_conta"],
        custo_estimado
    )

    cenarios_eficiencia = calcular_cenarios_eficiencia(
        consumo,
        tarifa_total
    )

    resultado_solar = simular_energia_solar(consumo)
    comparacao = calcular_comparacao_alternativas(
        consumo,
        tarifa_total,
        cenarios_eficiencia,
        resultado_solar
    )

    exibir_resultado_simples(
        dados,
        tarifa,
        custo_estimado,
        diferenca_conta,
        cenarios_eficiencia,
        resultado_solar,
        comparacao["solar"]["economia_potencial_mensal"]
    )

    print("\nAgora vou mostrar a comparação detalhada calculada pelo "
          "projeto:")
    comparar_alternativas(
        consumo,
        tarifa_total,
        cenarios_eficiencia,
        resultado_solar
    )

    recomendacoes = gerar_recomendacoes(comparacao)
    exibir_recomendacoes(recomendacoes)

    print(
        "\nVocê pode escolher a opção 1 para fazer um novo diagnóstico "
        "ou a opção 4 para encerrar a conversa."
    )


def configurar_saida():
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, OSError):
            pass


def main():
    configurar_saida()
    exibir_apresentacao()

    while True:
        exibir_menu()

        try:
            opcao = input("\nEscolha uma opção: ").strip()
        except EOFError:
            print("\nAté logo!")
            return 0

        if opcao == "1":
            executar_diagnostico()

        elif opcao == "2":
            conversar_sobre_energia()

        elif opcao == "3":
            exibir_fontes_e_limitacoes()

        elif opcao == "4":
            print(
                f"\n{NOME_ASSISTENTE}: Obrigado pela conversa! "
                "Até logo."
            )
            return 0

        else:
            print(
                "Opção inválida. Digite 1, 2, 3 ou 4."
            )


if __name__ == "__main__":
    sys.exit(main())
