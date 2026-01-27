import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Consumo Shopping Garden Itaqua",
    layout="wide"
)

# =========================
# 📂 CARREGAR EXCEL
# =========================
arquivo_excel = "ConsumoDiario.xlsx"

# ---------- GRÁFICO 1 | Tabela ----------
df_tabela1 = pd.read_excel(
    arquivo_excel,
    sheet_name="Tabela",
    header=3,
    usecols="B:D"
)

df_tabela1.columns = ["Categoria", "Consumo", "Custo"]
df_tabela1["Consumo"] = pd.to_numeric(df_tabela1["Consumo"], errors="coerce")
df_tabela1["Custo"] = pd.to_numeric(df_tabela1["Custo"], errors="coerce")
df_tabela1 = df_tabela1.dropna()

# ---------- GRÁFICO 2 | Tabela2 ----------
df_horario = pd.read_excel(
    arquivo_excel,
    sheet_name="Tabela2",
    header=3,
    usecols="B:C"
)

df_horario.columns = ["Hora", "Consumo"]
df_horario["Hora"] = pd.to_numeric(df_horario["Hora"], errors="coerce")
df_horario["Consumo"] = pd.to_numeric(df_horario["Consumo"], errors="coerce")
df_horario = df_horario.dropna()

# Data na célula C2
data_ref = pd.read_excel(
    arquivo_excel,
    sheet_name="Tabela2",
    header=None,
    usecols="C",
    nrows=2
).iloc[1, 0]

# ---------- GRÁFICO 3 | Tabela3 ----------
df_mensal = pd.read_excel(
    arquivo_excel,
    sheet_name="Tabela3"
)

df_mensal.iloc[:, 0] = pd.to_datetime(df_mensal.iloc[:, 0], errors="coerce")
df_mensal.iloc[:, 1] = pd.to_numeric(df_mensal.iloc[:, 1], errors="coerce")
df_mensal = df_mensal.dropna()

df_mensal.columns = ["Data", "Consumo"]
df_mensal["Mes"] = df_mensal["Data"].dt.strftime("%m/%Y")

# =========================
# 📊 GRÁFICOS
# =========================

st.title("📊 Consumo de Energia – Shopping Garden Itaqua")

# ---------- GRÁFICO 1 ----------
fig1 = px.bar(
    df_tabela1,
    x="Categoria",
    y="Consumo",
    text="Consumo",
    title="Consumo por Categoria"
)

fig1.update_traces(
    texttemplate="%{y:.1f}",
    hovertemplate="%{y:.1f}"
)
fig1.update_yaxes(tickformat=".1f")
fig1.update_layout(height=420)

st.plotly_chart(fig1, use_container_width=True)

# ---------- GRÁFICO 2 ----------
fig2 = px.bar(
    df_horario,
    x="Hora",
    y="Consumo",
    text="Consumo",
    title=f"Consumo Horário – {pd.to_datetime(data_ref).strftime('%d/%m/%Y')}"
)

fig2.update_traces(
    texttemplate="%{y:.1f}",
    hovertemplate="%{y:.1f}"
)
fig2.update_yaxes(tickformat=".1f")
fig2.update_layout(
    height=420,
    xaxis=dict(tickmode="linear")
)

st.plotly_chart(fig2, use_container_width=True)

# ---------- GRÁFICO 3 ----------
fig3 = px.bar(
    df_mensal,
    x="Mes",
    y="Consumo",
    text="Consumo",
    title="Consumo Mensal"
)

fig3.update_traces(
    texttemplate="%{y:.1f}",
    hovertemplate="%{y:.1f}"
)
fig3.update_yaxes(tickformat=".1f")
fig3.update_layout(height=420)

st.plotly_chart(fig3, use_container_width=True)
