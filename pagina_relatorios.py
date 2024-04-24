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


def render_pagina():
    st.title("Relatório Geral")
    st.write("Conteúdo da página de início aqui.")

    # Carrega os dados dos clientes
    df_clientes = obter_dados_clientes()

    # Exibe os dados dos clientes
    st.write(df_clientes)
