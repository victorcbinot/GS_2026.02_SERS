
import csv
import json
import sys
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path

import requests
from requests.exceptions import RequestException


URL_API = "https://dadosabertos.aneel.gov.br/api/3/action/datastore_search"
ID_RECURSO = "fcf2906c-7c32-4b9b-a637-054e7a5234f4"

FILTROS = {
    "DscBaseTarifaria": "Tarifa de Aplicação",
    "DscSubGrupo": "B1",
    "DscClasse": "Residencial",
    "DscModalidadeTarifaria": "Convencional",
    "DscSubClasse": "Residencial",
    "DscDetalhe": "Não se aplica"
}

PASTA_DADOS = Path(__file__).parent / "dados"
ARQUIVO_SAIDA = PASTA_DADOS / "tarifas_residenciais_processadas.csv"


def converter_data(valor):
    formatos = ("%d/%m/%Y", "%Y-%m-%d")

    for formato in formatos:
        try:
            return datetime.strptime(valor, formato).date()
        except ValueError:
            continue

    raise ValueError(f"Data inválida: {valor}")


def converter_decimal(valor):
    valor = str(valor).strip()

    if "," in valor:
        valor = valor.replace(".", "").replace(",", ".")

    return Decimal(valor)


def buscar_registros():
    registros = []
    limite = 1000
    deslocamento = 0

    while True:
        parametros = {
            "resource_id": ID_RECURSO,
            "limit": limite,
            "offset": deslocamento,
            "filters": json.dumps(FILTROS, ensure_ascii=False)
        }

        try:
            resposta = requests.get(
                URL_API,
                params=parametros,
                timeout=60
            )

            resposta.raise_for_status()
            resultado = resposta.json()

        except ValueError as erro:
            raise RuntimeError(
                "A API da ANEEL retornou uma resposta inválida."
            ) from erro

        except RequestException as erro:
            raise RuntimeError(
                "Falha ao consultar a API da ANEEL. "
                "Verifique a conexão com a internet e tente novamente."
            ) from erro

        if not resultado.get("success"):
            raise RuntimeError("A API da ANEEL retornou um erro.")

        dados_resultado = resultado.get("result") or {}
        lote = dados_resultado.get("records")

        if not isinstance(lote, list):
            raise RuntimeError(
                "A API da ANEEL retornou uma resposta inesperada."
            )

        registros.extend(lote)

        print(f"Registros consultados: {len(registros)}")

        if len(lote) < limite:
            break

        deslocamento += limite

    return registros


def processar_registros(registros):
    hoje = date.today()
    tarifas = {}

    for registro in registros:
        try:
            inicio = converter_data(registro["DatInicioVigencia"])
            fim = converter_data(registro["DatFimVigencia"])

            if not (inicio <= hoje <= fim):
                continue

            unidade = registro["DscUnidadeTerciaria"]

            te = converter_decimal(registro["VlrTE"])
            tusd = converter_decimal(registro["VlrTUSD"])

            if unidade == "MWh":
                te /= Decimal("1000")
                tusd /= Decimal("1000")
            elif unidade != "kWh":
                continue

            tarifa_total = te + tusd

            distribuidora = registro["SigAgente"]
            cnpj = registro["NumCNPJDistribuidora"]

            chave = (cnpj, distribuidora, inicio, te, tusd)

            tarifas[chave] = {
                "distribuidora": distribuidora,
                "cnpj": cnpj,
                "vigencia_inicio": inicio.isoformat(),
                "vigencia_fim": fim.isoformat(),
                "resolucao": registro["DscREH"],
                "tarifa_te": str(te),
                "tarifa_tusd": str(tusd),
                "tarifa_total": str(tarifa_total)
            }

        except (KeyError, ValueError, ArithmeticError):
            continue

    return list(tarifas.values())


def salvar_csv(tarifas):
    PASTA_DADOS.mkdir(exist_ok=True)

    if not tarifas:
        print("\nNenhuma tarifa vigente foi encontrada.")
        return

    campos = list(tarifas[0].keys())

    with open(ARQUIVO_SAIDA, "w", newline="", encoding="utf-8-sig") as arquivo:
        escritor = csv.DictWriter(
            arquivo,
            fieldnames=campos,
            delimiter=";"
        )

        escritor.writeheader()
        escritor.writerows(tarifas)

    print(f"\nArquivo gerado: {ARQUIVO_SAIDA}")
    print(f"Registros processados: {len(tarifas)}")


def main():
    print("Consultando tarifas da ANEEL...")

    try:
        registros = buscar_registros()
        tarifas = processar_registros(registros)
        salvar_csv(tarifas)

    except RuntimeError as erro:
        print(f"\nErro: {erro}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
