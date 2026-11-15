import io
import sys
import unittest
from contextlib import redirect_stdout
from decimal import Decimal, InvalidOperation
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from comparar_alternativas import (  # noqa: E402
    calcular_comparacao_alternativas,
    comparar_alternativas
)
from consultar_tarifa import (  # noqa: E402
    buscar_tarifa,
    listar_distribuidoras,
    listar_meses_disponiveis,
    meses_da_tarifa
)
from diagnostico_energetico import (  # noqa: E402
    calcular_custo_estimado,
    calcular_diferenca_conta,
    converter_numero_brasileiro
)
from eficiencia_energetica import (  # noqa: E402
    calcular_cenarios_eficiencia,
    simular_eficiencia
)
from energia_solar import simular_energia_solar  # noqa: E402
from processar_tarifa import converter_decimal  # noqa: E402
from recomendacoes import gerar_recomendacoes  # noqa: E402


TARIFAS_CONTROLE = [
    {
        "distribuidora": "DISTRIBUIDORA TESTE",
        "cnpj": "00000000000000",
        "vigencia_inicio": "2026-01-01",
        "vigencia_fim": "2026-03-31",
        "resolucao": "TESTE",
        "tarifa_te": "0.30",
        "tarifa_tusd": "0.20",
        "tarifa_total": "0.50"
    },
    {
        "distribuidora": "NÃO INFORMADO",
        "cnpj": "11111111111111",
        "vigencia_inicio": "2026-01-01",
        "vigencia_fim": "2026-03-31",
        "resolucao": "TESTE",
        "tarifa_te": "0.10",
        "tarifa_tusd": "0.10",
        "tarifa_total": "0.20"
    }
]


class TestEntradaNumerica(unittest.TestCase):
    def test_inteiro_sem_separador(self):
        self.assertEqual(
            converter_numero_brasileiro("1500"),
            Decimal("1500")
        )

    def test_milhar_com_ponto(self):
        self.assertEqual(
            converter_numero_brasileiro("1.500"),
            Decimal("1500")
        )

    def test_milhar_com_virgula_decimal(self):
        self.assertEqual(
            converter_numero_brasileiro("1.500,50"),
            Decimal("1500.50")
        )

    def test_virgula_decimal(self):
        self.assertEqual(
            converter_numero_brasileiro("1500,50"),
            Decimal("1500.50")
        )

    def test_ponto_decimal(self):
        self.assertEqual(
            converter_numero_brasileiro("1500.50"),
            Decimal("1500.50")
        )

    def test_milhoes_com_virgula_decimal(self):
        self.assertEqual(
            converter_numero_brasileiro("1.500.000,25"),
            Decimal("1500000.25")
        )

    def test_com_cifrao_e_espacos(self):
        self.assertEqual(
            converter_numero_brasileiro("R$ 1.500,50"),
            Decimal("1500.50")
        )

    def test_rejeita_separadores_invalidos(self):
        with self.assertRaises(InvalidOperation):
            converter_numero_brasileiro("1.50.00")

    def test_rejeita_texto(self):
        with self.assertRaises(InvalidOperation):
            converter_numero_brasileiro("abc")

    def test_rejeita_vazio(self):
        with self.assertRaises(InvalidOperation):
            converter_numero_brasileiro("")

    def test_rejeita_valor_negativo(self):
        with self.assertRaises(InvalidOperation):
            converter_numero_brasileiro("-10")


class TestValorDaConta(unittest.TestCase):
    def test_custo_estimado(self):
        self.assertEqual(
            calcular_custo_estimado(
                Decimal("1500"),
                Decimal("0.50")
            ),
            Decimal("750.00")
        )

    def test_diferenca_positiva(self):
        self.assertEqual(
            calcular_diferenca_conta(
                Decimal("1000"),
                Decimal("750")
            ),
            Decimal("250")
        )

    def test_diferenca_negativa(self):
        self.assertEqual(
            calcular_diferenca_conta(
                Decimal("500"),
                Decimal("750")
            ),
            Decimal("-250")
        )


