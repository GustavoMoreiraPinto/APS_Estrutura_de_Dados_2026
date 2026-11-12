
from pathlib import Path
import pandas as pd

pasta_dados = Path(__file__).parent / "dados"

arquivos = [
    "planilha_com_filtro.csv",
    "planilha_sem_filtro.csv"
]

data_inicio = pd.Timestamp("2021-08-20")
data_fim = pd.Timestamp("2025-08-20")

for nome_arquivo in arquivos:
    caminho = pasta_dados / nome_arquivo

    print("\n" + "=" * 50)
    print(f"Arquivo: {nome_arquivo}")

    if not caminho.exists():
        print("Arquivo não encontrado!")
        continue

    dados = pd.read_csv(caminho)

    # Converter as datas para o formato reconhecido pelo Python
    dados["viewDate"] = pd.to_datetime(
        dados["viewDate"],
        format="%d/%m/%Y",
        errors="coerce"
    )

    # Identificar os registros dentro do período exigido
    filtro_periodo = (
        (dados["viewDate"] >= data_inicio) &
        (dados["viewDate"] <= data_fim)
    )

    dados_periodo = dados.loc[filtro_periodo]

    print(f"Registros originais: {len(dados)}")
    print(f"Registros no período da APS: {len(dados_periodo)}")
    print(f"Registros fora do período ou sem data válida: {len(dados) - len(dados_periodo)}")

    # Verificar os valores numéricos utilizados na ordenação
    areas = pd.to_numeric(
        dados_periodo["areaMunKm"],
        errors="coerce"
    )

    print(f"Áreas numéricas válidas: {areas.notna().sum()}")
    print(f"Áreas ausentes ou inválidas: {areas.isna().sum()}")

    print("\nVerificação concluída!")
