import streamlit as st
import pandas as pd
import plotly.express as px

# ===============================
# CONFIG STREAMLIT
# ===============================
st.set_page_config(page_title="Consumo Garden Itaqua", layout="wide")
st.title("📊 Consumo de Energia – Shopping Garden Itaqua")

# ===============================
# PALETA DE CORES
# ===============================
PALETA_CORES = ["#1f77b4", "#2ca02c", "#ff7f0e"]

# ===============================
# LEITURA DO EXCEL
# ===============================
arquivo_excel = "ConsumoDiario.xlsx"

df_raw = pd.read_excel(
    arquivo_excel,
    sheet_name=0,
    header=None
)

# ===============================
# DATA DE REFERÊNCIA (C2)
# ===============================
data_referencia = pd.to_datetime(df_raw.iloc[1, 2])
data_ref_fmt = data_referencia.strftime("%d/%m/%Y")

# ===============================
# GRÁFICO 1 – CONSUMO DIÁRIO (MWh)
# ===============================
df_diario = pd.read_excel(
    arquivo_excel,
    sheet_name=0,
    usecols="B,D",
    skiprows=4,
    nrows=24
)

df_diario.columns = ["Data", "Consumo_MWh"]
df_diario["Data"] = pd.to_datetime(df_diario["Data"])

fig_diario = px.bar(
    df_diario,
    x="Data",
    y="Consumo_MWh",
    title="Consumo Diário (MWh)",
    labels={"Data": "Data", "Consumo_MWh": "Consumo (MWh)"},
    color_discrete_sequence=[PALETA_CORES[0]]
)

fig_diario.update_layout(
    xaxis_tickformat="%d/%m",
    bargap=0.15
)

fig_diario.update_traces(
    texttemplate="%{y:.1f}",
    textposition="outside"
)

# ===============================
# GRÁFICO 2 – CONSUMO HORÁRIO (MWh)
# ===============================
df_horario = pd.read_excel(
    arquivo_excel,
    sheet_name=0,
    usecols="D",
    skiprows=4,
    nrows=24
)

df_horario.columns = ["Consumo_MWh"]
df_horario["Hora"] = range(1, 25)

fig_horario = px.bar(
    df_horario,
    x="Hora",
    y="Consumo_MWh",
    title=f"Consumo Horário (MWh) – Referente a {data_ref_fmt}",
    labels={"Hora": "Hora do dia", "Consumo_MWh": "Consumo (MWh)"},
    color_discrete_sequence=[PALETA_CORES[1]]
)

fig_horario.update_layout(
    xaxis=dict(tickmode="linear", tick0=1, dtick=1),
    bargap=0.2
)

fig_horario.update_traces(
    texttemplate="%{y:.1f}",
    textposition="outside"
)

# ===============================
# GRÁFICO 3 – CONSUMO MENSAL (MWh)
# (GERADO A PARTIR DO DIÁRIO)
# ===============================
df_mensal = df_diario.copy()
df_mensal["Mes_Ano"] = df_mensal["Data"].dt.strftime("%m/%Y")

df_mensal = (
    df_mensal
    .groupby("Mes_Ano", as_index=False)["Consumo_MWh"]
    .sum()
)

fig_mensal = px.bar(
    df_mensal,
    x="Mes_Ano",
    y="Consumo_MWh",
    title="Consumo Mensal (MWh)",
    labels={"Mes_Ano": "Mês/Ano", "Consumo_MWh": "Consumo (MWh)"},
    color_discrete_sequence=[PALETA_CORES[2]]
)

fig_mensal.update_layout(
    xaxis_tickangle=-45,
    bargap=0.25
)

fig_mensal.update_traces(
    texttemplate="%{y:.1f}",
    textposition="outside"
)

# ===============================
# EXIBIÇÃO
# ===============================
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig_diario, use_container_width=True)

with col2:
    st.plotly_chart(fig_horario, use_container_width=True)

st.plotly_chart(fig_mensal, use_container_width=True)
