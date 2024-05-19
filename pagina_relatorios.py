import streamlit as st
import psycopg2
import pandas as pd

# Função para conectar ao banco de dados PostgreSQL


def conectar_bd():
    conn = psycopg2.connect(
        host="localhost",
        database="bsbdasha",
        user="postgres",
        password="root"
    )
    return conn

# Função para obter dados dos clientes


def obter_dados_clientes():
    conn = conectar_bd()
    query = "SELECT * FROM bsbdasha"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Função para deletar um registro


def deletar_registro(cliente, equipamento, mes):
    conn = conectar_bd()
    cur = conn.cursor()
    cur.execute("DELETE FROM bsbdasha WHERE cliente = %s AND equipamento = %s AND mes = %s",
                (cliente, equipamento, mes))
    conn.commit()
    conn.close()

# Função para renderizar a página


def render_pagina():
    st.title("Relatório Geral")

    # Adiciona CSS personalizado para garantir largura total e responsividade
    st.markdown(
        """
        <style>
        .full-width {
            width: 100%;
            max-width: 100%;
            display: block;
        }
        .full-width-table {
            width: 100%;
            display: block;
            overflow-x: auto;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Carrega os dados dos clientes
    df_clientes = obter_dados_clientes()

    # Cria um formulário para selecionar e deletar registros
    with st.form("delete_form"):
        # Adiciona uma coluna de seleção
        selecoes = [False] * len(df_clientes)

        # Exibe os dados dos clientes em formato de tabela com checkboxes
        st.markdown('<div class="full-width-table">', unsafe_allow_html=True)
        cols = st.columns([2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1])
        headers = ["Cliente", "Equipamento", "Mês", "Qtd Ordens", "Total Horas",
                   "Total Horas/Mês", "Disponibilidade", "Indisponibilidade", "MTTR", "MTBF", "Selecionar"]
        for col, header in zip(cols, headers):
            col.write(f"**{header}**")

        for i, row in df_clientes.iterrows():
            cols = st.columns([2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1])
            cols[0].write(row['cliente'])
            cols[1].write(row['equipamento'])
            cols[2].write(row['mes'])
            cols[3].write(row['qtd_ordens_servico'])
            cols[4].write(row['total_horas'])
            cols[5].write(row['total_horas_mes'])
            cols[6].write(row['disponibilidade'])
            cols[7].write(row['indisponibilidade'])
            cols[8].write(row['mttr'])
            cols[9].write(row['mtbf'])
            selecoes[i] = cols[10].checkbox("", key=f"select_{i}")

        st.markdown('</div>', unsafe_allow_html=True)

        # Botão para excluir equipamentos selecionados
        submit_button = st.form_submit_button("Excluir Equipamento(s)")

        if submit_button:
            for i, row in df_clientes.iterrows():
                if selecoes[i]:
                    deletar_registro(
                        row['cliente'], row['equipamento'], row['mes'])
            st.experimental_rerun()  # Recarrega a página após a exclusão


# Chama a função para renderizar a página
render_pagina()
