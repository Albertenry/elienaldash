# main.py
import pandas as pd
import streamlit as st
from PIL import Image
from streamlit_option_menu import option_menu
import Paginas.pagina_clientes as pagina_clientes
import Paginas.pagina_dashboards as pagina_dashboards
import Paginas.pagina_inicio as pagina_inicio
import Paginas.pagina_monitoramento as pagina_monitoramento
import Paginas.pagina_relatorios as pagina_relatorios
import Paginas.pagina_suporte as pagina_suporte
import Paginas.ordem_de_servico as ordem_de_servico

# Função para carregar o CSS


def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


# Carregar o CSS personalizado
load_css("style.css")

# -- Criar o sidebar
with st.sidebar:
    logo_teste = Image.open('./Mídia/bsb_logo.png')
    st.image(logo_teste, width=300)
    st.subheader('CONTROLE DE SERVIÇOS')
    selected = option_menu(
        menu_title="Menu principal",
        options=["Início", "Clientes", "Dashboards",
                 "Relatórios", "Monitoramento", "Suporte", "Ordem_de_serviço"],
        icons=["house", "people", "bar-chart",
               "bandaid", "laptop", "telephone", "clipboard"],
        menu_icon="cast",
        default_index=0
    )

# Dicionário de mapeamento de páginas
pagina_mapeamento = {
    "Início": pagina_inicio.render_home,
    "Clientes": pagina_clientes.render_lista,
    "Dashboards": pagina_dashboards.render_dashboard,
    "Relatórios": pagina_relatorios.render_tabela,
    "Monitoramento": pagina_monitoramento.render_dados,
    "Suporte": pagina_suporte.render_contato,
    "Ordem_de_serviço": ordem_de_servico.render_formulario
}

# Função para renderizar a página selecionada


def render_pagina(pagina_selecionada):
    if pagina_selecionada in pagina_mapeamento:
        pagina_mapeamento[pagina_selecionada]()
    else:
        st.error("Página não encontrada!")


# Inicialização da página
render_pagina(selected)
