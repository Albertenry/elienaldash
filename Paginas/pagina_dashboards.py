import streamlit as st
import psycopg2
import pandas as pd
import plotly.express as px
import numpy as np


def conectar_bd():
    conn = psycopg2.connect(
        host="localhost",
        database="bsbdasha",
        user="postgres",
        password="root"
    )
    return conn


def obter_dados_clientes():
    conn = conectar_bd()
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT cliente FROM bsbdasha")
    clientes = [row[0] for row in cur.fetchall()]
    conn.close()
    return clientes


def obter_dados_equipamentos():
    conn = conectar_bd()
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT equipamento FROM bsbdasha")
    equipamentos = [row[0] for row in cur.fetchall()]
    conn.close()
    return equipamentos


def obter_dados_meses():
    conn = conectar_bd()
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT mes FROM bsbdasha ORDER BY mes")
    meses = [row[0] for row in cur.fetchall()]
    conn.close()
    return meses


def obter_dados_filtrados(cliente, equipamento, meses):
    conn = conectar_bd()
    cur = conn.cursor()
    query = """
        SELECT mes, disponibilidade, indisponibilidade, mttr, mtbf
        FROM bsbdasha
        WHERE cliente = %s AND equipamento = %s AND mes IN %s
    """
    cur.execute(query, (cliente, equipamento, tuple(meses)))
    dados = cur.fetchall()
    conn.close()
    return dados


def calcular_metricas(dados):
    df = pd.DataFrame(
        dados, columns=['mes', 'disponibilidade', 'indisponibilidade', 'mttr', 'mtbf'])
    disponibilidade_media = df['disponibilidade'].mean()
    indisponibilidade_media = df['indisponibilidade'].mean()
    mttr_media = df['mttr'].mean()
    mtbf_media = df['mtbf'].mean()
    return disponibilidade_media, indisponibilidade_media, mttr_media, mtbf_media, df


def render_dashboard():
    st.title("Dashboard")

    clientes = obter_dados_clientes()
    equipamentos = obter_dados_equipamentos()
    meses = obter_dados_meses()

    cliente_selecionado = st.selectbox("Selecione o Cliente", clientes)
    equipamento_selecionado = st.selectbox(
        "Selecione o Equipamento", equipamentos)
    meses_selecionados = st.multiselect("Selecione o(s) Mês(es)", meses)

    if cliente_selecionado and equipamento_selecionado and meses_selecionados:
        dados = obter_dados_filtrados(
            cliente_selecionado, equipamento_selecionado, meses_selecionados)
        if dados:
            disponibilidade, indisponibilidade, mttr, mtbf, df = calcular_metricas(
                dados)

            # Cabeçalho com as métricas
            dst1, dst2, dst3, dst4 = st.columns([1, 1, 1, 1])

            with dst1:
                st.write('**DISPONIBILIDADE:**')
                st.info(f"{disponibilidade:.2f}%")

            with dst2:
                st.write('**INDISPONIBILIDADE:**')
                st.info(f"{indisponibilidade:.2f}%")

            with dst3:
                st.write('**MTTR:**')
                st.info(f"{mttr:.2f} horas")

            with dst4:
                st.write('**MTBF:**')
                st.info(f"{mtbf:.2f} horas")

            st.markdown('---')
            st.markdown('')
            st.markdown('---')

            # Adicionar o gráfico de evolução da disponibilidade
            df['mes'] = pd.Categorical(
                df['mes'], categories=meses, ordered=True)
            df = df.sort_values('mes')
            fig = px.line(df, x='mes', y='disponibilidade',
                          title='Evolução da Disponibilidade por Mês')

            # Exibir o gráfico em duas colunas
            col1, col2 = st.columns([1, 1])
            with col1:
                st.plotly_chart(fig, use_container_width=True)

        else:
            st.warning("Nenhum dado encontrado para os filtros selecionados.")
    else:
        st.info("Por favor, selecione o cliente, equipamento e os meses.")


# Chama a função para renderizar o dashboard
render_dashboard()
