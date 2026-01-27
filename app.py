import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Shopping Garden Itaqua",
    layout="wide"
)

# =========================
# CONFIGURAÇÕES
# =========================
arquivo_excel = "ConsumoDiario.xlsx"
paleta_diario = ["#90bf3b"]
paleta_horario = ["#263a64"]
paleta_mensal = ["#a3afc4"]

# =========================
# TÍTULO PRINCIPAL
# =========================
st.title("🏬 Shopping Garden Itaqua")
st.markdown(
    "📊 **Dashboard de Consumo de Energia Elétrica**",
    unsafe_allow_html=True
)

st.divider()

# =========================
# GRÁFICO 1 — CONSUMO DIÁRIO (MWh)
# Aba: Tabela
# =========================
df_diario = pd.read_excel(
    arquivo_excel,
    sheet_name="Tabela",
    header=0
)

df_diario = df_diario.iloc[:, [0, 3]]
df_diario.columns = ["Data", "Consumo_MWh"]
df_diario["Data"] = pd.to_datetime(df_diario["Data"])

fig_diario = px.bar(
    df_diario,
    x="Data",
    y="Consumo_MWh",
    text=df_diario["Consumo_MWh"].round(1),
    title="📅 Consumo Diário de Energia (MWh)",
    color_discrete_sequence=paleta_diario
)

fig_diario.update_layout(
    xaxis_title="Data",
    yaxis_title="MWh",
    xaxis_tickformat="%d/%m",
    xaxis_tickangle=-45,
    bargap=0.25
)

fig_diario.update_traces(
    textposition="outside",
    textfont_size=14
)

st.plotly_chart(fig_diario, use_container_width=True)

st.divider()

# =========================
# GRÁFICO 2 — CONSUMO HORÁRIO (MWh)
# Aba: Tabela2
# =========================
df_horario = pd.read_excel(
    arquivo_excel,
    sheet_name="Tabela2",
    header=3,
    usecols="B:D"
)

df_horario.columns = ["Hora", "Ignorar", "Consumo_MWh"]
df_horario = df_horario[["Hora", "Consumo_MWh"]]

fig_horario = px.bar(
    df_horario,
    x="Hora",
    y="Consumo_MWh",
    text=df_horario["Consumo_MWh"].round(1),
    title="⏱️ Consumo Horário de Energia (MWh) — Dia Anterior",
    color_discrete_sequence=paleta_horario
)

fig_horario.update_layout(
    xaxis_title="Hora do Dia",
    yaxis_title="MWh",
    xaxis_tickmode="linear",
    xaxis_tick0=1,
    xaxis_dtick=1,
    bargap=0.2
)

fig_horario.update_traces(
    textposition="outside",
    textfont_size=14
)

st.plotly_chart(fig_horario, use_container_width=True)

st.divider()

# =========================
# GRÁFICO 3 — CONSUMO MENSAL (MWh)
# Aba: Tabela3
# =========================
df_mensal = pd.read_excel(
    arquivo_excel,
    sheet_name="Tabela3",
    header=0
)

df_mensal = df_mensal.iloc[:, [0, 4]]
df_mensal.columns = ["Data", "Consumo_MWh"]
df_mensal["Data"] = pd.to_datetime(df_mensal["Data"])
df_mensal["MesAno"] = df_mensal["Data"].dt.strftime("%m/%Y")

df_mensal_agg = df_mensal.groupby(
    "MesAno", as_index=False
)["Consumo_MWh"].sum()

fig_mensal = px.bar(
    df_mensal_agg,
    x="MesAno",
    y="Consumo_MWh",
    text=df_mensal_agg["Consumo_MWh"].round(1),
    title="📈 Consumo Mensal de Energia (MWh)",
    color_discrete_sequence=paleta_mensal
)

fig_mensal.update_layout(
    xaxis_title="Mês / Ano",
    yaxis_title="MWh",
    bargap=0.3
)

fig_mensal.update_traces(
    textposition="outside",
    textfont_size=14
)

st.plotly_chart(fig_mensal, use_container_width=True)