class TestEnergiaSolar(unittest.TestCase):
    def test_dimensionamento_para_1500_kwh(self):
        resultado = simular_energia_solar(Decimal("1500"))

        self.assertEqual(resultado["potencia_kwp"], Decimal("12.5"))
        self.assertEqual(resultado["geracao_mensal"], Decimal("1500.000"))
        self.assertEqual(resultado["geracao_anual"], Decimal("18000.000"))
        self.assertEqual(
            resultado["investimento_estimado"],
            Decimal("33250.00")
        )


class TestEficienciaEnergetica(unittest.TestCase):
    def test_cenarios_de_reducao_controlados(self):
        cenarios = calcular_cenarios_eficiencia(
            Decimal("1000"),
            Decimal("0.50")
        )

        self.assertEqual(len(cenarios), 3)

        economias = [cenario["economia"] for cenario in cenarios]
        esperadas = [
            Decimal("25"),
            Decimal("50"),
            Decimal("75")
        ]

        self.assertEqual(economias, esperadas)

    def test_novos_consumos_controlados(self):
        cenarios = calcular_cenarios_eficiencia(
            Decimal("1000"),
            Decimal("0.50")
        )

        novos_consumos = [
            cenario["novo_consumo"] for cenario in cenarios
        ]

        self.assertEqual(
            novos_consumos,
            [
                Decimal("950.00"),
                Decimal("900.00"),
                Decimal("850.00")
            ]
        )

    def test_simulacao_continua_retornando_cenarios(self):
        with redirect_stdout(io.StringIO()) as saida:
            cenarios = simular_eficiencia(
                Decimal("1000"),
                Decimal("0.50")
            )

        self.assertEqual(len(cenarios), 3)
        self.assertIn(
            "SIMULAÇÃO DE EFICIÊNCIA ENERGÉTICA",
            saida.getvalue()
        )


class TestComparacaoAlternativas(unittest.TestCase):
    def criar_comparacao(self):
        consumo = Decimal("1000")
        tarifa = Decimal("0.50")
        cenarios = calcular_cenarios_eficiencia(consumo, tarifa)
        solar = simular_energia_solar(consumo)

        return calcular_comparacao_alternativas(
            consumo,
            tarifa,
            cenarios,
            solar
        )

    def test_custo_e_emissao_atuais(self):
        comparacao = self.criar_comparacao()

        self.assertEqual(comparacao["custo_atual"], Decimal("500.00"))
        self.assertEqual(
            comparacao["emissao_atual"],
            Decimal("46.100")
        )

    def test_economia_dos_cenarios(self):
        comparacao = self.criar_comparacao()

        economias = [
            cenario["economia"]
            for cenario in comparacao["cenarios_eficiencia"]
        ]

        self.assertEqual(
            economias,
            [Decimal("25"), Decimal("50"), Decimal("75")]
        )

    def test_investimento_solar_preservado(self):
        comparacao = self.criar_comparacao()
        solar = simular_energia_solar(Decimal("1000"))

        self.assertEqual(
            comparacao["solar"]["investimento_estimado"],
            solar["investimento_estimado"]
        )

    def test_nao_exibe_payback_numerico(self):
        consumo = Decimal("1000")
        tarifa = Decimal("0.50")
        cenarios = calcular_cenarios_eficiencia(consumo, tarifa)
        solar = simular_energia_solar(consumo)

        with redirect_stdout(io.StringIO()) as saida:
            comparar_alternativas(
                consumo,
                tarifa,
                cenarios,
                solar
            )

        texto = saida.getvalue()

        self.assertIn(
            "Não é apresentado um prazo de retorno (payback) numérico.",
            texto
        )
        self.assertNotIn("Retorno estimado:", texto)
        self.assertNotIn("Equivalente a:", texto)


