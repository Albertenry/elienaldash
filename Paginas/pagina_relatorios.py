import streamlit as st
import psycopg2
import pandas as pd


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
    query = "SELECT * FROM bsbdasha"
    df = pd.read_sql(query, conn)
    conn.close()
    return df


def deletar_registro(cliente, equipamento, mes):
    conn = conectar_bd()
    cur = conn.cursor()
    cur.execute("DELETE FROM bsbdasha WHERE cliente = %s AND equipamento = %s AND mes = %s",
                (cliente, equipamento, mes))
    conn.commit()
    conn.close()


def render_tabela():
    st.title("Relatórios")
    df_clientes = obter_dados_clientes()

    # Adicionar filtros
    clientes_unicos = df_clientes['cliente'].unique()
    equipamentos_unicos = df_clientes['equipamento'].unique()
    meses_unicos = df_clientes['mes'].unique()

    cliente_selecionado = st.selectbox(
        "Selecionar Cliente", options=clientes_unicos)
    equipamento_selecionado = st.selectbox(
        "Selecionar Equipamento", options=equipamentos_unicos)
    meses_selecionados = st.multiselect(
        "Selecionar Mês(es)", options=meses_unicos, default=meses_unicos)

    # Aplicar filtros aos dados
    df_filtrado = df_clientes[
        (df_clientes['cliente'] == cliente_selecionado) &
        (df_clientes['equipamento'] == equipamento_selecionado) &
        (df_clientes['mes'].isin(meses_selecionados))
    ]

    with st.form("delete_form"):
        st.write(
            "Selecione os registros a serem deletados e clique em 'Excluir Equipamento(s)'")

        # Adiciona uma coluna de seleção
        df_filtrado["Selecionar"] = False

        # Exibe os dados dos clientes em formato de tabela
        edited_df = st.data_editor(df_filtrado, num_rows="dynamic")

        submit_button = st.form_submit_button("Excluir Equipamento(s)")

        if submit_button:
            for i, row in edited_df.iterrows():
                if row["Selecionar"]:
                    deletar_registro(
                        row['cliente'], row['equipamento'], row['mes'])
            st.experimental_rerun()


# Chama a função para renderizar a tabela
render_tabela()
