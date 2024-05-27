# ordem_de_servico.py
import streamlit as st
from datetime import datetime
from Services.cliente_services import (
    conectar_bd,
    inserir_dados,
    calcular_disponibilidade,
    calcular_indisponibilidade,
    calcular_mttr,
    calcular_mtbf
)


def obter_clientes():
    conn = conectar_bd()
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT cliente FROM bsbdasha")
    clientes = [row[0] for row in cur.fetchall()]
    conn.close()
    return clientes


def obter_equipamentos():
    conn = conectar_bd()
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT equipamento FROM bsbdasha")
    equipamentos = [row[0] for row in cur.fetchall()]
    conn.close()
    return equipamentos


def render_formulario():
    st.title("Cadastro")

    clientes = obter_clientes()
    cliente = st.selectbox("Cliente", options=clientes +
                           ["Adicionar novo cliente"])

    if cliente == "Adicionar novo cliente":
        cliente = st.text_input("Novo Cliente")

    equipamentos = obter_equipamentos()
    equipamento = st.selectbox(
        "Equipamento", options=equipamentos + ["Adicionar novo equipamento"])

    if equipamento == "Adicionar novo equipamento":
        equipamento = st.text_input("Novo Equipamento")

    meses = [
        "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
    ]
    mes = st.selectbox("Mês", meses, index=datetime.now().month - 1)
    qtd_ordens_servico = st.number_input(
        "Quantidade de Ordem de Serviço", min_value=1)
    total_horas_mes = st.number_input("Total horas/Mês", min_value=1)
    total_horas = 730

    if st.button("Enviar Dados"):
        mttr = calcular_mttr(qtd_ordens_servico, total_horas_mes)
        mtbf = calcular_mtbf(total_horas, total_horas_mes, qtd_ordens_servico)
        disponibilidade = calcular_disponibilidade(mtbf, mttr)
        indisponibilidade = calcular_indisponibilidade(
            total_horas, total_horas_mes)

        inserir_dados(cliente, equipamento, mes, qtd_ordens_servico, total_horas,
                      total_horas_mes, disponibilidade, indisponibilidade, mttr, mtbf)

        st.success("Dados inseridos com sucesso!")


render_formulario()
