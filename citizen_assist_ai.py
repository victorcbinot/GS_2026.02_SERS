import io
import sys
import unicodedata
from contextlib import redirect_stdout

from comparar_alternativas import comparar_alternativas
from consultar_tarifa import buscar_tarifa
from diagnostico_energetico import (
    calcular_custo_estimado,
    coletar_dados
)
from eficiencia_energetica import simular_eficiencia
from energia_solar import simular_energia_solar


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
        ("retorno", "payback", "vale a pena", "se paga"),
        "O retorno estimado compara o investimento inicial do sistema solar "
        "com a economia mensal teórica. Ele é apenas uma referência: não "
        "considera todas as regras de compensação, impostos, manutenção ou "
        "variações futuras da tarifa. Por isso, não deve ser tratado como "
        "garantia de retorno."
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
    "energia solar, tarifas, investimento, retorno estimado e emissões de "
    "CO₂. Para resultados com seus números, escolha a opção 1 do menu e "
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
    cenarios_eficiencia,
    resultado_solar
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
    print(
        "A conta informada foi R$ "
        f"{dados['valor_conta']:.2f}; a diferença pode ocorrer por causa "
        "de impostos, bandeiras e outros componentes."
    )

    print("\nO que as alternativas podem trazer:")
    print(
        f"- Eficiência energética: reduzir 5% do consumo economizaria "
        f"cerca de R$ {economia_5:.2f} por mês."
    )
    print(
        f"  Com 10%, a economia seria de aproximadamente "
        f"R$ {economia_10:.2f}; com 15%, R$ {economia_15:.2f}."
    )
    print(
        "  Vantagens: costuma exigir pouco ou nenhum investimento e "
        "pode trazer resultado rápido."
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

    with redirect_stdout(io.StringIO()):
        cenarios_eficiencia = simular_eficiencia(
            consumo,
            tarifa_total
        )

    resultado_solar = simular_energia_solar(consumo)

    exibir_resultado_simples(
        dados,
        tarifa,
        custo_estimado,
        cenarios_eficiencia,
        resultado_solar
    )

    print("\nAgora vou mostrar a comparação detalhada calculada pelo "
          "projeto:")
    comparar_alternativas(
        consumo,
        tarifa_total,
        cenarios_eficiencia,
        resultado_solar
    )

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
