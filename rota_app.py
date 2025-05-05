import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

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

st.title("Simulador de Rotas - Planta de Grãos")

origem = st.selectbox("Selecione a origem:", list(G.nodes))
destino = st.selectbox("Selecione o destino:", list(G.nodes))

if st.button("Simular Rota"):
    if nx.has_path(G, origem, destino):
        caminho = nx.shortest_path(G, origem, destino)
        st.success(f"Rota encontrada: {' → '.join(caminho)}")
    else:
        st.error("Não há caminho possível entre os pontos selecionados.")
else:
    caminho = []

fig, ax = plt.subplots(figsize=(8, 6))
pos = nx.spring_layout(G, seed=42)
edge_colors = []
for u, v in G.edges():
    if caminho and (u, v) in zip(caminho, caminho[1:]):
        edge_colors.append("red")
    else:
        edge_colors.append("gray")

nx.draw(G, pos, with_labels=True, node_color="lightblue", edge_color=edge_colors, width=2.5, node_size=1500, arrows=True, ax=ax)
st.pyplot(fig)
