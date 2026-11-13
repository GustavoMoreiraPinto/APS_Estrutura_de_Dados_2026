# APS_Estrutura_de_Dados_2026
APS_Estrutura_de_Dados_2026
# Análise de Performance de Algoritmos de Ordenação Aplicados a Dados Ambientais

**Atividade Prática Supervisionada (APS) — Estrutura de Dados**  
Universidade Paulista (UNIP) | 2026

## Sobre o projeto

Este projeto apresenta uma análise experimental do desempenho de cinco algoritmos de ordenação, utilizando dados ambientais de avisos de desmatamento disponibilizados pelo Instituto Nacional de Pesquisas Espaciais (INPE), por meio da plataforma TerraBrasilis.

O objetivo é comparar o comportamento computacional dos algoritmos em diferentes condições de entrada, relacionando os tempos de execução observados às suas respectivas complexidades assintóticas.

A aplicação inclui um dashboard interativo desenvolvido em Python e Streamlit para exploração e visualização dos resultados.

## Algoritmos implementados

- Bubble Sort (otimizado)
- Selection Sort
- Insertion Sort
- Merge Sort
- Quick Sort (iterativo, com pivô aleatório)

Cada algoritmo foi implementado em Python e validado quanto à correção da ordenação.

## Base de dados

**Fonte:** INPE — TerraBrasilis  
**Tema:** Avisos de desmatamento no bioma Amazônia  
**Período analisado:** 20/08/2021 a 20/08/2025  
**Variável utilizada na ordenação:** `areaMunKm`

Foram considerados dois conjuntos de dados, identificados como *com filtro* e *sem filtro*.

Após a delimitação temporal e a validação dos valores numéricos, foram selecionadas amostras reproduzíveis de 3.000 registros por conjunto, utilizando `random_state=42`.

Os resultados do benchmark correspondem às amostras, e não à ordenação integral das bases originais.

## Metodologia experimental

Os algoritmos foram avaliados em dois cenários:

1. **Ordem decrescente:** registros inicialmente organizados do maior para o menor valor.
2. **Ordem aleatória:** registros organizados em sequência pseudoaleatória.

Cada combinação de algoritmo, conjunto de dados e cenário foi executada 10 vezes, totalizando **200 medições**.

Os tempos de execução foram registrados em segundos utilizando `time.perf_counter()`.

As análises incluem média, mediana, valores mínimo e máximo e desvio padrão.

## Complexidade computacional

| Algoritmo | Melhor caso | Caso médio | Pior caso |
|---|---|---|---|
| Bubble Sort otimizado | Ω(n) | Θ(n²) | O(n²) |
| Selection Sort | Ω(n²) | Θ(n²) | O(n²) |
| Insertion Sort | Ω(n) | Θ(n²) | O(n²) |
| Merge Sort | Ω(n log n) | Θ(n log n) | O(n log n) |
| Quick Sort | Ω(n log n) | Θ(n log n) | O(n²) |

As classificações representam os limites assintóticos usuais dos respectivos casos, considerando as implementações utilizadas.

## Resultados

Nos experimentos realizados com amostras de 3.000 registros, o **Merge Sort apresentou o menor tempo médio de execução nos quatro recortes analisados**.

Os algoritmos quadráticos apresentaram tempos superiores aos algoritmos de complexidade média O(n log n), nas condições avaliadas.

Essas observações são específicas das implementações, amostras e condições experimentais utilizadas.

## Dashboard interativo

O dashboard desenvolvido com Streamlit disponibiliza:

- Visão geral dos experimentos e indicadores;
- Filtros por cenário e conjunto de dados;
- Gráficos comparativos com escala linear ou logarítmica;
- Ranking dos algoritmos por tempo médio;
- Visualização da distribuição das medições;
- Estatísticas descritivas dos experimentos;
- Tabela de complexidade computacional;
- Exportação dos resultados em CSV.

## Tecnologias utilizadas

- **Python:** implementação dos algoritmos e processamento dos dados;
- **Pandas e NumPy:** manipulação e análise de dados;
- **Streamlit:** interface interativa;
- **Plotly:** gráficos e visualizações;
- **Matplotlib:** suporte à visualização;
- **Git e GitHub:** versionamento do projeto.

## Como executar

### 1. Clonar o repositório

```bash
git clone https://github.com/GustavoMoreiraPinto/APS_Estrutura_de_Dados_2026.git
cd APS_Estrutura_de_Dados_2026
```

### 2. Criar e ativar o ambiente virtual

No Windows:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 4. Executar o dashboard

```bash
python -m streamlit run app.py
```

O dashboard utiliza o arquivo `resultados/tempos_execucao.csv`, gerado pelo processo experimental.

Para reproduzir as medições, é necessário disponibilizar os arquivos de entrada esperados na pasta `dados` e executar:

```bash
python medir_desempenho.py
```

## Limitações

A análise considera amostras de tamanho fixo e não mede diretamente o consumo de memória. Além disso, os resultados dependem das características do computador, da implementação dos algoritmos e da distribuição dos dados.

A avaliação experimental complementa a análise teórica de complexidade, mas não demonstra, isoladamente, o comportamento assintótico para diferentes tamanhos de entrada.

## Fonte dos dados

Instituto Nacional de Pesquisas Espaciais (INPE). **TerraBrasilis**.

https://terrabrasilis.dpi.inpe.br/

## Contexto acadêmico

Projeto desenvolvido para a disciplina de **Estrutura de Dados**, no âmbito da Atividade Prática Supervisionada (APS) da Universidade Paulista (UNIP).

**Ano:** 2026.