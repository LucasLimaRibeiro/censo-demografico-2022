
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ==========================================
# 1. CONFIGURAÇÃO DA PÁGINA
# ==========================================

st.set_page_config(
    page_title="Censo Demográfico 2022",
    page_icon="📊",
    layout="wide"
)

PASTA = Path(__file__).parent

ARQUIVO_POPULACAO = (
    PASTA / "data" / "processed" / "populacao_2022.csv.gz"
)

ARQUIVO_PERCENTUAL = (
    PASTA / "data" / "processed" / "percentual_populacao_2022.csv.gz"
)

REGIOES = [
    "Norte",
    "Nordeste",
    "Sudeste",
    "Sul",
    "Centro-Oeste"
]

# ==========================================
# 2. CARREGAMENTO DOS DADOS
# ==========================================

@st.cache_data
def carregar_dados():
    populacao = pd.read_csv(ARQUIVO_POPULACAO)
    percentual = pd.read_csv(ARQUIVO_PERCENTUAL)

    return populacao, percentual


try:
    df, df_percentual = carregar_dados()

except Exception as erro:
    st.error(f"Erro ao carregar os dados: {erro}")
    st.stop()


# ==========================================
# 3. CABEÇALHO
# ==========================================

st.title("📊 Censo Demográfico 2022")
st.subheader("Análise da população brasileira")

st.markdown("""
Projeto acadêmico desenvolvido para analisar a estrutura
demográfica brasileira a partir dos dados oficiais do IBGE.

**Disciplina:** Linguagem de Programação 

**Instituição:** Unilasalle

**Autores:** Lucas Lima Ribeiro e Gustavo Madruga
""")

st.divider()


# ==========================================
# 4. FILTROS
# ==========================================

st.sidebar.header("Filtros da análise")

nivel = st.sidebar.selectbox(
    "Localidade",
    ["Brasil", "Grandes Regiões", "Estados"]
)

if nivel == "Brasil":
    localidades = ["Brasil"]

elif nivel == "Grandes Regiões":
    localidades = REGIOES

else:
    localidades = [
        local for local in df["localidade"].unique()
        if local != "Brasil" and local not in REGIOES
    ]

localidade_selecionada = st.sidebar.selectbox(
    "Selecione a localidade",
    localidades
)

sexos = ["Total", "Homens", "Mulheres"]

sexo_selecionado = st.sidebar.selectbox(
    "Sexo",
    sexos
)

faixas = sorted(
    df.loc[
        (df["localidade"] == "Brasil") &
        (df["sexo"] == "Total") &
        (df["faixa_etaria"] != "Total"),
        "faixa_etaria"
    ].unique()
)

faixa_selecionada = st.sidebar.selectbox(
    "Faixa etária",
    ["Todas as idades"] + list(faixas)
)


# ==========================================
# 5. INDICADORES PRINCIPAIS
# ==========================================

dados_localidade = df[
    df["localidade"] == localidade_selecionada
]

total_brasil = df[
    (df["localidade"] == "Brasil") &
    (df["sexo"] == "Total") &
    (df["faixa_etaria"] == "Total")
]["valor"].iloc[0]

total_homens = df[
    (df["localidade"] == "Brasil") &
    (df["sexo"] == "Homens") &
    (df["faixa_etaria"] == "Total")
]["valor"].iloc[0]

total_mulheres = df[
    (df["localidade"] == "Brasil") &
    (df["sexo"] == "Mulheres") &
    (df["faixa_etaria"] == "Total")
]["valor"].iloc[0]

dados_filtrados = dados_localidade[
    (dados_localidade["sexo"] == sexo_selecionado)
]

if faixa_selecionada != "Todas as idades":
    dados_filtrados = dados_filtrados[
        dados_filtrados["faixa_etaria"] == faixa_selecionada
    ]
else:
    dados_filtrados = dados_filtrados[
        dados_filtrados["faixa_etaria"] == "Total"
    ]

total_selecionado = dados_filtrados["valor"].sum()

st.subheader("Indicadores demográficos")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "População brasileira",
    f"{total_brasil:,.0f}".replace(",", ".")
)

col2.metric(
    "Homens",
    f"{total_homens:,.0f}".replace(",", ".")
)

