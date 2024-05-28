import streamlit as st
import psycopg2
import pandas as pd
import plotly.express as px


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
        SELECT mes, qtd_ordens_servico, disponibilidade, indisponibilidade, mttr, mtbf
        FROM bsbdasha
        WHERE cliente = %s AND equipamento = %s AND mes IN %s
    """
    cur.execute(query, (cliente, equipamento, tuple(meses)))
    dados = cur.fetchall()
    conn.close()
    return dados


def calcular_metricas(dados):
    df = pd.DataFrame(
        dados, columns=['mes', 'qtd_ordens_servico', 'disponibilidade', 'indisponibilidade', 'mttr', 'mtbf'])
    disponibilidade_media = df['disponibilidade'].mean()
    indisponibilidade_media = df['indisponibilidade'].mean()
    mttr_media = df['mttr'].mean()
    mtbf_media = df['mtbf'].mean()
    return df, disponibilidade_media, indisponibilidade_media, mttr_media, mtbf_media


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
            df, disponibilidade, indisponibilidade, mttr, mtbf = calcular_metricas(
                dados)

            st.markdown('---')

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

            # Gráficos
            st.markdown('---')

            col1, col2, col3 = st.columns([1, 1, 1])

            with col1:
                fig = px.bar(df, x='mes', y='disponibilidade',
                             title='Disponibilidade (%)', range_y=[95, 100])
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                fig = px.area(df, x='mes', y='indisponibilidade',
                              title='Indisponibilidade (%)', range_y=[0, 3])
                st.plotly_chart(fig, use_container_width=True)

            with col1:
                fig = px.area(df, x='mes', y='mttr',
                              title='MTTR', range_y=[0, 3])
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                fig = px.line(df, x='mes', y='mtbf',
                              title='MTBF', range_y=[360, 370])
                st.plotly_chart(fig, use_container_width=True)

            # Gráfico de rosca para comparar a quantidade de ordens de serviço entre os meses escolhidos
            with col3:
                fig = px.pie(df, values='qtd_ordens_servico', names='mes', hole=0.4,
                             title='Qtd de Ordens de Serviços')
                st.plotly_chart(fig, use_container_width=True)

        else:
            st.warning("Nenhum dado encontrado para os filtros selecionados.")
    else:
        st.info("Por favor, selecione o cliente, equipamento e os meses.")


# Chama a função para renderizar o dashboard
render_dashboard()
