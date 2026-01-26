import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# =========================
# CONFIG STREAMLIT
# =========================
st.set_page_config(
    page_title="SHOPPING GARDEN ITAQUA",
    layout="wide"
)

st.title("📊 Consumo de Energia — SHOPPING GARDEN ITAQUA")

# =========================
# CAMINHO DO EXCEL
# =========================
BASE_DIR = Path(__file__).parent
arquivo_excel = BASE_DIR / "ConsumoDiario.xlsx"

# =========================
# LEITURA DA ABA TABELA
# =========================
df_tabela = pd.read_excel(
    arquivo_excel,
    sheet_name="Tabela",
    usecols="A:E"
)

df_tabela["Data"] = pd.to_datetime(df_tabela["Data"])
df_tabela = df_tabela.dropna(subset=["Energia Ativa (mwh)"])

# =========================
# GRÁFICO 1 — CONSUMO DIÁRIO
# =========================
st.subheader("📅 Consumo Diário — Energia Ativa (MWh)")

fig1, ax1 = plt.subplots(figsize=(10, 5))

bars1 = ax1.bar(
    df_tabela["Data"].dt.strftime("%d/%m"),
    df_tabela["Energia Ativa (mwh)"],
    color="#90bf3b"
)

for bar in bars1:
    height = bar.get_height()
    ax1.text(
        bar.get_x() + bar.get_width() / 2,
        height,
        f"{height:.2f}",
        ha="center",
        va="bottom",
        fontsize=9,
        color="#263a64"
    )

ax1.set_xlabel("Data")
ax1.set_title("Consumo Diário — Energia Ativa (MWh)")
ax1.get_yaxis().set_visible(False)

plt.tight_layout()
st.pyplot(fig1)

# =========================
# DATA DE REFERÊNCIA (C2)
# =========================
df_data_ref = pd.read_excel(
    arquivo_excel,
    sheet_name="Tabela2",
    usecols="C",
    nrows=1
)

data_referencia = pd.to_datetime(df_data_ref.iloc[0, 0])

# =========================
# LEITURA DA ABA TABELA2
# =========================
df_tabela2 = pd.read_excel(
    arquivo_excel,
    sheet_name="Tabela2",
    skiprows=3,
    usecols="B:D",
    names=["Hora", "Energia Ativa (kwh)", "Energia Ativa (mwh)"]
)

df_tabela2 = df_tabela2.dropna()
df_tabela2 = df_tabela2[df_tabela2["Hora"] <= 24]

# =========================
# GARANTIR HORAS 1 A 24
# =========================
horas = pd.DataFrame({"Hora": range(1, 25)})

df_tabela2 = horas.merge(
    df_tabela2,
    on="Hora",
    how="left"
)

df_tabela2["Energia Ativa (mwh)"] = (
    df_tabela2["Energia Ativa (mwh)"]
    .fillna(0)
)

# =========================
# GRÁFICO 2 — CONSUMO HORÁRIO
# =========================
st.subheader(
    f"⏰ Consumo Horário — {data_referencia.strftime('%d/%m/%Y')}"
)

fig2, ax2 = plt.subplots(figsize=(10, 5))

bars2 = ax2.bar(
    df_tabela2["Hora"],
    df_tabela2["Energia Ativa (mwh)"],
    color="#263a64"
)

for bar in bars2:
    height = bar.get_height()
    ax2.text(
        bar.get_x() + bar.get_width() / 2,
        height,
        f"{height:.2f}",
        ha="center",
        va="bottom",
        fontsize=8,
        color="#a3afc4"
    )

ax2.set_xlabel("Hora")
ax2.set_title(
    f"Consumo Horário — {data_referencia.strftime('%d/%m/%Y')}"
)

# 👉 FORÇAR EIXO X DE 1 A 24
ax2.set_xlim(0.5, 24.5)
ax2.set_xticks(range(1, 25))
ax2.set_xticklabels(range(1, 25))

ax2.get_yaxis().set_visible(False)

plt.tight_layout()
st.pyplot(fig2)
