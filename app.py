import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# =============================
# CONFIGURAÇÃO STREAMLIT
# =============================
st.set_page_config(
    page_title="Consumo de Energia | Shopping Garden Itaqua",
    layout="centered"
)

arquivo_excel = "ConsumoDiario.xlsx"

# Paleta
COR_VERDE = "#90bf3b"
COR_AZUL = "#263a64"
COR_CINZA = "#a3afc4"

def adicionar_rotulos(ax, formato="{:.1f}"):
    for container in ax.containers:
        ax.bar_label(container, fmt=formato, fontsize=9, padding=3)

st.title("📊 Consumo de Energia — Shopping Garden Itaqua")

# =====================================================
# GRÁFICO 1 — CONSUMO DIÁRIO (MWh)
# Aba: Tabela
# =====================================================
df_diario = pd.read_excel(
    arquivo_excel,
    sheet_name="Tabela",
    header=None
)

# A:E → dados começam na linha 2
df_diario = df_diario.iloc[1:, [0, 3]]
df_diario.columns = ["Data", "Consumo"]

df_diario["Data"] = pd.to_datetime(df_diario["Data"])
df_diario["Consumo"] = pd.to_numeric(df_diario["Consumo"], errors="coerce")

# 🔥 TRANSFORMAR DATA EM CATEGORIA
df_diario["Data_str"] = df_diario["Data"].dt.strftime("%d/%m")

fig1, ax1 = plt.subplots(figsize=(14, 5))
ax1.bar(df_diario["Data_str"], df_diario["Consumo"], color=COR_VERDE)

ax1.set_title("Consumo Diário (MWh)")
ax1.set_ylabel("MWh")
ax1.grid(axis="y", alpha=0.3)
ax1.tick_params(axis="x", rotation=45)

adicionar_rotulos(ax1)

plt.tight_layout()
st.pyplot(fig1)

# =====================================================
# GRÁFICO 2 — CONSUMO HORÁRIO (MWh)
# Aba: Tabela2
# =====================================================
df_horario = pd.read_excel(
    arquivo_excel,
    sheet_name="Tabela2",
    header=None
)

# B4:D28 → Hora / kWh / MWh
df_horario = df_horario.iloc[4:28, [1, 3]]
df_horario.columns = ["Hora", "Consumo"]

# Força horas 1 a 24
df_horario["Hora"] = range(1, 25)
df_horario["Consumo"] = pd.to_numeric(df_horario["Consumo"], errors="coerce")

fig2, ax2 = plt.subplots(figsize=(14, 5))
ax2.bar(df_horario["Hora"], df_horario["Consumo"], color=COR_AZUL)

ax2.set_title("Consumo Horário (MWh)")
ax2.set_xlabel("Hora")
ax2.set_ylabel("MWh")
ax2.set_xticks(range(1, 25))
ax2.grid(axis="y", alpha=0.3)

adicionar_rotulos(ax2)

plt.tight_layout()
st.pyplot(fig2)

# =====================================================
# GRÁFICO 3 — CONSUMO MENSAL (MWh)
# Aba: Tabela3
# =====================================================
df_mensal = pd.read_excel(
    arquivo_excel,
    sheet_name="Tabela3"
)

df_mensal["Data"] = pd.to_datetime(df_mensal["Data"])
df_mensal["MesAno"] = df_mensal["Data"].dt.strftime("%m/%Y")
df_mensal["Energia Ativa (mwh)"] = pd.to_numeric(
    df_mensal["Energia Ativa (mwh)"], errors="coerce"
)

fig3, ax3 = plt.subplots(figsize=(10, 5))
ax3.bar(
    df_mensal["MesAno"],
    df_mensal["Energia Ativa (mwh)"],
    color=COR_CINZA
)

ax3.set_title("Consumo Mensal (MWh)")
ax3.set_ylabel("MWh")
ax3.grid(axis="y", alpha=0.3)
ax3.tick_params(axis="x", rotation=45)

adicionar_rotulos(ax3)

plt.tight_layout()
st.pyplot(fig3)
