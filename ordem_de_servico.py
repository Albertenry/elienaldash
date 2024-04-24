import streamlit as st
from datetime import datetime
import psycopg2
from psycopg2 import sql

# Função para calcular a disponibilidade
def calcular_disponibilidade(total_horas, total_horas_mes):
    return (total_horas_mes - total_horas) / total_horas_mes

# Função para calcular a indisponibilidade


def calcular_indisponibilidade(total_horas, total_horas_mes):
    return 1 - calcular_disponibilidade(total_horas, total_horas_mes)

# Função para calcular o MTTR (Mean Time To Repair)


def calcular_mttr(quantidade_ordens_servico, total_horas_mes):
    return total_horas_mes / quantidade_ordens_servico

# Função para calcular o MTBF (Mean Time Between Failures)


def calcular_mtbf(disponibilidade, indisponibilidade):
    return disponibilidade / indisponibilidade

# Função para conectar ao banco de dados PostgreSQL


def conectar_bd():
    conn = psycopg2.connect(
        host="localhost",
        database="bsbdasha",
        user="postgres",
        password="root"
    )
    return conn

# Função para verificar se a tabela existe no banco de dados


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

# Função para criar a tabela no banco de dados caso ela não exista


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

# Função para inserir dados na tabela do banco de dados


def inserir_dados(cliente,
                  equipamento,
                  mes,
                  qtd_ordens_servico,
                  total_horas,
                  total_horas_mes,
                  disponibilidade,
                  indisponibilidade,
                  mttr,
                  mtbf
                  ):
    conn = conectar_bd()
    cur = conn.cursor()

    if not tabela_existe("bsbdasha", cur):
        criar_tabela("bsbdasha", cur)

    cur.execute(
        "INSERT INTO bsbdasha (cliente, equipamento, mes, qtd_ordens_servico, total_horas, total_horas_mes, disponibilidade, indisponibilidade, mttr, mtbf) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
        (cliente, equipamento, mes, qtd_ordens_servico, total_horas, total_horas_mes, disponibilidade, indisponibilidade, mttr, mtbf))
    conn.commit()
    conn.close()

# Função para renderizar a página de cadastro de ordem de serviço


def render_pagina():
    st.title("Cadastrar Ordem de Serviço")

    # Campos do formulário
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
    total_horas = 730  # Fixa o total de horas por mês

    # Botão para calcular e inserir os dados
    if st.button("Calcular e Inserir Dados"):
        # Calculando métricas
        disponibilidade = calcular_disponibilidade(
            total_horas, total_horas_mes)
        indisponibilidade = calcular_indisponibilidade(
            total_horas, total_horas_mes)
        mttr = calcular_mttr(qtd_ordens_servico, total_horas_mes)
        mtbf = calcular_mtbf(disponibilidade, indisponibilidade)

        # Inserindo dados no banco de dados
        inserir_dados(cliente, equipamento, mes, qtd_ordens_servico, total_horas,
                      total_horas_mes, disponibilidade, indisponibilidade, mttr, mtbf)

        # Exibindo mensagem de sucesso
        st.success("Dados inseridos com sucesso!")

        if st.button("Novo Cadastro"):
            # Define os campos do formulário como vazios ou padrão
            cliente = ""
            equipamento = ""
            mes = meses[datetime.now().month - 1]
            qtd_ordens_servico = 1
            total_horas_mes = 1
            total_horas = 730
