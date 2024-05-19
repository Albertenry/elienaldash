import streamlit as st
from datetime import datetime
import psycopg2
from psycopg2 import sql

# Função para calcular a disponibilidade

def calcular_disponibilidade(mtbf, mttr):
    return (mtbf / (mtbf + mttr)) * 100

# Função para calcular a indisponibilidade

def calcular_indisponibilidade(total_horas, total_horas_mes):
    return (total_horas_mes / total_horas) * 100

# Função para calcular o MTTR (Mean Time To Repair)

def calcular_mttr(qtd_ordens_servico, total_horas_mes):
    return total_horas_mes / qtd_ordens_servico

# Função para calcular o MTBF (Mean Time Between Failures)

def calcular_mtbf(total_horas, total_horas_mes, qtd_ordens_servico):
    return (total_horas - total_horas_mes) / qtd_ordens_servico

# Função para conectar ao banco de dados PostgreSQL

def conectar_bd():
    conn = psycopg2.connect(
        host="localhost",
        database="bsbdasha",
        user="postgres",
        password="root"
    )
    return conn


def tabela_existe(nome_tabela, cursor):
    cursor.execute(
        """
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_name = %s
        )
        """,
        (nome_tabela,)
    )
    return cursor.fetchone()[0]


def criar_tabela(nome_tabela, cursor):
    cursor.execute(
        sql.SQL("""
        CREATE TABLE IF NOT EXISTS bsbdasha (
            cliente TEXT,
            equipamento TEXT,
            mes TEXT,
            qtd_ordens_servico INTEGER,
            total_horas INTEGER,
            total_horas_mes INTEGER,
            disponibilidade FLOAT,
            indisponibilidade FLOAT,
            mttr FLOAT,
            mtbf FLOAT
        )
        """).format(sql.Identifier(nome_tabela))
    )

def inserir_dados(cliente, equipamento, mes, qtd_ordens_servico, total_horas, total_horas_mes, disponibilidade, indisponibilidade, mttr, mtbf):
    conn = conectar_bd()
    cur = conn.cursor()

    if not tabela_existe("bsbdasha", cur):
        criar_tabela("bsbdasha", cur)

    cur.execute(
        "INSERT INTO bsbdasha (cliente, equipamento, mes, qtd_ordens_servico, total_horas, total_horas_mes, disponibilidade, indisponibilidade, mttr, mtbf) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
        (cliente, equipamento, mes, qtd_ordens_servico, total_horas, total_horas_mes, disponibilidade, indisponibilidade, mttr, mtbf))
    conn.commit()
    conn.close()

def render_pagina():
    st.title("Cadastrar Ordem de Serviço")
    cliente = st.text_input("Cliente")
    equipamento = st.text_input("Equipamento")
    meses = [
        "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
    ]
    mes = st.selectbox("Mês", meses, index=datetime.now().month - 1)
    qtd_ordens_servico = st.number_input(
        "Quantidade de Ordem de Serviço", min_value=1)
    total_horas_mes = st.number_input("Total horas/Mês", min_value=1)
    total_horas = 730

    if st.button("Calcular e Inserir Dados"):
        mttr = calcular_mttr(qtd_ordens_servico, total_horas_mes)
        mtbf = calcular_mtbf(total_horas, total_horas_mes, qtd_ordens_servico)
        disponibilidade = calcular_disponibilidade(mtbf, mttr)
        indisponibilidade = calcular_indisponibilidade(
            total_horas, total_horas_mes)


        inserir_dados(cliente, equipamento, mes, qtd_ordens_servico, total_horas,
                      total_horas_mes, disponibilidade, indisponibilidade, mttr, mtbf)

        st.success("Dados inseridos com sucesso!")

    #if st.button("Novo Cadastro"):
    #   st.experimental_rerun()


render_pagina()
