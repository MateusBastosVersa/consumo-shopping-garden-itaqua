import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Consumo de Energia", layout="wide")

# =========================
# CONFIGURAÇÕES
# =========================
arquivo_excel = "ConsumoDiario.xlsx"
paleta = ["#90bf3b", "#263a64", "#a3afc4"]

# =========================
# GRÁFICO 1 — CONSUMO DIÁRIO (MWh)
# Aba: Tabela
# =========================
df_diario = pd.read_excel(
    arquivo_excel,
    sheet_name="Tabela",
    header=0
)

# Col A: Data | Col D: Energia Ativa (MWh)
df_diario = df_diario.iloc[:, [0, 3]]
df_diario.columns = ["Data", "Consumo_MWh"]
df_diario["Data"] = pd.to_datetime(df_diario["Data"])

fig_diario = px.bar(
    df_diario,
    x="Data",
    y="Consumo_MWh",
    title="Consumo Diário de Energia (MWh)",
    color_discrete_sequence=[paleta[0]],
    text=df_diario["Consumo_MWh"].round(1)
)

fig_diario.update_layout(
    xaxis=dict(
        title="Data",
        tickmode="linear",
        dtick="D",
        tickformat="%d/%m",
        tickangle=-45
    ),
    yaxis_title="MWh",
    bargap=0.2
)

fig_diario.update_traces(
    textposition="outside",
    textfont_size=14
)

st.plotly_chart(fig_diario, use_container_width=True)

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
    title="Consumo Horário (MWh) – Referente ao dia anterior",
    color_discrete_sequence=[paleta[1]],
    text=df_horario["Consumo_MWh"].round(1)
)

fig_horario.update_layout(
    xaxis=dict(
        title="Hora",
        tickmode="linear",
        tick0=1,
        dtick=1
    ),
    yaxis_title="MWh",
    bargap=0.15
)

fig_horario.update_traces(
    textposition="outside",
    textfont_size=14
)

st.plotly_chart(fig_horario, use_container_width=True)

# =========================
# GRÁFICO 3 — CONSUMO MENSAL (MWh)
# Aba: Tabela3
# =========================
df_mensal = pd.read_excel(
    arquivo_excel,
    sheet_name="Tabela3",
    header=0
)

# Col A: Data | Col E: Energia Ativa (MWh)
df_mensal = df_mensal.iloc[:, [0, 4]]
df_mensal.columns = ["Data", "Consumo_MWh"]
df_mensal["Data"] = pd.to_datetime(df_mensal["Data"])
df_mensal["MesAno"] = df_mensal["Data"].dt.strftime("%m/%Y")

df_mensal_agg = df_mensal.groupby("MesAno", as_index=False)["Consumo_MWh"].sum()

fig_mensal = px.bar(
    df_mensal_agg,
    x="MesAno",
    y="Consumo_MWh",
    title="Consumo Mensal (MWh)",
    color_discrete_sequence=[paleta[2]],
    text=df_mensal_agg["Consumo_MWh"].round(1)
)

fig_mensal.update_layout(
    xaxis_title="Mês/Ano",
    yaxis_title="MWh",
    bargap=0.3
)

fig_mensal.update_traces(
    textposition="outside",
    textfont_size=14
)

st.plotly_chart(fig_mensal, use_container_width=True)
