import io
import sys
import unittest
from contextlib import redirect_stdout
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from consultar_tarifa import (  # noqa: E402
    buscar_tarifa,
    listar_distribuidoras,
    meses_da_tarifa
)
from eficiencia_energetica import simular_eficiencia  # noqa: E402
from energia_solar import simular_energia_solar  # noqa: E402
from processar_tarifa import converter_decimal  # noqa: E402


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
    def test_cenarios_de_reducao(self):
        with redirect_stdout(io.StringIO()):
            cenarios = simular_eficiencia(
                Decimal("1500"),
                Decimal("0.80168")
            )

        self.assertEqual(len(cenarios), 3)

        economias = [cenario["economia"] for cenario in cenarios]
        esperadas = [
            Decimal("60.1260000"),
            Decimal("120.2520000"),
            Decimal("180.3780000")
        ]

        self.assertEqual(economias, esperadas)


class TestConsultarTarifa(unittest.TestCase):
    def test_tarifa_edp_sp_dezembro_2026(self):
        tarifa = buscar_tarifa("EDP SP", "12/2026")

        self.assertIsNotNone(tarifa)
        self.assertEqual(tarifa["tarifa_te"], Decimal("0.33224"))
        self.assertEqual(tarifa["tarifa_tusd"], Decimal("0.46944"))
        self.assertEqual(tarifa["tarifa_total"], Decimal("0.80168"))

    def test_tarifa_inexistente_retorna_none(self):
        self.assertIsNone(buscar_tarifa("NAO EXISTE", "12/2026"))

    def test_meses_da_tarifa_somente_meses_completos(self):
        tarifa = {
            "vigencia_inicio": "2026-01-01",
            "vigencia_fim": "2026-03-15"
        }

        self.assertEqual(meses_da_tarifa(tarifa), ["01/2026", "02/2026"])

    def test_lista_nao_inclui_valor_invalido(self):
        nomes = [nome.casefold() for nome in listar_distribuidoras()]
        self.assertNotIn("não informado", nomes)


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
