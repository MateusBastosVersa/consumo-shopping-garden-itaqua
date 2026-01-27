import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Consumo de Energia", layout="wide")

arquivo_excel = "ConsumoDiario.xlsx"

# =========================
# GRÁFICO 1 — DIÁRIO
# =========================
df_diario = pd.read_excel(
    arquivo_excel,
    sheet_name="Tabela"
)

df_diario = df_diario.iloc[:, :2]
df_diario.columns = ["Data", "Consumo"]

df_diario["Data"] = pd.to_datetime(df_diario["Data"])
df_diario["Consumo"] = pd.to_numeric(df_diario["Consumo"], errors="coerce")

fig1, ax1 = plt.subplots(figsize=(8, 4))
ax1.bar(df_diario["Data"], df_diario["Consumo"])
ax1.set_title("Consumo Diário (kWh)")
ax1.set_ylabel("kWh")

ax1.yaxis.set_major_formatter(lambda x, _: f"{x:.1f}")

st.pyplot(fig1)

# =========================
# GRÁFICO 2 — HORÁRIO
# =========================
df_horario = pd.read_excel(
    arquivo_excel,
    sheet_name="Tabela2",
    header=3,
    usecols="B:D"
)

df_horario.columns = ["Hora", "kWh", "MWh"]

df_horario = df_horario.dropna()
df_horario["Hora"] = df_horario["Hora"].astype(str)
df_horario["kWh"] = pd.to_numeric(df_horario["kWh"], errors="coerce")

fig2, ax2 = plt.subplots(figsize=(10, 4))
ax2.bar(df_horario["Hora"], df_horario["kWh"])
ax2.set_title("Consumo Horário (kWh)")
ax2.set_ylabel("kWh")

ax2.yaxis.set_major_formatter(lambda x, _: f"{x:.1f}")
ax2.tick_params(axis="x", rotation=90)

st.pyplot(fig2)

# =========================
# GRÁFICO 3 — MENSAL
# =========================
df_mensal = pd.read_excel(
    arquivo_excel,
    sheet_name="Tabela3"
)

df_mensal = df_mensal[["Data", "Energia Ativa (mwh)"]]
df_mensal.columns = ["Data", "Consumo"]

df_mensal["Data"] = pd.to_datetime(df_mensal["Data"])
df_mensal["Consumo"] = pd.to_numeric(df_mensal["Consumo"], errors="coerce")

df_mensal["MesAno"] = df_mensal["Data"].dt.strftime("%m/%Y")

fig3, ax3 = plt.subplots(figsize=(8, 4))
ax3.bar(df_mensal["MesAno"], df_mensal["Consumo"])
ax3.set_title("Consumo Mensal (MWh)")
ax3.set_ylabel("MWh")

ax3.yaxis.set_major_formatter(lambda x, _: f"{x:.1f}")

st.pyplot(fig3)
