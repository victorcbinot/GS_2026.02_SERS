
import csv
from decimal import Decimal
from pathlib import Path


ARQUIVO_TARIFAS = (
    Path(__file__).parent
    / "dados"
    / "tarifas_residenciais_processadas.csv"
)


def carregar_tarifas():
    with open(
        ARQUIVO_TARIFAS,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as arquivo:
        leitor = csv.DictReader(arquivo, delimiter=";")
        return list(leitor)


def listar_distribuidoras():
    tarifas = carregar_tarifas()

    distribuidoras = sorted({
        tarifa["distribuidora"].strip()
        for tarifa in tarifas
        if tarifa["distribuidora"].strip()
    })

    return distribuidoras


def buscar_tarifa(nome_distribuidora):
    tarifas = carregar_tarifas()

    nome_busca = nome_distribuidora.strip().casefold()

    for tarifa in tarifas:
        nome_arquivo = tarifa["distribuidora"].strip().casefold()

        if nome_busca == nome_arquivo:
            return {
                "distribuidora": tarifa["distribuidora"],
                "tarifa_te": Decimal(tarifa["tarifa_te"]),
                "tarifa_tusd": Decimal(tarifa["tarifa_tusd"]),
                "tarifa_total": Decimal(tarifa["tarifa_total"]),
                "vigencia_inicio": tarifa["vigencia_inicio"],
                "vigencia_fim": tarifa["vigencia_fim"]
            }

    return None
