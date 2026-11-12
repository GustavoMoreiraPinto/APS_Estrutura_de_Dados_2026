
import random
import time
from pathlib import Path

import pandas as pd

from preparar_dados import carregar_areas

from algoritmos.bubble_sort import bubble_sort
from algoritmos.selection_sort import selection_sort
from algoritmos.insertion_sort import insertion_sort
from algoritmos.merge_sort import merge_sort
from algoritmos.quick_sort import quick_sort


ALGORITMOS = {
    "Bubble Sort": bubble_sort,
    "Selection Sort": selection_sort,
    "Insertion Sort": insertion_sort,
    "Merge Sort": merge_sort,
    "Quick Sort": quick_sort,
}

REPETICOES = 10
PASTA_RESULTADOS = Path(__file__).parent / "resultados"


def medir_tempo(algoritmo, lista, esperado):
    copia = lista.copy()

    inicio = time.perf_counter()
    resultado = algoritmo(copia)
    tempo = time.perf_counter() - inicio

    if resultado != esperado:
        raise ValueError("O algoritmo não ordenou corretamente!")

    return tempo


def executar_testes(nome_arquivo, nome_conjunto):
    areas = carregar_areas(nome_arquivo)

    decrescente = sorted(areas, reverse=True)

    aleatoria = areas.copy()
    random.Random(42).shuffle(aleatoria)

    cenarios = {
        "Decrescente": decrescente,
        "Aleatoria": aleatoria,
    }

    resultados = []

    print(f"\nConjunto: {nome_conjunto}")

    for nome_cenario, lista in cenarios.items():
        esperado = sorted(lista)

        print(f"\nCenário: {nome_cenario}")

        for nome_algoritmo, algoritmo in ALGORITMOS.items():
            tempos = []

            for repeticao in range(1, REPETICOES + 1):
                tempo = medir_tempo(
                    algoritmo,
                    lista,
                    esperado
                )

                tempos.append(tempo)

                resultados.append({
                    "conjunto": nome_conjunto,
                    "cenario": nome_cenario,
                    "algoritmo": nome_algoritmo,
                    "repeticao": repeticao,
                    "quantidade_registros": len(lista),
                    "tempo_segundos": tempo,
                })

            media = sum(tempos) / len(tempos)

            print(
                f"{nome_algoritmo:<18} "
                f"Média: {media:.6f} s"
            )

    return resultados


if __name__ == "__main__":
    todos_resultados = []

    todos_resultados.extend(
        executar_testes(
            "planilha_com_filtro.csv",
            "Com filtro"
        )
    )

    todos_resultados.extend(
        executar_testes(
            "planilha_sem_filtro.csv",
            "Sem filtro"
        )
    )

    PASTA_RESULTADOS.mkdir(
        parents=True,
        exist_ok=True
    )

    tabela = pd.DataFrame(todos_resultados)

    caminho_saida = (
        PASTA_RESULTADOS / "tempos_execucao.csv"
    )

    tabela.to_csv(
        caminho_saida,
        index=False,
        encoding="utf-8-sig"
    )

    print("\n" + "=" * 55)
    print("Experimentos concluídos!")
    print(f"Total de medições: {len(tabela)}")
    print(f"Resultados salvos em: {caminho_saida}")
