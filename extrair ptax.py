import time
import logging
from datetime import datetime, timedelta
from pathlib import Path

import requests
import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

OUTPUT_DIR = Path(".")

# Endpoint correto: CotacaoMoedaPeriodo tem o campo tipoBoletim
# CotacaoDolarPeriodo NAO tem esse campo e retorna 400 se voce tentar seleciona-lo
BCB_URL = (
    "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/"
    "CotacaoMoedaPeriodo(moeda=@moeda,dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)"
    "?@moeda='USD'"
    "&@dataInicial='{start}'"
    "&@dataFinalCotacao='{end}'"
    "&$top=10000"
    "&$format=json"
    "&$select=cotacaoCompra,cotacaoVenda,dataHoraCotacao,tipoBoletim"
)


def download_chunk(start: str, end: str) -> pd.DataFrame:
    """Baixa um chunk. start/end no formato 'MM-DD-YYYY'."""
    url = BCB_URL.format(start=start, end=end)
    log.info(f"Requisicao: {start} -> {end}")

    r = requests.get(url, timeout=60)
    r.raise_for_status()
    data = r.json().get("value", [])

    if not data:
        return pd.DataFrame()

    df = pd.DataFrame(data)
    df.rename(columns={
        "cotacaoCompra":   "bid",
        "cotacaoVenda":    "ask",
        "dataHoraCotacao": "timestamp",
        "tipoBoletim":     "boletim",
    }, inplace=True)

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["mid"] = (df["bid"] + df["ask"]) / 2
    return df[["timestamp", "boletim", "bid", "ask", "mid"]]


def download_ptax(start_date: datetime, end_date: datetime,
                  boletim: str = "Fechamento") -> pd.DataFrame:
    """
    Baixa cotacoes PTAX USD/BRL para o periodo informado.

    boletim: "Fechamento" | "Abertura" | "Intermediario" | "todos"
    """
    all_frames = []
    current = start_date

    while current <= end_date:
        chunk_end = min(current + timedelta(days=364), end_date)
        try:
            df = download_chunk(
                current.strftime("%m-%d-%Y"),
                chunk_end.strftime("%m-%d-%Y")
            )
            if not df.empty:
                all_frames.append(df)
                log.info(f"  -> {len(df)} registros")
        except requests.HTTPError as e:
            log.error(f"Erro HTTP: {e}")

        current = chunk_end + timedelta(days=1)
        time.sleep(0.3)

    if not all_frames:
        log.warning("Nenhum dado retornado.")
        return pd.DataFrame()

    result = (pd.concat(all_frames, ignore_index=True)
                .drop_duplicates("timestamp")
                .sort_values("timestamp")
                .reset_index(drop=True))

    log.info(f"Total: {len(result)} | boletins: {result['boletim'].value_counts().to_dict()}")

    if boletim != "todos":
        result = result[result["boletim"] == boletim].reset_index(drop=True)
        log.info(f"Apos filtro '{boletim}': {len(result)} registros")

    return result



START   = datetime(2000, 1, 1)
END     = datetime(2024, 12, 31)
BOLETIM = "todos"   # opcoes: "Fechamento" | "Abertura" | "Intermediario" | "todos"

log.info("=" * 55)
log.info(f"  BCB PTAX | USD/BRL | {BOLETIM} | {START.date()} -> {END.date()}")
log.info("=" * 55)

df = download_ptax(START, END, boletim=BOLETIM)


