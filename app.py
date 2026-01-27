import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ===============================
# CONFIGURAÇÃO DA PÁGINA
# ===============================
st.set_page_config(
    page_title="Consumo de Energia | Shopping Garden Itaqua",
    layout="centered"
)

st.title("📊 Consumo de Energia — Shopping Garden Itaqua")

arquivo_excel = "ConsumoDiario.xlsx"

# ===============================
# LEITURA DAS ABAS
# ===============================

# --- TABELA 1: CONSUMO DIÁRIO ---
df_diario = pd.read_excel(
    arquivo_excel,
    sheet_name="Tabela"
)

# --- TABELA 2: CONSUMO HORÁRIO ---
df_horario = pd.read_excel(
    arquivo_excel,
    sheet_name="Tabela2",
    skiprows=3  # começa na linha do cabeçalho real
)

df_horario.columns = [
    "Hora",
    "Energia_kwh",
    "Energia_mwh"
]

# --- TABELA 3: CONSUMO MENSAL ---
df_mensal = pd.read_excel(
    arquivo_excel,
    sheet_name="Tabela3"
)

# ===============================
# GRÁFICO 1 — CONSUMO DIÁRIO
# ===============================
st.subheader("🔹 Consumo Diário")

fig1, ax1 = plt.subplots(figsize=(6, 4))

bars = ax1.bar(
    df_diario.iloc[:, 0],
    df_diario.iloc[:, 3],  # Energia Ativa (mwh)
    color="#90bf3b"
)

for bar in bars:
    ax1.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height(),
        f"{bar.get_height():,.0f}",
        ha="center",
        va="bottom",
        fontsize=8
    )

ax1.set_ylabel("")
ax1.set_yticks([])
ax1.set_xlabel("")
plt.xticks(rotation=45)

st.pyplot(fig1)

# ===============================
# GRÁFICO 2 — CONSUMO HORÁRIO
# ===============================
st.subheader("🔹 Consumo Horário")

fig2, ax2 = plt.subplots(figsize=(7, 4))

bars = ax2.bar(
    df_horario["Hora"],
    df_horario["Energia_mwh"],
    color="#263a64"
)

for bar in bars:
    ax2.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height(),
        f"{bar.get_height():,.0f}",
        ha="center",
        va="bottom",
        fontsize=8
    )

ax2.set_xlim(1, 24)
ax2.set_xticks(range(1, 25))
ax2.set_ylabel("")
ax2.set_yticks([])
ax2.set_xlabel("Hora")

st.pyplot(fig2)

# ===============================
# GRÁFICO 3 — CONSUMO MENSAL
# ===============================
st.subheader("🔹 Consumo Mensal")

df_mensal["Data"] = pd.to_datetime(df_mensal["Data"])
df_mensal["MesAno"] = df_mensal["Data"].dt.strftime("%B/%Y")

fig3, ax3 = plt.subplots(figsize=(6, 4))

bars = ax3.bar(
    df_mensal["MesAno"],
    df_mensal["Energia Ativa (kwh)"],
    color="#a3afc4"
)

for bar in bars:
    ax3.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height(),
        f"{bar.get_height():,.0f}",
        ha="center",
        va="bottom",
        fontsize=8
    )

ax3.set_ylabel("")
ax3.set_yticks([])
ax3.set_xlabel("")
plt.xticks(rotation=30)

st.pyplot(fig3)