class TestRecomendacoes(unittest.TestCase):
    def criar_recomendacoes(self):
        consumo = Decimal("1000")
        tarifa = Decimal("0.50")
        cenarios = calcular_cenarios_eficiencia(consumo, tarifa)
        solar = simular_energia_solar(consumo)
        comparacao = calcular_comparacao_alternativas(
            consumo,
            tarifa,
            cenarios,
            solar
        )

        return gerar_recomendacoes(comparacao)

    def test_recomendacao_de_eficiencia_usa_cenarios(self):
        recomendacoes = self.criar_recomendacoes()

        self.assertEqual(
            recomendacoes["eficiencia"]["economia_minima"],
            Decimal("25")
        )
        self.assertEqual(
            recomendacoes["eficiencia"]["economia_maxima"],
            Decimal("75")
        )
        self.assertIsNone(
            recomendacoes["eficiencia"]["investimento"]
        )

    def test_recomendacao_solar_preserva_estimativas(self):
        recomendacoes = self.criar_recomendacoes()

        self.assertEqual(
            recomendacoes["solar"]["investimento"],
            Decimal("22166.67")
        )
        self.assertEqual(
            recomendacoes["solar"]["economia_potencial"],
            Decimal("500.00")
        )
        self.assertIn(
            "não é garantida",
            recomendacoes["solar"]["limitacoes"]
        )

    def test_conclusao_nao_afirma_retorno_financeiro(self):
        recomendacoes = self.criar_recomendacoes()

        self.assertIn(
            "Não há dados suficientes",
            recomendacoes["conclusao"]
        )
        self.assertIn(
            "retorno financeiro",
            recomendacoes["conclusao"]
        )

    def test_todas_as_alternativas_sao_justificadas(self):
        recomendacoes = self.criar_recomendacoes()

        for chave in ("eficiencia", "solar", "combinacao"):
            self.assertIn("titulo", recomendacoes[chave])
            self.assertIn("justificativa", recomendacoes[chave])
            self.assertIn("limitacoes", recomendacoes[chave])


class TestConsultarTarifa(unittest.TestCase):
    @patch(
        "consultar_tarifa.carregar_tarifas",
        return_value=TARIFAS_CONTROLE
    )
    def test_tarifa_controlada(self, _):
        tarifa = buscar_tarifa("DISTRIBUIDORA TESTE", "02/2026")

        self.assertIsNotNone(tarifa)
        self.assertEqual(tarifa["tarifa_te"], Decimal("0.30"))
        self.assertEqual(tarifa["tarifa_tusd"], Decimal("0.20"))
        self.assertEqual(tarifa["tarifa_total"], Decimal("0.50"))

    @patch(
        "consultar_tarifa.carregar_tarifas",
        return_value=TARIFAS_CONTROLE
    )
    def test_tarifa_inexistente_retorna_none(self, _):
        self.assertIsNone(buscar_tarifa("NAO EXISTE", "02/2026"))

    @patch(
        "consultar_tarifa.carregar_tarifas",
        return_value=TARIFAS_CONTROLE
    )
    def test_mes_fora_da_vigencia_retorna_none(self, _):
        self.assertIsNone(buscar_tarifa("DISTRIBUIDORA TESTE", "04/2026"))

    @patch(
        "consultar_tarifa.carregar_tarifas",
        return_value=TARIFAS_CONTROLE
    )
    def test_listar_meses_controlados(self, _):
        self.assertEqual(
            listar_meses_disponiveis("DISTRIBUIDORA TESTE"),
            ["01/2026", "02/2026", "03/2026"]
        )

    @patch(
        "consultar_tarifa.carregar_tarifas",
        return_value=TARIFAS_CONTROLE
    )
    def test_lista_nao_inclui_valor_invalido(self, _):
        nomes = [nome.casefold() for nome in listar_distribuidoras()]
        self.assertNotIn("não informado", nomes)

    def test_meses_da_tarifa_somente_meses_completos(self):
        tarifa = {
            "vigencia_inicio": "2026-01-01",
            "vigencia_fim": "2026-03-15"
        }

        self.assertEqual(meses_da_tarifa(tarifa), ["01/2026", "02/2026"])


class TestProcessarTarifa(unittest.TestCase):
    def test_converte_mwh_para_kwh(self):
        self.assertEqual(
            converter_decimal("332,24") / Decimal("1000"),
            Decimal("0.33224")
        )

    def test_converte_decimal_com_virgula(self):
        self.assertEqual(converter_decimal("0,80168"), Decimal("0.80168"))


if __name__ == "__main__":
    unittest.main()
