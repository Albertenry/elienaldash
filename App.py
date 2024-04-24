import pandas as pd
import streamlit as st
from PIL import Image
from streamlit_option_menu import option_menu
import pagina_clientes
import pagina_dashboards
import pagina_inicio
import pagina_monitoramento
import pagina_relatorios
import pagina_suporte
import ordem_de_servico

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
    pagina_mapeamento = {
        "Início": pagina_inicio.render_pagina,
        "Clientes": pagina_clientes.render_pagina,
        "Dashboards": pagina_dashboards.renderizar_dashboard,
        "Relatórios": pagina_relatorios.render_pagina,
        "Monitoramento": pagina_monitoramento.render_pagina,
        "Suporte": pagina_suporte.render_pagina,
        "Ordem_de_serviço": ordem_de_servico.render_pagina
    }

    # Função para renderizar a página selecionada
    def render_pagina(pagina_selecionada):
        if pagina_selecionada in pagina_mapeamento:
            pagina_mapeamento[pagina_selecionada]()
        else:
            st.error("Página não encontrada!")

# Inicialização da página
render_pagina(selected)
