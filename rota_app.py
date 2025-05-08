import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

st.set_page_config(page_title="Simulador de Rotas", layout="wide")

# Criação do grafo direcionado
G = nx.DiGraph()

# Definindo os nós (origens, intermediários, destinos)
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

# Adicionando os nós no grafo
G.add_nodes_from(origens + intermediarios + limpeza + secador + destinos)

# Adicionando as arestas (exemplo simplificado)
G.add_edge("MOEGA 1", "V-1")
G.add_edge("V-1", "CT-1")
G.add_edge("CT-1", "V-2")
G.add_edge("V-2", "E-1")
G.add_edge("E-1", "Sem Limpeza")
G.add_edge("Sem Limpeza", "Sem Secador")
G.add_edge("Sem Secador", "CT-03")
G.add_edge("CT-03", "SP-01")

# Heurística para A*
def heuristica(n1, n2):
    return 1  # heurística neutra

def verifica_conflito(caminho, idx):
    pares_arestas = set(zip(caminho, caminho[1:]))
    for k, outro in st.session_state["rotas_ativas"].items():
        if k != idx:
            outros_pares = set(zip(outro, outro[1:]))
            if pares_arestas & outros_pares:
                return True
    return False

# Inicializações
rotas = [f"Rota {i+1}" for i in range(3)]
if "rotas_ativas" not in st.session_state:
    st.session_state["rotas_ativas"] = {}
if "status_rotas" not in st.session_state:
    st.session_state["status_rotas"] = {i: "parado" for i in range(len(rotas))}
if "mensagens_rotas" not in st.session_state:
    st.session_state["mensagens_rotas"] = {i: {"erro": None, "sucesso": None} for i in range(len(rotas))}

st.title("Simulador de Rotas Industriais")

for i, rota in enumerate(rotas):
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        origem = st.selectbox(f"Origem {rota}", origens, key=f"origem_{i}")
    with col2:
        limpeza_selec = st.selectbox(f"Limpeza {rota}", limpeza, key=f"limpeza_{i}")
    with col3:
        secagem = st.selectbox(f"Secador {rota}", secador, key=f"secador_{i}")
    with col4:
        destino = st.selectbox(f"Destino {rota}", destinos, key=f"destino_{i}")
    with col5:
        if st.button("Executar", key=f"executar_{i}"):
            rota_completa = [origem]
            if limpeza_selec != "Sem Limpeza":
                rota_completa.append(limpeza_selec)
            if secagem != "Sem Secador":
                rota_completa.append(secagem)
            rota_completa.append(destino)

            caminho = []
            conflito = False

            for j in range(len(rota_completa) - 1):
                o, d = rota_completa[j], rota_completa[j+1]
                trecho_ok = False

                # 1. Caminho mais curto direto
                try:
                    sub = nx.shortest_path(G, o, d)
                    if not verifica_conflito(sub, i):
                        if j > 0:
                            sub = sub[1:]
                        caminho.extend(sub)
                        trecho_ok = True
                except:
                    pass

                # 2. Todas as alternativas mais curtas
                if not trecho_ok:
                    try:
                        for alt in nx.all_shortest_paths(G, o, d):
                            if not verifica_conflito(alt, i):
                                if j > 0:
                                    alt = alt[1:]
                                caminho.extend(alt)
                                trecho_ok = True
                                break
                    except:
                        pass

                # 3. A* fallback
                if not trecho_ok:
                    try:
                        astar = nx.astar_path(G, o, d, heuristic=heuristica)
                        if not verifica_conflito(astar, i):
                            if j > 0:
                                astar = astar[1:]
                            caminho.extend(astar)
                            trecho_ok = True
                    except:
                        pass

                if not trecho_ok:
                    conflito = True
                    st.session_state["mensagens_rotas"][i]["erro"] = f"Conflito em {o} → {d}"
                    st.session_state["status_rotas"][i] = "parado"
                    break

            if not conflito:
                st.session_state["rotas_ativas"][i] = caminho
                st.session_state["status_rotas"][i] = "executando"
                st.session_state["mensagens_rotas"][i]["erro"] = None
                st.session_state["mensagens_rotas"][i]["sucesso"] = f"{rota}: {' → '.join(caminho)}"

    st.text(st.session_state["mensagens_rotas"][i]["erro"] or st.session_state["mensagens_rotas"][i]["sucesso"] or "")
