import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import calendar

# ===============================
# CONFIGURAÇÃO DA PÁGINA
# ===============================
st.set_page_config(
    page_title="Consumo Energético | Shopping Garden Itaqua",
    layout="wide"
)

st.title("📊 Consumo Energético — Shopping Garden Itaqua")

# ===============================
# CORES PADRÃO
# ===============================
COR_PRINCIPAL = "#90bf3b"
COR_SECUNDARIA = "#263a64"
COR_TERCIARIA = "#a3afc4"

# ===============================
# LEITURA DO EXCEL
# ===============================
arquivo_excel = "ConsumoDiario.xlsx"

# Aba Tabela
df_tabela = pd.read_excel(
    arquivo_excel,
    sheet_name="Tabela"
)

df_tabela["Data"] = pd.to_datetime(df_tabela["Data"])

# Aba Tabela2
df_tabela2 = pd.read_excel(
    arquivo_excel,
    sheet_name="Tabela2",
    header=3,
    usecols="B:D"
)

df_tabela2.columns = ["Hora", "Energia Ativa (kwh)", "Energia Ativa (mwh)"]
df_tabela2["Hora"] = df_tabela2["Hora"].astype(int)

# Aba Tabela3 (NOVO)
df_tabela3 = pd.read_excel(
    arquivo_excel,
    sheet_name="Tabela3"
)

df_tabela3["Data"] = pd.to_datetime(df_tabela3["Data"])

# Cria coluna Mês/Ano em texto (ex: janeiro/2025)
df_tabela3["MesAno"] = df_tabela3["Data"].apply(
    lambda x: f"{calendar.month_name[x.month].capitalize()}/{x.year}"
)

# ===============================
# GRÁFICO 1 — CONSUMO DIÁRIO
# ===============================
st.subheader("🔹 Consumo Diário — Energia Ativa (MWh)")

fig1, ax1 = plt.subplots()

bars = ax1.bar(
    df_tabela["Data"].dt.strftime("%d/%m/%Y"),
    df_tabela["Energia Ativa (mwh)"],
    color=COR_PRINCIPAL
)

ax1.set_ylabel("")
ax1.set_yticks([])
ax1.set_xlabel("Data")

for bar in bars:
    altura = bar.get_height()
    ax1.text(
        bar.get_x() + bar.get_width() / 2,
        altura,
        f"{altura:.2f}",
        ha="center",
        va="bottom"
    )

st.pyplot(fig1)

# ===============================
# GRÁFICO 2 — CONSUMO HORÁRIO
# ===============================
st.subheader("🔹 Consumo Horário — Energia Ativa (MWh)")

horas_completas = pd.DataFrame({"Hora": range(1, 25)})
df_horario = horas_completas.merge(
    df_tabela2,
    on="Hora",
    how="left"
).fillna(0)

fig2, ax2 = plt.subplots()

bars2 = ax2.bar(
    df_horario["Hora"],
    df_horario["Energia Ativa (mwh)"],
    color=COR_SECUNDARIA
)

ax2.set_xticks(range(1, 25))
ax2.set_xlabel("Hora")
ax2.set_ylabel("")
ax2.set_yticks([])

for bar in bars2:
    altura = bar.get_height()
    ax2.text(
        bar.get_x() + bar.get_width() / 2,
        altura,
        f"{altura:.2f}",
        ha="center",
        va="bottom",
        fontsize=8
    )

st.pyplot(fig2)

# ===============================
# GRÁFICO 3 — CONSUMO MENSAL (NOVO)
# ===============================
st.subheader("🔹 Consumo Mensal — Energia Ativa (MWh)")

fig3, ax3 = plt.subplots()

bars3 = ax3.bar(
    df_tabela3["MesAno"],
    df_tabela3["Energia Ativa (mwh)"],
    color=COR_TERCIARIA
)

ax3.set_xlabel("Mês / Ano")
ax3.set_ylabel("")
ax3.set_yticks([])

for bar in bars3:
    altura = bar.get_height()
    ax3.text(
        bar.get_x() + bar.get_width() / 2,
        altura,
        f"{altura:.2f}",
        ha="center",
        va="bottom"
    )

st.pyplot(fig3)

# ===============================
# RODAPÉ
# ===============================
st.caption("Fonte: ConsumoDiario.xlsx | Atualização manual via Git")
