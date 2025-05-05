import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

# Criar o grafo com os caminhos possíveis
G = nx.DiGraph()
G.add_edges_from([
    ('A', 'B'), ('B', 'C'), ('C', 'D'),
    ('A', 'E'), ('E', 'F'), ('F', 'G'),
    ('B', 'F'), ('G', 'H'), ('H', 'D'),
    ('C', 'G')
])

# Lista de rotas
rotas = [f"Rota {i+1}" for i in range(10)]

st.title("Simulador de Rotas na Planta de Grãos")

# Inicializar session_state
for i in range(10):
    if f"origem_{i}" not in st.session_state:
        st.session_state[f"origem_{i}"] = list(G.nodes)[0]
    if f"destino_{i}" not in st.session_state:
        st.session_state[f"destino_{i}"] = list(G.nodes)[1]

# Função para desenhar rota
def desenha_rota(caminho):
    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=800, arrows=True)
    edge_path = list(zip(caminho[:-1], caminho[1:]))
    nx.draw_networkx_edges(G, pos, edgelist=edge_path, edge_color='r', width=2)
    st.pyplot(plt)

# Mostrar rotas
st.subheader("Defina as rotas:")

for i, rota in enumerate(rotas):
    with st.form(key=f"form_rota_{i}"):
        col1, col2, col3, col4 = st.columns([1, 3, 3, 4])

        with col1:
            st.write(f"**{rota}**")

        with col2:
            origem = st.selectbox(
                "Origem:", list(G.nodes), key=f"select_origem_{i}",
                index=list(G.nodes).index(st.session_state.get(f"origem_{i}", list(G.nodes)[0]))
            )

        with col3:
            destino = st.selectbox(
                "Destino:", list(G.nodes), key=f"select_destino_{i}",
                index=list(G.nodes).index(st.session_state.get(f"destino_{i}", list(G.nodes)[1]))
            )

        with col4:
            submitted = st.form_submit_button(f"Mostrar {rota}")
            if submitted:
                st.session_state[f"origem_{i}"] = origem
                st.session_state[f"destino_{i}"] = destino

                if nx.has_path(G, origem, destino):
                    caminho = nx.shortest_path(G, origem, destino)
                    st.success(f"{rota}: {origem} → {destino}: {' → '.join(caminho)}")
                    desenha_rota(caminho)
                else:
                    st.error(f"{rota}: Sem caminho entre {origem} e {destino}")
