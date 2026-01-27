import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# =============================
# CONFIGURAÇÕES GERAIS
# =============================
st.set_page_config(
    page_title="Consumo de Energia | Shopping Garden Itaqua",
    layout="centered"
)

arquivo_excel = "ConsumoDiario.xlsx"

# Paleta oficial
COR_VERDE = "#90bf3b"
COR_AZUL = "#263a64"
COR_CINZA = "#a3afc4"

# Função padrão para rótulos
def adicionar_rotulos(ax, formato="{:.1f}"):
    for container in ax.containers:
        ax.bar_label(container, fmt=formato, fontsize=9, padding=3)

# =============================
# TÍTULO
# =============================
st.title("📊 Consumo de Energia — Shopping Garden Itaqua")

# =============================
# GRÁFICO 1 — CONSUMO DIÁRIO (MWh)
# =============================
df_diario = pd.read_excel(
    arquivo_excel,
    sheet_name="Tabela"
)

df_diario = df_diario.iloc[4:35, 1:3]
df_diario.columns = ["Data", "Consumo"]
df_diario["Data"] = pd.to_datetime(df_diario["Data"])
df_diario["Consumo"] = pd.to_numeric(df_diario["Consumo"], errors="coerce")

fig1, ax1 = plt.subplots(figsize=(8, 4))
ax1.bar(df_diario["Data"], df_diario["Consumo"], color=COR_VERDE)
ax1.set_title("Consumo Diário (MWh)")
ax1.set_ylabel("MWh")
ax1.grid(axis="y", alpha=0.3)

adicionar_rotulos(ax1)

st.pyplot(fig1)

# =============================
# GRÁFICO 2 — CONSUMO HORÁRIO (kWh)
# =============================
df_horario = pd.read_excel(
    arquivo_excel,
    sheet_name="Tabela2",
    header=None
)

df_horario = df_horario.iloc[4:28, 1:3]
df_horario.columns = ["Hora", "Consumo"]
df_horario["Hora"] = range(1, len(df_horario) + 1)
df_horario["Consumo"] = pd.to_numeric(df_horario["Consumo"], errors="coerce")

fig2, ax2 = plt.subplots(figsize=(8, 4))
ax2.bar(df_horario["Hora"], df_horario["Consumo"], color=COR_AZUL)
ax2.set_title("Consumo Horário (kWh)")
ax2.set_xlabel("Hora")
ax2.set_ylabel("kWh")
ax2.set_xlim(1, 24)
ax2.grid(axis="y", alpha=0.3)

adicionar_rotulos(ax2)

st.pyplot(fig2)

# =============================
# GRÁFICO 3 — CONSUMO MENSAL (MWh)
# =============================
df_mensal = pd.read_excel(
    arquivo_excel,
    sheet_name="Tabela3"
)

df_mensal["Data"] = pd.to_datetime(df_mensal["Data"])
df_mensal["MesAno"] = df_mensal["Data"].dt.strftime("%m/%Y")
df_mensal["Energia Ativa (mwh)"] = pd.to_numeric(
    df_mensal["Energia Ativa (mwh)"], errors="coerce"
)

fig3, ax3 = plt.subplots(figsize=(8, 4))
ax3.bar(df_mensal["MesAno"], df_mensal["Energia Ativa (mwh)"], color=COR_CINZA)
ax3.set_title("Consumo Mensal (MWh)")
ax3.set_ylabel("MWh")
ax3.grid(axis="y", alpha=0.3)

adicionar_rotulos(ax3)

st.pyplot(fig3)
