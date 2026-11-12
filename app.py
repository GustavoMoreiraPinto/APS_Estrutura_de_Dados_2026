from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="APS | Laboratório de Ordenação", page_icon="📊", layout="wide", initial_sidebar_state="expanded")
BASE = Path(__file__).resolve().parent
ARQUIVO = BASE / "resultados" / "tempos_execucao.csv"
ORDEM = ["Bubble Sort", "Selection Sort", "Insertion Sort", "Merge Sort", "Quick Sort"]
CORES = {"Bubble Sort": "#D47A67", "Selection Sort": "#C99A55", "Insertion Sort": "#8A8BC4", "Merge Sort": "#46A99B", "Quick Sort": "#5B91C8"}

st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');
html,body,[class*="css"], [data-testid="stApp"] {font-family:'DM Sans',sans-serif;}
[data-testid="stAppViewContainer"] {background:#F6F8FB;color:#18263B;}
[data-testid="stSidebar"] {background:#101E32;}
[data-testid="stSidebar"] * {color:#E9EFF8 !important;}
[data-testid="stSidebar"] [role="radiogroup"] label {padding:8px 9px;border-radius:8px;}
.block-container {padding-top:2rem;max-width:1380px;}
h1,h2,h3 {font-family:'Manrope',sans-serif;letter-spacing:-.025em;}
h1 {font-weight:800 !important;}
[data-testid="stMetric"] {background:#fff;border:1px solid #E4EAF1;border-radius:13px;padding:18px 20px;box-shadow:0 3px 16px #20314908;}
[data-testid="stMetricLabel"] {color:#63738A;}
[data-testid="stMetricValue"] {color:#172C46;font-weight:800;}
[data-testid="stPlotlyChart"], [data-testid="stDataFrame"] {background:white;border:1px solid #E4EAF1;border-radius:13px;padding:10px;}
.section-kicker {font-size:12px;font-weight:800;letter-spacing:.16em;color:#367C91;text-transform:uppercase;margin-bottom:6px;}
.hero-note {color:#64748B;font-size:15px;line-height:1.7;margin-bottom:18px;}
.pill {display:inline-block;background:#E7F4F1;color:#257C71;padding:5px 11px;border-radius:99px;font-size:12px;font-weight:700;}
footer {visibility:hidden;}
</style>""", unsafe_allow_html=True)

@st.cache_data(show_spinner=False)
def carregar(caminho, modificado):
    df = pd.read_csv(caminho)
    colunas = {"conjunto", "cenario", "algoritmo", "repeticao", "quantidade_registros", "tempo_segundos"}
    faltando = colunas - set(df.columns)
    if faltando:
        raise ValueError("Colunas ausentes no CSV: " + ", ".join(sorted(faltando)))
    df["tempo_segundos"] = pd.to_numeric(df["tempo_segundos"], errors="coerce")
    df["quantidade_registros"] = pd.to_numeric(df["quantidade_registros"], errors="coerce")
    df = df.dropna(subset=["tempo_segundos", "quantidade_registros"])
    df = df[df["tempo_segundos"] > 0].copy()
    return df

def formato(segundos):
    return f"{segundos:.6f} s".replace(".", ",")

def estilizar(fig, altura=480, log=False):
    fig.update_layout(
        template="plotly_white", height=altura,
        font=dict(family="DM Sans, Arial", color="#30435D"),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#FFFFFF",
        margin=dict(l=18,r=18,t=45,b=18),
        legend_title_text="", hovermode="closest",
    )
    fig.update_xaxes(showgrid=False, linecolor="#E6EBF1", tickfont=dict(size=11))
    fig.update_yaxes(type="log" if log else "linear", gridcolor="#ECF0F5", zeroline=False)
    return fig

def csv_bytes(df):
    return df.to_csv(index=False, sep=";", decimal=",").encode("utf-8-sig")

st.sidebar.markdown("### ◈ APS / ESTRUTURA DE DADOS")
st.sidebar.caption("Laboratório de performance · 2026")
st.sidebar.divider()
pagina = st.sidebar.radio("NAVEGAÇÃO", ["Visão geral", "Dados com filtro", "Dados sem filtro", "Relatório técnico"], label_visibility="collapsed")
st.sidebar.divider()
st.sidebar.caption("FONTE DOS DADOS")
st.sidebar.markdown("**INPE · TerraBrasilis**")
st.sidebar.caption("Avisos de desmatamento · Bioma Amazônia")
st.sidebar.caption("Período: 20/08/2021 a 20/08/2025")
st.sidebar.caption("Variável: área municipal (km²)")

if not ARQUIVO.exists():
    st.error("Não encontrei `resultados/tempos_execucao.csv`. Execute `python medir_desempenho.py` na pasta do projeto.")
    st.stop()
try:
    dados = carregar(str(ARQUIVO), ARQUIVO.stat().st_mtime)
except Exception as exc:
    st.error(f"Não foi possível carregar os resultados: {exc}")
    st.stop()
if dados.empty:
    st.warning("O CSV de resultados está vazio ou não contém tempos válidos.")
    st.stop()

resumo = dados.groupby(["conjunto", "cenario", "algoritmo"], as_index=False).agg(
    media=("tempo_segundos", "mean"), mediana=("tempo_segundos", "median"),
    minimo=("tempo_segundos", "min"), maximo=("tempo_segundos", "max"),
    desvio_padrao=("tempo_segundos", "std"), repeticoes=("tempo_segundos", "count")
)
resumo["desvio_padrao"] = resumo["desvio_padrao"].fillna(0)
algoritmos = [a for a in ORDEM if a in dados["algoritmo"].unique()] + [a for a in dados["algoritmo"].unique() if a not in ORDEM]

st.markdown('<div class="section-kicker">UNIP · APS · ESTRUTURA DE DADOS</div>', unsafe_allow_html=True)
st.title("Análise de performance de algoritmos")
st.markdown('<div class="hero-note">Benchmark de cinco métodos de ordenação aplicados a amostras de dados ambientais do INPE. Comparação de tempos, cenários e complexidade computacional.</div>', unsafe_allow_html=True)

if pagina == "Visão geral":
    a,b,c,d = st.columns(4)
    a.metric("Algoritmos", dados["algoritmo"].nunique())
    b.metric("Execuções medidas", f"{len(dados):,}".replace(",", "."))
    c.metric("Registros por amostra", f"{int(dados['quantidade_registros'].median()):,}".replace(",", "."))
    d.metric("Cenários", dados["cenario"].nunique())
    st.write("")
    st.subheader("Panorama dos experimentos")
    col_f1,col_f2,col_f3 = st.columns([1,1,1])
    with col_f1:
        cenarios = st.multiselect("Cenário", sorted(dados["cenario"].unique()), default=sorted(dados["cenario"].unique()))
    with col_f2:
        conjuntos = st.multiselect("Conjunto", sorted(dados["conjunto"].unique()), default=sorted(dados["conjunto"].unique()))
    with col_f3:
        escala = st.toggle("Escala logarítmica", value=False, help="Exibe diferenças entre tempos de ordens de grandeza distintas.")
    selecionados = resumo[resumo["cenario"].isin(cenarios) & resumo["conjunto"].isin(conjuntos)].copy()
    if selecionados.empty:
        st.info("Selecione pelo menos um cenário e um conjunto para visualizar os resultados.")
    else:
        grafico = px.bar(selecionados, x="algoritmo", y="media", color="algoritmo", facet_col="cenario", facet_row="conjunto",
                         category_orders={"algoritmo":algoritmos}, color_discrete_map=CORES,
                         labels={"algoritmo":"Algoritmo", "media":"Tempo médio (s)", "cenario":"Cenário", "conjunto":"Conjunto"},
                         hover_data={"media":":.6f", "repeticoes":True})
        grafico.update_layout(showlegend=False)
        st.plotly_chart(estilizar(grafico, altura=650 if len(cenarios)>1 and len(conjuntos)>1 else 460, log=escala), use_container_width=True)
        if escala:
            st.caption("Escala logarítmica: os intervalos do eixo Y são multiplicativos; a altura visual das barras não representa uma proporção linear.")
        st.subheader("Ranking por tempo médio")
        ranking = (selecionados.groupby("algoritmo",as_index=False)["media"].mean().sort_values("media").reset_index(drop=True))
        ranking.insert(0,"Posição",range(1,len(ranking)+1))
        ranking["Tempo médio (s)"] = ranking["media"].map(lambda x: f"{x:.6f}")
        esquerda,direita=st.columns([1.3,1])
        with esquerda:
            st.dataframe(ranking[["Posição","algoritmo","Tempo médio (s)"]].rename(columns={"algoritmo":"Algoritmo"}),hide_index=True,use_container_width=True)
        with direita:
            melhor=ranking.iloc[0]
            pior=ranking.iloc[-1]
            st.markdown("**Destaque do recorte selecionado**")
            st.metric("Menor tempo médio",str(melhor["algoritmo"]),formato(float(melhor["media"])))
            if len(ranking)>1 and melhor["media"]>0:
                st.caption(f"Neste recorte, {pior['algoritmo']} levou aproximadamente {pior['media']/melhor['media']:.1f}× o tempo de {melhor['algoritmo']}.")
            st.caption("O ranking reflete apenas as amostras e condições medidas; não é uma classificação universal.")
    st.divider()
    st.subheader("Exportar resultados")
    x,y=st.columns(2)
    with x:
        st.download_button("Baixar medições completas (CSV)",csv_bytes(dados),"medicoes_completas.csv","text/csv",use_container_width=True)
    with y:
        st.download_button("Baixar estatísticas consolidadas (CSV)",csv_bytes(resumo),"estatisticas_algoritmos.csv","text/csv",use_container_width=True)

elif pagina in ["Dados com filtro", "Dados sem filtro"]:
    conjunto = "Com filtro" if pagina=="Dados com filtro" else "Sem filtro"
    recorte = resumo[resumo["conjunto"].str.casefold()==conjunto.casefold()].copy()
    st.subheader(f"Conjunto: {conjunto.lower()}")
    st.caption("Cada barra representa a média das execuções registradas para um algoritmo e cenário.")
    if recorte.empty:
        st.warning(f"Não há resultados identificados como '{conjunto}' no arquivo CSV.")
    else:
        c1,c2,c3=st.columns(3)
        c1.metric("Algoritmos avaliados",recorte["algoritmo"].nunique())
        c2.metric("Cenários avaliados",recorte["cenario"].nunique())
        c3.metric("Medições no conjunto",int(dados["conjunto"].str.casefold().eq(conjunto.casefold()).sum()))
        st.write("")
        escala = st.toggle("Escala logarítmica",value=False)
        fig=px.bar(recorte,x="algoritmo",y="media",color="cenario",barmode="group",category_orders={"algoritmo":algoritmos},
                   labels={"algoritmo":"Algoritmo", "media":"Tempo médio (s)", "cenario":"Cenário"},
                   hover_data={"media":":.6f","desvio_padrao":":.6f","repeticoes":True})
        st.plotly_chart(estilizar(fig,520,escala),use_container_width=True)
        st.subheader("Consistência das medições")
        fig2=px.box(dados[dados["conjunto"].str.casefold()==conjunto.casefold()],x="algoritmo",y="tempo_segundos",color="cenario",points="all",
                    category_orders={"algoritmo":algoritmos},labels={"algoritmo":"Algoritmo", "tempo_segundos":"Tempo (s)","cenario":"Cenário"})
        st.plotly_chart(estilizar(fig2,480,escala),use_container_width=True)
        st.caption("Cada ponto corresponde a uma execução. A caixa resume a dispersão dos tempos medidos.")
        st.subheader("Estatísticas por algoritmo")
        tabela=recorte.rename(columns={"algoritmo":"Algoritmo","cenario":"Cenário","media":"Média (s)","mediana":"Mediana (s)","minimo":"Mínimo (s)","maximo":"Máximo (s)","desvio_padrao":"Desvio padrão (s)","repeticoes":"Execuções"})
        st.dataframe(tabela[["Algoritmo","Cenário","Média (s)","Mediana (s)","Mínimo (s)","Máximo (s)","Desvio padrão (s)","Execuções"]],hide_index=True,use_container_width=True,
                     column_config={k:st.column_config.NumberColumn(format="%.6f") for k in ["Média (s)","Mediana (s)","Mínimo (s)","Máximo (s)","Desvio padrão (s)"]})
        st.download_button("Baixar estatísticas deste conjunto",csv_bytes(recorte),f"estatisticas_{conjunto.lower().replace(' ','_')}.csv","text/csv")

else:
    st.subheader("Relatório técnico")
    st.markdown("""### Objetivo e origem dos dados
Comparar o desempenho de **Bubble Sort, Selection Sort, Insertion Sort, Merge Sort e Quick Sort** ao ordenar a variável **`areaMunKm`** de dados de avisos de desmatamento do INPE/TerraBrasilis, considerando o período de **20/08/2021 a 20/08/2025**.

### Procedimento experimental
Foram preparados dois conjuntos de dados, denominados **com filtro** e **sem filtro**. Após a delimitação do período e a validação da variável numérica, foram extraídas **amostras reproduzíveis de 3.000 registros por conjunto**, com `random_state=42`. Cada algoritmo foi avaliado com entradas inicialmente **aleatórias** e **em ordem decrescente**, realizando-se **10 medições por combinação**, com `time.perf_counter()`. Os resultados apresentados são médias e estatísticas das execuções registradas no CSV.

**Atenção:** os resultados se referem às amostras de 3.000 registros, não ao processamento integral das bases originais.
""")
    st.subheader("Complexidade assintótica")
    complexidades=pd.DataFrame([
        ["Bubble Sort (otimizado)","Ω(n)","Θ(n²)","O(n²)","O(1)"],
        ["Selection Sort","Ω(n²)","Θ(n²)","O(n²)","O(1)"],
        ["Insertion Sort","Ω(n)","Θ(n²)","O(n²)","O(1)"],
        ["Merge Sort","Ω(n log n)","Θ(n log n)","O(n log n)","O(n)"],
        ["Quick Sort*","Ω(n log n)","Θ(n log n)","O(n²)","O(n) no pior caso"],
    ],columns=["Algoritmo","Melhor caso","Caso médio","Pior caso","Espaço auxiliar"])
    st.dataframe(complexidades,hide_index=True,use_container_width=True)
    st.caption("Ω, Θ e O indicam limites assintóticos; aqui, as colunas apresentam os limites usuais dos casos melhor, médio e pior. *Quick Sort: implementação iterativa com pivô aleatório; o espaço auxiliar depende da pilha de partições.")
    st.markdown("""### Interpretação dos resultados
- **Merge Sort** tende a apresentar bom desempenho em conjuntos maiores graças à complexidade `O(n log n)`, com custo adicional de memória.
- **Quick Sort** possui desempenho médio `Θ(n log n)`, mas seu pior caso teórico continua sendo `O(n²)`, mesmo com escolha aleatória do pivô.
- **Bubble Sort, Selection Sort e Insertion Sort** têm custo quadrático no caso médio, embora o Insertion Sort e o Bubble Sort otimizado possam aproveitar entradas já ordenadas.
- A comparação empírica deve ser interpretada **dentro das condições testadas**: máquina, implementação, amostra e distribuição dos dados.

### Limitações
O estudo usa amostras de tamanho fixo, não mede consumo de memória e não permite, sozinho, demonstrar experimentalmente as curvas assintóticas em função de diferentes valores de `n`. Os tempos também podem variar com a carga do computador.

### Documentação acadêmica
Este painel é um instrumento de visualização. O **relatório acadêmico em Word, conforme as normas ABNT**, será elaborado separadamente, com introdução, fundamentação teórica, metodologia, resultados, discussão, conclusão e referências.
""")
    st.subheader("Resumo consolidado dos resultados")
    st.dataframe(resumo,hide_index=True,use_container_width=True)
    st.download_button("Baixar dados consolidados",csv_bytes(resumo),"resultados_consolidados.csv","text/csv")

st.divider()
st.caption("APS · Estrutura de Dados · UNIP | Análise experimental de algoritmos de ordenação | Fonte: INPE / TerraBrasilis")
