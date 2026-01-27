import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

arquivo_excel = "ConsumoDiario.xlsx"

# =====================================================
# GRÁFICO 1 — CONSUMO DIÁRIO (MWh)
# Aba: Tabela
# =====================================================
df_diario = pd.read_excel(
    arquivo_excel,
    sheet_name="Tabela",
    skiprows=3,
    usecols="B:D"
)

df_diario.columns = ["Data", "Consumo_kWh", "Consumo_MWh"]

df_diario["Data"] = pd.to_datetime(df_diario["Data"])
df_diario["Dia"] = df_diario["Data"].dt.strftime("%d/%m")
df_diario["Consumo_MWh"] = df_diario["Consumo_MWh"].astype(float)

fig_diario = px.bar(
    df_diario,
    x="Dia",
    y="Consumo_MWh",
    text=df_diario["Consumo_MWh"].round(1),
    title="Consumo Diário de Energia (MWh)",
    color_discrete_sequence=["#90bf3b"]
)

fig_diario.update_layout(
    xaxis_title="Dia",
    yaxis_title="MWh",
    bargap=0.25
)

fig_diario.update_traces(
    textposition="outside",
    textfont_size=12
)

# =====================================================
# GRÁFICO 2 — CONSUMO HORÁRIO (MWh)
# Aba: Tabela2
# =====================================================
df_horario = pd.read_excel(
    arquivo_excel,
    sheet_name="Tabela2",
    skiprows=3,
    usecols="B:D"
)

df_horario.columns = ["Hora", "Consumo_kWh", "Consumo_MWh"]
df_horario["Hora"] = df_horario["Hora"].astype(int)
df_horario["Consumo_MWh"] = df_horario["Consumo_MWh"].astype(float)

fig_horario = px.bar(
    df_horario,
    x="Hora",
    y="Consumo_MWh",
    text=df_horario["Consumo_MWh"].round(1),
    title="Consumo Horário de Energia (MWh) — Referente ao dia anterior",
    color_discrete_sequence=["#263a64"]
)

fig_horario.update_layout(
    xaxis=dict(
        tickmode="linear",
        dtick=1
    ),
    xaxis_title="Hora",
    yaxis_title="MWh"
)

fig_horario.update_traces(
    textposition="outside",
    textfont_size=12
)

# =====================================================
# GRÁFICO 3 — CONSUMO MENSAL (MWh)
# Aba: Tabela3
# =====================================================
df_mensal = pd.read_excel(
    arquivo_excel,
    sheet_name="Tabela3",
    usecols=["Data", "Energia Ativa (mwh)"]
)

df_mensal["Data"] = pd.to_datetime(df_mensal["Data"])
df_mensal["MesAno"] = df_mensal["Data"].dt.strftime("%m/%Y")
df_mensal["Energia Ativa (mwh)"] = df_mensal["Energia Ativa (mwh)"].astype(float)

fig_mensal = px.bar(
    df_mensal,
    x="MesAno",
    y="Energia Ativa (mwh)",
    text=df_mensal["Energia Ativa (mwh)"].round(1),
    title="Consumo Mensal de Energia (MWh)",
    color_discrete_sequence=["#a3afc4"]
)

fig_mensal.update_layout(
    xaxis_title="Mês/Ano",
    yaxis_title="MWh"
)

fig_mensal.update_traces(
    textposition="outside",
    textfont_size=12
)

# =====================================================
# EXIBIÇÃO
# =====================================================
st.title("📊 Dashboard de Consumo de Energia")

st.plotly_chart(fig_diario, use_container_width=True)
st.plotly_chart(fig_horario, use_container_width=True)
st.plotly_chart(fig_mensal, use_container_width=True)
