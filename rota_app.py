import streamlit as st
import networkx as nx

# Criando o grafo com as rotas
G = nx.DiGraph()

# Definindo nós e arestas
G.add_edges_from([
    ("Moega", "Correia A"),
    ("Correia A", "Elevador 1"),
    ("Elevador 1", "Válvula 1"),
    ("Válvula 1", "Silo 1"),
    ("Válvula 1", "Silo 2"),
    ("Elevador 1", "Válvula 2"),
    ("Válvula 2", "Secador")
])

# Função para desenhar o grafo
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

# Interface Streamlit
st.title("Simulador de Rotas - Planta de Grãos")

# Lista de rotas
rotas = ["Rota 1", "Rota 2", "Rota 3", "Rota 4", "Rota 5", "Rota 6", "Rota 7", "Rota 8", "Rota 9", "Rota 10"]

# Colocando a lista de rotas e as caixas de seleção na mesma linha
col1, col2 = st.columns([1, 3])  # Coluna esquerda (para rotas) e direita (para
