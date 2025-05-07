import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

st.set_page_config(page_title="Simulador de Rotas", layout="wide")

# Criação do grafo direcionado
G = nx.DiGraph()

# Definindo os nós (origens, intermediários, destinos)
origens = ["MOEGA 1", "MOEGA 2"]
intermediarios = ["V-1", "V-4", "V-7", "V-8", "CT-1", "CT-2"]
limpeza = ["Não", "MLP-1", "MLP-2", "MLP-3", "MLP-4"]
secador = ["Não", "SEC-1", "SEC-2"]
destinos = ["Elevador-1", "Elevador-2", "Elevador-3", "Elevador-4"]

# Adicionando os nós no grafo
vb = [f"V-{i}" for i in range(1, 81)]
el = [f"E-{i}" for i in range(1, 21)]
ct = [f"CT-{i}" for i in range(1, 51)]
rt = [f"RT-{i}" for i in range(1, 10)]
tc = [f"TC-{i}" for i in range(1, 10)]
vr = [f"VR-{i}" for i in range(1, 10)]
val = [f"VAL-{i}" for i in range(1, 10)]

origens = ["MOEGA 1", "MOEGA 2", "SP-01", "SP-02", "SP-03", "SP-04", "SP-05", "SP-06", "SP-07", "SP-08", "SP-09", "SP-10", "SA-01", "SA-02", "SA-03", "SA-04", "SA-05", "SA-06", "SA-07", "SA-08"]
intermediarios = vb + el + ct + rt + tc + vr + val
limpeza = ["Sem Limpeza", "MLP-1", "MLP-2", "MLP-3", "MLP-4"]
secador = ["Sem Secador", "SEC-1", "SEC-2"]
destinos = ["SP-01", "SP-02", "SP-03", "SP-04", "SP-05", "SP-06", "SP-07", "SP-08", "SP-09", "SP-10", "SA-01", "SA-02", "SA-03", "SA-04", "SA-05", "SA-06", "SA-07", "SA-08", "SIL-01", "SIL-02", "SIL-03", "SIL-04", "SIL-05"]

G.add_nodes_from(origens + intermediarios + limpeza + secador + destinos)

G.add_edge("MOEGA 1", "V-1")
G.add_edge("MOEGA 2", "V-4")
G.add_edge("V-1", "CT-1")
G.add_edge("V-1", "CT-2")
G.add_edge("V-4", "CT-1")
G.add_edge("V-4", "CT-2")
G.add_edge("CT-1", "V-7")
G.add_edge("CT-2", "V-8")
G.add_edge("V-7", "E-1")
G.add_edge("V-7", "E-3")
G.add_edge("V-8", "E-2")
G.add_edge("V-8", "E-4")
G.add_edge("E-1", "V-11")
G.add_edge("V-11", "V-12")
G.add_edge("V-11", "Sem Limpeza")
G.add_edge("Sem Limpeza", "Sem Secador")
G.add_edge("Sem Secador", "CT-04")
G.add_edge("V-12", "V-53")
G.add_edge("V-12", "Sem Limpeza")
G.add_edge("Sem Secador", "CT-03")
G.add_edge("CT-04", "SP-06")
G.add_edge("CT-04", "SP-07")
G.add_edge("CT-04", "SP-08")
G.add_edge("CT-04", "SP-09")
G.add_edge("CT-04", "SP-10")
G.add_edge("CT-03", "SP-01")
G.add_edge("CT-03", "SP-02")
G.add_edge("CT-03", "SP-03")
G.add_edge("CT-03", "SP-04")
G.add_edge("CT-03", "SP-05")

# Rotas
rotas = [f"Rota {i+1}" for i in range(10)]

# Inicializações
if "rotas_ativas" not in st.session_state:
    st.session_state["rotas_ativas"] = {}

if "status_rotas" not in st.session_state:
    st.session_state["status_rotas"] = {i: "parado" for i in range(len(rotas))}

if "mensagens_rotas" not in st.session_state:
    st.session_state["mensagens_rotas"] = {i: {"erro": None, "sucesso": None} for i in range(len(rotas))}

st.title("Simulador de Rotas Industriais")

