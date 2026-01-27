import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# =============================
# CONFIGURAÇÃO DA PÁGINA
# =============================
st.set_page_config(
    page_title="Consumo de Energia | Shopping Garden Itaqua",
    layout="centered"  # 👈 EVITA GRÁFICO GIGANTE
)

st.title("📊 Consumo de Energia — Shopping Garden Itaqua")

# =============================
# LEITURA DO EXCEL
# =============================
arquivo_excel = "ConsumoDiario.xlsx"

# -------- TABELA PRINCIPAL (Consumo Diário) --------
df_diario = pd.read_excel(
    arquivo_excel,
    sheet_name="ConsumoDiario"
)

# -------- TABELA HORÁRIA --------
df_horario = pd.read_excel(
    arquivo_excel,
    sheet_name="Tabela2"
)

# -------- TABELA MENSAL --------
df_tabela3 = pd.read_excel(
    arquivo_excel,
    sheet_name="Tabela3"
)

# =============================
# AJUSTES DE DADOS
# =============================

# --- Consumo horário: garantir horas 1 a 24 ---
horas_completas = pd.DataFrame({"Hora": range(1, 25)})
df_horario = horas_completas.merge(df_horario, on="Hora", how="left")
df_horario["Consumo"] = df_horario["Consumo"].fillna(0)

# --- Consumo mensal: criar coluna Mês/Ano ---
df_tabela3["Data"] = pd.to_datetime(df_tabela3["Data"])
df_tabela3["Mes_Ano"] = df_tabela3["Data"].dt.strftime("%B/%Y")

# =============================
# CORES PADRÃO
# =============================
CORES = {
    "verde": "#90bf3b",
    "azul": "#263a64",
    "cinza": "#a3afc4"
}

# =============================
# GRÁFICO 1 — CONSUMO DIÁRIO
# =============================
st.subheader("📅 Consumo Diário")

fig1, ax1 = plt.subplots(figsize=(7, 3))  # 👈 ZOOM CONTROLADO

ax1.bar(
    df_diario["Data"],
    df_diario["Consumo"],
    color=CORES["verde"]
)

ax1.set_title("Consumo Diário de Energia")
ax1.set_xlabel("")
ax1.set_ylabel("kWh")

plt.xticks(rotation=45)

st.pyplot(fig1, clear_figure=True)

# =============================
# GRÁFICO 2 — CONSUMO HORÁRIO
# =============================
st.subheader("⏰ Consumo Horário")

fig2, ax2 = plt.subplots(figsize=(7, 3))  # 👈 ZOOM CONTROLADO

ax2.plot(
    df_horario["Hora"],
    df_horario["Consumo"],
    marker="o",
    color=CORES["azul"]
)

ax2.set_title("Consumo Horário Médio")
ax2.set_xlabel("Hora")
ax2.set_ylabel("kWh")
ax2.set_xticks(range(1, 25))

st.pyplot(fig2, clear_figure=True)

# =============================
# GRÁFICO 3 — CONSUMO MENSAL
# =============================
st.subheader("📆 Consumo Mensal")

fig3, ax3 = plt.subplots(figsize=(7, 3))  # 👈 ZOOM CONTROLADO

ax3.bar(
    df_tabela3["Mes_Ano"],
    df_tabela3["Energia Ativa (kwh)"],
    color=CORES["cinza"]
)

ax3.set_title("Consumo Mensal de Energia")
ax3.set_xlabel("Mês/Ano")
ax3.set_ylabel("kWh")

plt.xticks(rotation=45)

st.pyplot(fig3, clear_figure=True)

# =============================
# RODAPÉ
# =============================
st.markdown("---")
st.caption("Dashboard desenvolvido para acompanhamento de consumo energético")
