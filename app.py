
import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="APS 2026/2 | Estrutura de Dados",
    page_icon="📊",
    layout="wide"
)

# Título principal
st.title("📊 APS 2026/2 — Estrutura de Dados")

st.write(
    "Sistema de Análise de Performance de Algoritmos "
    "de Ordenação Aplicados a Dados Ambientais"
)

# Menu lateral
st.sidebar.title("Menu de Navegação")

pagina = st.sidebar.radio(
    "Selecione uma página:",
    [
        "🏠 Visão Geral",
        "🌳 Dados com Filtro",
        "🌎 Dados sem Filtro",
        "📑 Relatório Técnico"
    ]
)

# Conteúdo das páginas
if pagina == "🏠 Visão Geral":
    st.header("Visão Geral")
    st.success("Bem-vindo ao nosso projeto de APS!")

elif pagina == "🌳 Dados com Filtro":
    st.header("Análise dos Dados com Filtro")
    st.info("Os resultados serão apresentados aqui.")

elif pagina == "🌎 Dados sem Filtro":
    st.header("Análise dos Dados sem Filtro")
    st.info("Os resultados serão apresentados aqui.")

elif pagina == "📑 Relatório Técnico":
    st.header("Relatório Técnico")
    st.info("A documentação será apresentada aqui.")