col3.metric(
    "Mulheres",
    f"{total_mulheres:,.0f}".replace(",", ".")
)

col4.metric(
    "População selecionada",
    f"{total_selecionado:,.0f}".replace(",", ".")
)

st.divider()


# ==========================================
# 6. DISTRIBUIÇÃO POR FAIXA ETÁRIA
# ==========================================

st.subheader("População por faixa etária")

dados_idade = df[
    (df["localidade"] == localidade_selecionada) &
    (df["sexo"] == sexo_selecionado) &
    (df["faixa_etaria"] != "Total")
].copy()

if not dados_idade.empty:

    fig_idade = px.bar(
        dados_idade,
        x="faixa_etaria",
        y="valor",
        title="Distribuição da população por faixa etária",
        labels={
            "faixa_etaria": "Faixa etária",
            "valor": "Habitantes"
        }
    )

    fig_idade.update_layout(
        xaxis_tickangle=-45
    )

    st.plotly_chart(
        fig_idade,
        use_container_width=True
    )


# ==========================================
# 7. COMPARAÇÃO ENTRE SEXOS
# ==========================================

st.subheader("Comparação entre homens e mulheres")

dados_sexo = df[
    (df["localidade"] == localidade_selecionada) &
    (df["sexo"].isin(["Homens", "Mulheres"])) &
    (df["faixa_etaria"] != "Total")
]

fig_sexo = px.line(
    dados_sexo,
    x="faixa_etaria",
    y="valor",
    color="sexo",
    markers=True,
    title="População por sexo e faixa etária",
    labels={
        "faixa_etaria": "Faixa etária",
        "valor": "Habitantes",
        "sexo": "Sexo"
    }
)

fig_sexo.update_layout(
    xaxis_tickangle=-45
)

st.plotly_chart(
    fig_sexo,
    use_container_width=True
)


# ==========================================
# 8. DISTRIBUIÇÃO REGIONAL
# ==========================================

st.subheader("População por Grande Região")

dados_regioes = df[
    (df["localidade"].isin(REGIOES)) &
    (df["sexo"] == "Total") &
    (df["faixa_etaria"] == "Total")
].copy()

dados_regioes = dados_regioes.sort_values(
    "valor",
    ascending=False
)

fig_regioes = px.bar(
    dados_regioes,
    x="localidade",
    y="valor",
    title="População residente por Grande Região",
    labels={
        "localidade": "Região",
        "valor": "Habitantes"
    }
)

st.plotly_chart(
    fig_regioes,
    use_container_width=True
)


# ==========================================
# 9. RANKING DOS ESTADOS
# ==========================================

st.subheader("Ranking populacional dos estados")

dados_estados = df[
    (df["sexo"] == "Total") &
    (df["faixa_etaria"] == "Total")
].copy()

dados_estados = dados_estados[
    ~dados_estados["localidade"].isin(
        ["Brasil"] + REGIOES
    )
]

dados_estados = dados_estados.sort_values(
    "valor",
    ascending=False
)

fig_estados = px.bar(
    dados_estados.head(10).sort_values("valor"),
    x="valor",
    y="localidade",
    orientation="h",
    title="10 estados mais populosos",
    labels={
        "localidade": "Estado",
        "valor": "Habitantes"
    }
)

st.plotly_chart(
    fig_estados,
    use_container_width=True
)


# ==========================================
# 10. TABELA DE DADOS
# ==========================================

st.subheader("Consulta aos dados")

st.markdown("""
A tabela abaixo apresenta os registros correspondentes
à localidade, sexo e faixa etária selecionados.
""")

st.dataframe(
    dados_localidade[
        dados_localidade["sexo"] == sexo_selecionado
    ],
    use_container_width=True,
    hide_index=True
)


# ==========================================
# 11. FONTE E RODAPÉ
# ==========================================

st.divider()

st.markdown("""
**Fonte:** Instituto Brasileiro de Geografia e Estatística (IBGE).

**Pesquisa:** Censo Demográfico 2022 — Tabela 9514.

**Tratamento:** Python, Pandas e NumPy.

**Visualização:** Plotly e Streamlit.

Projeto acadêmico — Unilasalle — 2026.2.
""")
