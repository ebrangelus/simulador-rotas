import streamlit as st
import networkx as nx

# Criando o grafo
G = nx.DiGraph()
G.add_edges_from([
    ("Moega", "Correia A"),
    ("Correia A", "Elevador 1"),
    ("Elevador 1", "Válvula 1"),
    ("Válvula 1", "Silo 1"),
    ("Válvula 1", "Silo 2"),
    ("Elevador 1", "Válvula 2"),
    ("Válvula 2", "Secador")
])

# Função para desenhar a rota
def desenha_rota(rota):
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(8, 6))
    pos = nx.spring_layout(G, seed=42)
    edge_colors = []
    for u, v in G.edges():
        if (u, v) in zip(rota, rota[1:]):
            edge_colors.append("red")
        else:
            edge_colors.append("gray")
    nx.draw(G, pos, with_labels=True, node_color="lightblue", edge_color=edge_colors, width=2.5, node_size=1500, arrows=True, ax=ax)
    st.pyplot(fig)

# Lista de rotas
rotas = [f"Rota {i+1}" for i in range(10)]

# Inicializar session_state
for i in range(10):
    if f"origem_{i}" not in st.session_state:
        st.session_state[f"origem_{i}"] = list(G.nodes)[0]
    if f"destino_{i}" not in st.session_state:
        st.session_state[f"destino_{i}"] = list(G.nodes)[1]

st.title("Simulador de Rotas - Planta de Grãos")

# Exibindo cada rota em linha
for i, rota in enumerate(rotas):
    col1, col2, col3, col4 = st.columns([1, 3, 3, 4])

    with col1:
        st.write(f"**{rota}**")

    with col2:
        st.session_state[f"origem_{i}"] = st.selectbox(
            f"Origem para {rota}:", list(G.nodes), key=f"select_origem_{i}", index=list(G.nodes).index(st.session_state[f"origem_{i}"])
        )

    with col3:
        st.session_state[f"destino_{i}"] = st.selectbox(
            f"Destino para {rota}:", list(G.nodes), key=f"select_destino_{i}", index=list(G.nodes).index(st.session_state[f"destino_{i}"])
        )

    with col4:
        if st.button(f"Mostrar rota para {rota}", key=f"mostrar_rota_{i}"):
            origem = st.session_state[f"origem_{i}"]
            destino = st.session_state[f"destino_{i}"]
            if nx.has_path(G, origem, destino):
                caminho = nx.shortest_path(G, origem, destino)
                st.success(f"Rota de {origem} até {destino}: {' → '.join(caminho)}")
                desenha_rota(caminho)
            else:
                st.error(f"Não há caminho possível entre {origem} e {destino} para {rota}.")
