import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

st.set_page_config(page_title="Simulador de Rotas", layout="wide")

# Criação do grafo direcionado
G = nx.DiGraph()

# Definindo os nós (origens, intermediários, destinos)
origens = ["MOEGA 1", "MOEGA 2"]
intermediarios = ["V-1", "V-7", "V-8", "CT-1", "CT-2"]
limpeza = ["Não", "MLP-1", "MLP-2", "MLP-3", "MLP-4"]
secador = ["Não", "SEC-1", "SEC-2"]
destinos = ["Elevador-1", "Elevador-2", "Elevador-3", "Elevador-4"]

# Adicionando os nós no grafo
G.add_nodes_from(origens + intermediarios + destinos)

# Adicionando as arestas

# MOEGA1 manda para V-1
G.add_edge("MOEGA 1", "V-1")

# MOEGA2 manda para V-1
G.add_edge("MOEGA 2", "V-4")

# V-1 manda para CT-1 ou CT-2
G.add_edge("V-1", "CT-1")
G.add_edge("V-1", "CT-2")

# V-41 manda para CT-1 ou CT-2
G.add_edge("V-4", "CT-1")
G.add_edge("V-4", "CT-2")

# CT-1 manda para V-7
G.add_edge("CT-1", "V-7")

# CT-2 manda para V-8
G.add_edge("CT-2", "V-8")

# V-7 manda para Elevador-1 ou Elevador-3
G.add_edge("V-7", "Elevador-1")
G.add_edge("V-7", "Elevador-3")

# V-8 manda para Elevador-2 ou Elevador-4
G.add_edge("V-8", "Elevador-2")
G.add_edge("V-8", "Elevador-4")

# O grafo agora está montado com as rotas possíveis

# Definir as rotas
rotas = ['Rota 1', 'Rota 2', 'Rota 3', 'Rota 4',  'Rota 5',  'Rota 6',  'Rota 7',  'Rota 8',  'Rota 9',  'Rota 10']

# Inicializações
if "rotas_ativas" not in st.session_state:
    st.session_state["rotas_ativas"] = {}

if "status_rotas" not in st.session_state:
    st.session_state["status_rotas"] = {i: "parado" for i in range(len(rotas))}

# def desenha_rota(caminho):
#   pos = nx.spring_layout(G)
#    plt.figure(figsize=(8, 6))
#    nx.draw(G, pos, with_labels=True, node_color="lightblue", node_size=1500, arrows=True)
#    edge_path = list(zip(caminho, caminho[1:]))
#    nx.draw_networkx_edges(G, pos, edgelist=edge_path, edge_color="red", width=3)
#    st.pyplot(plt)

st.title("Simulador de Rotas Industriais")

for i, rota in enumerate(rotas):
    with st.form(key=f"form_rota_{i}"):
        col1, col2, col3, col4, col5, col6, col7, col8 , col9, col10 = st.columns([1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
        
    with col1:
            st.write(f"**{rota}**")

    with col2:
        origem = st.selectbox(
            "Origem", origens,  # Usando a lista 'origens', que tem apenas "MOEGA 1" e "MOEGA 2"
                index=origens.index(st.session_state.get(f"origem_{i}", origens[0])),  # Corrigido para usar 'origens'
                    key=f"select_origem_{i}"
    )
        
    with col3:
        prelimpeza = st.selectbox(
            "Pré Limpeza", limpeza,  # Usando a lista 'limpeza', que tem apenas "MOEGA 1" e "MOEGA 2"
                index=limpeza.index(st.session_state.get(f"prelimpeza_{i}", limpeza[0])),  # Corrigido para usar 'origens'
                    key=f"select_prelimpeza_{i}"
    )    
        
    with col4:
        destino = st.selectbox(
            "Destino", destinos,  # Usando a lista 'destinos', que tem "SP1" até "SP10"
                index=destinos.index(st.session_state.get(f"destino_{i}", destinos[0])),  # Corrigido para usar 'destinos'
                    key=f"select_destino_{i}"
    )
    with col5:
        origemsecador = st.selectbox(
            "Secador", secador,  # Usando a lista 'secador', que tem "SP1" até "SP10"
                index=secador.index(st.session_state.get(f"origemsecador_{i}", secador[0])),  # Corrigido para usar 'destinos'
                    key=f"select_origemsecador_{i}"
    )

        with col6:
            comentario = st.text_input("Comentário", key=f"comentario_{i}")

        with col7:
            if st.form_submit_button("▶️"):
                if nx.has_path(G, origem, destino):
                    caminho = nx.shortest_path(G, origem, destino)

                    conflito = False
                    for j, outro_caminho in st.session_state["rotas_ativas"].items():
                        if i == j:
                            continue
                        if set(zip(caminho, caminho[1:])) & set(zip(outro_caminho, outro_caminho[1:])):
                            conflito = True
                            break

                    if conflito:
                        st.error(f"⚠️ Conflito com outra rota ativa!")
                        st.session_state["status_rotas"][i] = "parado"
                    else:
                        st.session_state[f"origem_{i}"] = origem
                        st.session_state[f"destino_{i}"] = destino
                        st.session_state["status_rotas"][i] = "executando"
                        st.session_state["rotas_ativas"][i] = caminho
                        #st.success(f"{rota}: {' → '.join(caminho)}")
                        #desenha_rota(caminho)
                else:
                    st.error("⚠️ Caminho inválido")
                    st.session_state["status_rotas"][i] = "parado"

        
        with col8:
            if st.form_submit_button("⏸️"):
                st.session_state["status_rotas"][i] = "pausado"
        
        with col9:
            if st.form_submit_button("⏹️"):
                st.session_state["status_rotas"][i] = "parado"
                st.session_state["rotas_ativas"].pop(i, None)
        
        with col10:
            status = st.session_state["status_rotas"][i]
            if status == "executando":
                st.markdown("🟢")
            elif status == "pausado":
                st.markdown("🟡")
            else:
                st.markdown("🔴")

        # Após botões, desenhar ou mostrar mensagem
        if status == "executando":
            st.session_state[f"origem_{i}"] = origem
            st.session_state[f"destino_{i}"] = destino

            if nx.has_path(G, origem, destino):
                caminho = nx.shortest_path(G, origem, destino)

                conflito = False
                for j, outro_caminho in st.session_state["rotas_ativas"].items():
                    if i == j:
                        continue
                    if set(zip(caminho, caminho[1:])) & set(zip(outro_caminho, outro_caminho[1:])):
                        conflito = True
                        st.error(f"⚠️ Conflito com {rotas[j]}!")
                        break

                if not conflito:
                    st.session_state["rotas_ativas"][i] = caminho
                    st.success(f"{rota}: {' → '.join(caminho)}")
                    # desenha_rota(caminho)
            else:
                st.error(f"{rota}: Caminho inválido")
