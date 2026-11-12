
from pathlib import Path
import pandas as pd

PASTA_DADOS = Path(__file__).parent / "dados"

DATA_INICIO = pd.Timestamp("2021-08-20")
DATA_FIM = pd.Timestamp("2025-08-20")


def carregar_areas(nome_arquivo, tamanho_amostra=3000):
    caminho = PASTA_DADOS / nome_arquivo

    dados = pd.read_csv(caminho)

    # Converter a coluna de datas
    dados["viewDate"] = pd.to_datetime(
        dados["viewDate"],
        format="%d/%m/%Y",
        errors="coerce"
    )

    # Selecionar somente o período da APS
    dados = dados.loc[
        dados["viewDate"].between(DATA_INICIO, DATA_FIM)
    ].copy()

    # Converter as áreas para valores numéricos
    dados["areaMunKm"] = pd.to_numeric(
        dados["areaMunKm"],
        errors="coerce"
    )

    # Remover registros sem área válida
    dados = dados.dropna(subset=["areaMunKm"])

    # Selecionar uma amostra reproduzível
    if tamanho_amostra is not None:
        dados = dados.sample(
            n=min(tamanho_amostra, len(dados)),
            random_state=42
        )

    return dados["areaMunKm"].tolist()


if __name__ == "__main__":
    com_filtro = carregar_areas("planilha_com_filtro.csv")
    sem_filtro = carregar_areas("planilha_sem_filtro.csv")

    print("Dados com filtro:", len(com_filtro))
    print("Dados sem filtro:", len(sem_filtro))

    print("\nPrimeiras 5 áreas com filtro:")
    print(com_filtro[:5])

    print("\nPrimeiras 5 áreas sem filtro:")
    print(sem_filtro[:5])