# Loop para exibir as rotas
for i, rota in enumerate(rotas):
    col1, col2, col3, col4, col5, col6, col7, col8 , col9, col10, col11 = st.columns([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2])

    with col1:
        st.write(f"**{rota}**")

    # Recupera os valores salvos anteriormente, se existirem
    valor_origem = st.session_state.get(f"origem_{i}", origens[0])
    valor_prelimpeza = st.session_state.get(f"prelimpeza_{i}", limpeza[0])
    valor_destino = st.session_state.get(f"destino_{i}", destinos[0])
    valor_secador = st.session_state.get(f"origemsecador_{i}", secador[0])

    with col2:
        origem = st.selectbox(
            "Origem", origens,
            index=origens.index(valor_origem) if valor_origem in origens else 0,
            key=f"select_origem_{i}"
        )

    with col3:
        prelimpeza = st.selectbox(
            "Pré Limpeza", limpeza,
            index=limpeza.index(valor_prelimpeza) if valor_prelimpeza in limpeza else 0,
            key=f"select_prelimpeza_{i}"
        )

    with col4:
        destino = st.selectbox(
            "Destino", destinos,
            index=destinos.index(valor_destino) if valor_destino in destinos else 0,
            key=f"select_destino_{i}"
        )

    with col5:
        origemsecador = st.selectbox(
            "Secador", secador,
            index=secador.index(valor_secador) if valor_secador in secador else 0,
            key=f"select_origemsecador_{i}"
        )

    with col6:
        comentario = st.text_input("Comentário", key=f"comentario_{i}")

    with col7:
        # Executar
        if st.button("▶️ Executar", key=f"executar_{i}"):
            if nx.has_path(G, origem, destino):
                caminho = nx.shortest_path(G, origem, destino)
                conflito = False
                for j, outro_caminho in st.session_state["rotas_ativas"].items():
                    if i == j:
                        continue
                    if set(zip(caminho, caminho[1:])) & set(zip(outro_caminho, outro_caminho[1:])):
                        conflito = True
                        st.session_state["mensagens_rotas"][i]["erro"] = f"⚠️ Conflito com {rotas[j]}!"
                        st.session_state["status_rotas"][i] = "parado"
                        break
                if not conflito:
                    st.session_state[f"origem_{i}"] = origem
                    st.session_state[f"destino_{i}"] = destino
                    st.session_state[f"prelimpeza_{i}"] = prelimpeza
                    st.session_state[f"origemsecador_{i}"] = origemsecador
                    st.session_state["status_rotas"][i] = "executando"
                    st.session_state["rotas_ativas"][i] = caminho
                    # limpa erro antigo
                    st.session_state["mensagens_rotas"][i]["erro"] = None
                    # define nova mensagem de sucesso
                    st.session_state["mensagens_rotas"][i]["sucesso"] = f"{rota}: {' → '.join(caminho)}"

            else:
                st.session_state["mensagens_rotas"][i]["erro"] = f"{rota}: Caminho inválido"
                st.session_state["status_rotas"][i] = "parado"

    with col8:
        # Pausar
        if st.button("⏸️ Pausar", key=f"pausar_{i}"):
            st.session_state["status_rotas"][i] = "pausado"

    with col9:
        # Parar
        if st.button("⏹️ Parar", key=f"parar_{i}"):
            st.session_state["status_rotas"][i] = "parado"
            st.session_state["rotas_ativas"].pop(i, None)
            st.session_state["mensagens_rotas"][i]["erro"] = None
            st.session_state["mensagens_rotas"][i]["sucesso"] = None

    with col10:
        status = st.session_state["status_rotas"][i]
        if status == "executando":
            st.markdown("🟢")
        elif status == "pausado":
            st.markdown("🟡")
        else:
            st.markdown("🔴")

    with col11:
        # Limpar mensagem de erro/sucesso
        mensagem_erro = st.session_state["mensagens_rotas"][i]["erro"]
        mensagem_sucesso = st.session_state["mensagens_rotas"][i]["sucesso"]

        if mensagem_erro:
            st.error(mensagem_erro)
        elif mensagem_sucesso:
            st.success(mensagem_sucesso)
