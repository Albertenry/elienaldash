# cliente_services.py
import psycopg2
from psycopg2 import sql

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

def calcular_disponibilidade(mtbf, mttr):
    return (mtbf / (mtbf + mttr)) * 100

def calcular_indisponibilidade(total_horas, total_horas_mes):
    return (total_horas_mes / total_horas) * 100

def calcular_mttr(qtd_ordens_servico, total_horas_mes):
    return total_horas_mes / qtd_ordens_servico

def calcular_mtbf(total_horas, total_horas_mes, qtd_ordens_servico):
    return (total_horas - total_horas_mes) / qtd_ordens_servico
