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

rotas = [f"Rota {i+1}" for i in range(10)]

# Inicializações
if "rotas_ativas" not in st.session_state:
    st.session_state["rotas_ativas"] = {}

if "status_rotas" not in st.session_state:
    st.session_state["status_rotas"] = {i: "parado" for i in range(len(rotas))}

def desenha_rota(caminho):
    pos = nx.spring_layout(G)
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_color="lightblue", node_size=1500, arrows=True)
    edge_path = list(zip(caminho, caminho[1:]))
    nx.draw_networkx_edges(G, pos, edgelist=edge_path, edge_color="red", width=3)
    st.pyplot(plt)

st.title("Simulador de Rotas Industriais")

for i, rota in enumerate(rotas):
    with st.form(key=f"form_rota_{i}"):
        col1, col2, col3, col4, col5, col6, col7, col8 = st.columns([1, 2.5, 2.5, 2, 1, 1, 1, 1])
        
        with col1:
            st.write(f"**{rota}**")

        with col2:
            origem = st.selectbox(
                "Origem", list(G.nodes),
                index=list(G.nodes).index(st.session_state.get(f"origem_{i}", list(G.nodes)[0])),
                key=f"select_origem_{i}"
            )

        with col3:
            destino = st.selectbox(
                "Destino", list(G.nodes),
                index=list(G.nodes).index(st.session_state.get(f"destino_{i}", list(G.nodes)[1])),
                key=f"select_destino_{i}"
            )

        with col4:
            comentario = st.text_input("Comentário", key=f"comentario_{i}")

        with col5:
            if st.form_submit_button("▶️"):
                st.session_state["status_rotas"][i] = "executando"
        
        with col6:
            if st.form_submit_button("⏸️"):
                st.session_state["status_rotas"][i] = "pausado"
        
        with col7:
            if st.form_submit_button("⏹️"):
                st.session_state["status_rotas"][i] = "parado"
                st.session_state["rotas_ativas"].pop(i, None)
        
        with col8:
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
                    desenha_rota(caminho)
            else:
                st.error(f"{rota}: Caminho inválido")
