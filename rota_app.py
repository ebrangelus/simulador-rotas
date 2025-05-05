import streamlit as st
import networkx as nx

# Criar um grafo simples para representar a planta
G = nx.Graph()
G.add_edges_from([
    ("MOEGA 1", "SP1"), ("MOEGA 1", "SP2"), ("MOEGA 1", "SP3"), ("MOEGA 1", "SP4"),
    ("MOEGA 1", "SP5"), ("MOEGA 1", "SP6"), ("MOEGA 1", "SP7"), ("MOEGA 1", "SP8"),
    ("MOEGA 1", "SP9"), ("MOEGA 1", "SP10"),
    ("MOEGA 2", "SP1"), ("MOEGA 2", "SP2"), ("MOEGA 2", "SP3"), ("MOEGA 2", "SP4"),
    ("MOEGA 2", "SP5"), ("MOEGA 2", "SP6"), ("MOEGA 2", "SP7"), ("MOEGA 2", "SP8"),
    ("MOEGA 2", "SP9"), ("MOEGA 2", "SP10")
])

# Definir os destinos fixos
origens = ["MOEGA 1", "MOEGA 2"]
destinos = [f"SP{i}" for i in range(1, 11)]

# Inicializando o estado da sessão
if "status_rotas" not in st.session_state:
    st.session_state["status_rotas"] = {i: "parado" for i in range(1, 11)}
    st.session_state["rotas_ativas"] = {}

# Função para desenhar a rota
def desenha_rota(caminho):
    st.write(f"Desenhando rota: {' → '.join(caminho)}")

# Loop para criar as rotas
for i in range(1, 11):
    with st.expander(f"Rota {i}"):
        col1, col2, col3, col4, col5 = st.columns([1, 3, 3, 1, 1])

        # Exibir a origem e destino para cada rota
        with col1:
            st.write(f"Rota {i}")
        
        with col2:
            origem = st.selectbox(f"Origem para Rota {i}:", origens, key=f"origem_{i}")
        
        with col3:
            destino = st.selectbox(f"Destino para Rota {i}:", destinos, key=f"destino_{i}")
        
        # Mostrar o LED de status
        with col4:
            if st.session_state["status_rotas"][i] == "executando":
                st.markdown("🟢 Rota Iniciada")
            elif st.session_state["status_rotas"][i] == "parado":
                st.markdown("🔴 Rota Parada")
            else:
                st.markdown("🟠 Rota Pausada")

        # Adicionar botão de Play
        with col5:
            if st.form_submit_button(f"▶️ Iniciar Rota {i}"):
                if nx.has_path(G, origem, destino):
                    caminho = nx.shortest_path(G, origem, destino)

                    # Verificar conflito
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
                        st.success(f"{origem} → {destino}: {' → '.join(caminho)}")
                        desenha_rota(caminho)
                else:
                    st.error("⚠️ Caminho inválido")
                    st.session_state["status_rotas"][i] = "parado"

        # Botão de Pausar
        with col5:
            if st.form_submit_button(f"⏸️ Pausar Rota {i}"):
                st.session_state["status_rotas"][i] = "pausado"
                st.warning(f"Rota {i} pausada.")

        # Botão de Parar
        with col5:
            if st.form_submit_button(f"🛑 Parar Rota {i}"):
                st.session_state["status_rotas"][i] = "parado"
                st.info(f"Rota {i} parada.")

