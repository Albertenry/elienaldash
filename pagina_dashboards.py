# pagina_dashboards.py

import streamlit as st
import psycopg2


def conectar_bd():
    conn = psycopg2.connect(
        host="localhost",
        database="bsbdasha",
        user="postgres",
        password="root"
    )
    return conn


def renderizar_dashboard():
    st.title("Dashboard")
    st.write("CLIENTE:")

    disponibilidade = 95
    indisponibilidade = 5
    mttr = 2.5
    mtbf = 60

# Cabeçalho com as métricas
    dst1, dst2, dst3, dst4 = st.columns([1, 1, 1, 1])

    with dst1:
        st.write('**DISPONIBILIDADE:**')
        st.info(disponibilidade)

    with dst2:
        st.write('**INDISPONIBILIDADE:**')
        st.info(indisponibilidade)

    with dst3:
        st.write('**MTTR:**')
        st.info(mttr)

    with dst4:
        st.write('**MTBF:**')
        st.info(mtbf)

        # Adicionando duas linhas horizontais
    st.markdown("---")
    st.markdown("---")

    def obter_disponibilidade():
        conn = conectar_bd()
        cur = conn.cursor()
        cur.execute("SELECT disponibilidade FROM bsbdasha")

        dados_disponibilidade = cur.fetchall()

        conn.close()

        return dados_disponibilidade
    st.write("Dados de Disponibilidade:")
    st.write(obter_disponibilidade())


# Chama a função para renderizar o dashboard
renderizar_dashboard()
