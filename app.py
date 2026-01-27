import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# =============================
# CONFIG STREAMLIT
# =============================
st.set_page_config(layout="wide")
st.title("⚡ Dashboard de Consumo de Energia — Shopping Garden Itaqua")

arquivo_excel = "ConsumoDiario.xlsx"

# =============================
# LEITURA DOS DADOS
# =============================
df_diario = pd.read_excel(
    arquivo_excel,
    sheet_name="Tabela",
    usecols="A:D"
)

df_diario.columns = ["Data", "Energia_kwh", "Energia_kvarh", "Energia_mwh"]
df_diario = df_diario.dropna(subset=["Data", "Energia_mwh"])
df_diario["Data"] = pd.to_datetime(df_diario["Data"])

df_horario = pd.read_excel(
    arquivo_excel,
    sheet_name="Tabela2",
    usecols="B:D",
    skiprows=3
)

df_horario.columns = ["Hora", "Energia_kwh", "Energia_mwh"]
df_horario = df_horario.dropna()

df_mensal = pd.read_excel(
    arquivo_excel,
    sheet_name="Tabela3",
    usecols="A:E"
)

df_mensal = df_mensal[["Data", "Energia Ativa (mwh)"]]
df_mensal = df_mensal.dropna()
df_mensal["Data"] = pd.to_datetime(df_mensal["Data"])
df_mensal["MesAno"] = df_mensal["Data"].dt.strftime("%m/%Y")

# =============================
# KPIs
# =============================
st.markdown("### 📌 Indicadores Gerais")

kpi1, kpi2, kpi3 = st.columns(3)

kpi1.metric(
    "📅 Último Consumo Diário (MWh)",
    f"{df_diario.iloc[-1]['Energia_mwh']:.2f}"
)

kpi2.metric(
    "⚡ Consumo Total do Mês (MWh)",
    f"{df_mensal['Energia Ativa (mwh)'].sum():.2f}"
)

kpi3.metric(
    "📈 Média Diária (MWh)",
    f"{df_diario['Energia_mwh'].mean():.2f}"
)

st.divider()

# =============================
# GRÁFICO 1 — DIÁRIO
# =============================
st.markdown("### 📊 Consumo Diário")

fig1, ax1 = plt.subplots(figsize=(14, 4))
ax1.bar(df_diario["Data"], df_diario["Energia_mwh"])
ax1.set_xlabel("Data")
ax1.set_ylabel("MWh")
ax1.set_title("Consumo Diário de Energia (MWh)")
ax1.tick_params(axis="x", rotation=45)

st.pyplot(fig1)

st.divider()

# =============================
# GRÁFICOS 2 E 3 LADO A LADO
# =============================
col1, col2 = st.columns(2)

with col1:
    st.markdown("### ⏱️ Consumo Horário — Dia Anterior")
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    ax2.bar(df_horario["Hora"], df_horario["Energia_mwh"])
    ax2.set_xlabel("Hora")
    ax2.set_ylabel("MWh")
    ax2.set_xticks(range(1, 25))
    st.pyplot(fig2)

with col2:
    st.markdown("### 🗓️ Consumo Mensal")
    fig3, ax3 = plt.subplots(figsize=(6, 4))
    ax3.bar(df_mensal["MesAno"], df_mensal["Energia Ativa (mwh)"])
    ax3.set_xlabel("Mês/Ano")
    ax3.set_ylabel("MWh")
    ax3.tick_params(axis="x", rotation=45)
    st.pyplot(fig3)
