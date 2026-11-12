
import csv
import calendar
from datetime import date
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


def meses_da_tarifa(tarifa):
    inicio = date.fromisoformat(tarifa["vigencia_inicio"])
    fim = date.fromisoformat(tarifa["vigencia_fim"])

    ano = inicio.year
    mes = inicio.month
    meses = []

    while (ano, mes) <= (fim.year, fim.month):
        primeiro_dia = date(ano, mes, 1)

        ultimo_numero = calendar.monthrange(ano, mes)[1]
        ultimo_dia = date(ano, mes, ultimo_numero)

        if primeiro_dia >= inicio and ultimo_dia <= fim:
            meses.append(f"{mes:02d}/{ano}")

        if mes == 12:
            ano += 1
            mes = 1
        else:
            mes += 1

    return meses


def listar_distribuidoras():
    tarifas = carregar_tarifas()

    distribuidoras = sorted({
        tarifa["distribuidora"].strip()
        for tarifa in tarifas
        if tarifa["distribuidora"].strip()
        and meses_da_tarifa(tarifa)
    })

    return distribuidoras


def listar_meses_disponiveis(nome_distribuidora):
    tarifas = carregar_tarifas()

    nome_busca = nome_distribuidora.strip().casefold()
    meses = set()

    for tarifa in tarifas:
        nome_arquivo = tarifa["distribuidora"].strip().casefold()

        if nome_busca == nome_arquivo:
            meses.update(meses_da_tarifa(tarifa))

    return sorted(
        meses,
        key=lambda mes: (int(mes[3:]), int(mes[:2]))
    )


def buscar_tarifa(nome_distribuidora, mes_referencia):
    tarifas = carregar_tarifas()

    nome_busca = nome_distribuidora.strip().casefold()

    for tarifa in tarifas:
        nome_arquivo = tarifa["distribuidora"].strip().casefold()

        if nome_busca != nome_arquivo:
            continue

        if mes_referencia not in meses_da_tarifa(tarifa):
            continue

        return {
            "distribuidora": tarifa["distribuidora"],
            "tarifa_te": Decimal(tarifa["tarifa_te"]),
            "tarifa_tusd": Decimal(tarifa["tarifa_tusd"]),
            "tarifa_total": Decimal(tarifa["tarifa_total"]),
            "vigencia_inicio": tarifa["vigencia_inicio"],
            "vigencia_fim": tarifa["vigencia_fim"]
        }

    return None
