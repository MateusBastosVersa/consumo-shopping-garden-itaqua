import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# CONFIG STREAMLIT
# -----------------------------
st.set_page_config(layout="wide")
st.title("📊 Consumo de Energia — Shopping Garden Itaqua")

# -----------------------------
# ARQUIVO
# -----------------------------
arquivo_excel = "ConsumoDiario.xlsx"

# =============================
# GRÁFICO 1 — CONSUMO DIÁRIO (MWh)
# =============================
df_diario = pd.read_excel(
    arquivo_excel,
    sheet_name="Tabela",
    usecols="A:D",
    skiprows=0
)

df_diario.columns = [
    "Data",
    "Energia_kwh",
    "Energia_kvarh",
    "Energia_mwh"
]

df_diario = df_diario.dropna(subset=["Data", "Energia_mwh"])
df_diario["Data"] = pd.to_datetime(df_diario["Data"])

fig1, ax1 = plt.subplots(figsize=(14, 5))

ax1.bar(
    df_diario["Data"],
    df_diario["Energia_mwh"],
    color="#90bf3b"
)

ax1.set_title("Consumo Diário de Energia (MWh)", fontsize=14)
ax1.set_xlabel("Data")
ax1.set_ylabel("MWh")

ax1.tick_params(axis="x", rotation=45)

# rótulos nas colunas
for i, v in enumerate(df_diario["Energia_mwh"]):
    ax1.text(
        df_diario["Data"].iloc[i],
        v,
        f"{v:.1f}",
        ha="center",
        va="bottom",
        fontsize=9
    )

st.pyplot(fig1)

# =============================
# GRÁFICO 2 — CONSUMO HORÁRIO (MWh)
# =============================
df_horario = pd.read_excel(
    arquivo_excel,
    sheet_name="Tabela2",
    usecols="B:D",
    skiprows=3
)

df_horario.columns = ["Hora", "Energia_kwh", "Energia_mwh"]
df_horario = df_horario.dropna(subset=["Hora", "Energia_mwh"])

fig2, ax2 = plt.subplots(figsize=(14, 4))

ax2.bar(
    df_horario["Hora"],
    df_horario["Energia_mwh"],
    color="#263a64"
)

ax2.set_title("Consumo Horário de Energia (MWh) — Dia Anterior", fontsize=14)
ax2.set_xlabel("Hora")
ax2.set_ylabel("MWh")
ax2.set_xticks(range(1, 25))

for i, v in enumerate(df_horario["Energia_mwh"]):
    ax2.text(
        df_horario["Hora"].iloc[i],
        v,
        f"{v:.1f}",
        ha="center",
        va="bottom",
        fontsize=9
    )

st.pyplot(fig2)

# =============================
# GRÁFICO 3 — CONSUMO MENSAL (MWh)
# =============================
df_mensal = pd.read_excel(
    arquivo_excel,
    sheet_name="Tabela3",
    usecols="A:E"
)

df_mensal = df_mensal[["Data", "Energia Ativa (mwh)"]]
df_mensal = df_mensal.dropna()

df_mensal["Data"] = pd.to_datetime(df_mensal["Data"])
df_mensal["MesAno"] = df_mensal["Data"].dt.strftime("%m/%Y")

fig3, ax3 = plt.subplots(figsize=(10, 4))

ax3.bar(
    df_mensal["MesAno"],
    df_mensal["Energia Ativa (mwh)"],
    color="#a3afc4"
)

ax3.set_title("Consumo Mensal de Energia (MWh)", fontsize=14)
ax3.set_xlabel("Mês/Ano")
ax3.set_ylabel("MWh")

for i, v in enumerate(df_mensal["Energia Ativa (mwh)"]):
    ax3.text(
        i,
        v,
        f"{v:.1f}",
        ha="center",
        va="bottom",
        fontsize=9
    )

st.pyplot(fig3)
