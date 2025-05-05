import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

st.set_page_config(page_title="Simulador de Rotas", layout="wide")

# Criar grafo de exemplo
G = nx.DiGraph()
G.add_edges_from([
    ("A", "B"), ("B", "C"), ("C", "D"),
    ("A", "D"), ("D", "E"), ("E", "F"),
    ("F", "G"), ("B", "E"), ("C", "F")
])

# Lista fixa de rotas
rotas = [f"Rota {i+1}" for i in range(10)]

# Função para desenhar a rota
def desenha_rota(caminho):
    pos = nx.spring_layout(G)
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_color="lightblue", node_size=1500, arrows=True)
    edge_path = list(zip(caminho, caminho[1:]))
    nx.draw_networkx_edges(G, pos, edgelist=edge_path, edge_color="red", width=3)
    st.pyplot(plt)

st.title("Simulador de Rotas Industriais")

# Layout da página: lista de rotas à esquerda
for i, rota in enumerate(rotas):
    with st.form(key=f"form_rota_{i}"):
        col1, col2, col3, col4 = st.columns([1, 3, 3, 2])
        
        with col1:
            st.write(f"**{rota}**")
        
        with col2:
            origem = st.selectbox(
                f"Origem {rota}", list(G.nodes),
                index=list(G.nodes).index(
                    st.session_state.get(f"origem_{i}", list(G.nodes)[0])
                ),
                key=f"select_origem_{i}"
            )
        
        with col3:
            destino = st.selectbox(
                f"Destino {rota}", list(G.nodes),
                index=list(G.nodes).index(
                    st.session_state.get(f"destino_{i}", list(G.nodes)[1])
                ),
                key=f"select_destino_{i}"
            )

        with col4:
            submit = st.form_submit_button("Mostrar")

        if submit:
            st.session_state[f"origem_{i}"] = origem
            st.session_state[f"destino_{i}"] = destino

            if nx.has_path(G, origem, destino):
                caminho = nx.shortest_path(G, origem, destino)
                st.success(f"{rota}: {origem} → {destino}: {' → '.join(caminho)}")
                desenha_rota(caminho)
            else:
                st.error(f"{rota}: Sem caminho entre {origem} e {destino}")
