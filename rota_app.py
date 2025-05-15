import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import re  # função eurística

def heuristica_no_simples(u, v):
    def extrair_numero(no):
        match = re.search(r'\d+', no)
        return int(match.group()) if match else 0
    return abs(extrair_numero(u) - extrair_numero(v))

st.set_page_config(page_title="Simulador de Rotas", layout="wide")

# Criação do grafo direcionado
G = nx.DiGraph()

# Definindo os nós (origens, intermediários, destinos)
vb = [f"V-{i}" for i in range(1, 81)]  # declarado 80 valvulas
el = [f"E-{i}" for i in range(1, 21)]  # declarado 20 elevadores
ct = [f"CT-{i}" for i in range(1, 71)]  # declarado 70 cts
rt = [f"RT-{i}" for i in range(1, 10)]  # declarado 10 rts
tc = [f"TC-{i}" for i in range(1, 10)]  # declarado 10 tcs
vr = [f"VR-{i}" for i in range(1, 10)]  # declarado 10 vrs
val = [f"VAL-{i}" for i in range(1, 10)]  # declarado 30 vals

origens = ["MOEGA 1", "MOEGA 2", "SP-01", "SP-02", "SP-03", "SP-04", "SP-05", "SP-06", "SP-07", "SP-08", "SP-09", "SP-10", "SA-01", "SA-02", "SA-03", "SA-04", "SA-05", "SA-06", "SA-07", "SA-08"]
intermediarios = vb + el + ct + rt + tc + vr + val + ["CT-201", "V-201", "V-202"]
limpeza = [" ","MLP-1", "MLP-2", "MLP-3", "MLP-4"]
secador = [" ", "SEC-1", "SEC-2"]
destinos = ["SP-01", "SP-02", "SP-03", "SP-04", "SP-05", "SP-06", "SP-07", "SP-08", "SP-09", "SP-10", "SA-01", "SA-02", "SA-03", "SA-04", "SA-05", "SA-06", "SA-07", "SA-08", "SIL-01", "SIL-02", "SIL-03", "SIL-04", "SIL-05"]

# Adicionando os nós no grafo
G.add_nodes_from(origens + intermediarios + destinos + limpeza + secador)


# ---------------------------------------------------CT - CORREIAS TRANSPORTADORAS---------------------------------------------------
arestas_ct = [
    ("CT-1", "V-7"),
    ("CT-2", "V-8"),
    ("CT-3", "SP-01"),
    ("CT-3", "SP-02"),
    ("CT-3", "SP-03"),
    ("CT-3", "SP-04"),
    ("CT-3", "SP-05"),
    ("CT-4", "SP-06"),
    ("CT-4", "SP-07"),
    ("CT-4", "SP-08"),
    ("CT-4", "SP-09"),
    ("CT-4", "SP-10"),
    ("CT-5", "V-9"),
    ("CT-6", "V-10"),
    ("CT-7", "V-19"),
    ("CT-8", "V-19"),
    ("CT-9", "V-28"),
    ("CT-10", "V-29"),
    ("CT-11", "E-5"),
    ("CT-12", "V-37"),
    ("CT-13", "V-39"),
    ("CT-14", "CT-16"), # SAIDA 1 - MANDA PARA SA1-4
    ("CT-14", "CT-17"), # SAIDA 2 - MANDA PARA SA4-8
    ("CT-15", "CT-16"),
    ("CT-15", "CT-17"),
    ("CT-16", "SA-01"),
    ("CT-16", "SA-02"),
    ("CT-16", "SA-03"),
    ("CT-16", "SA-04"),
    ("CT-17", "SA-05"),
    ("CT-17", "SA-06"),
    ("CT-17", "SA-07"),
    ("CT-17", "SA-08"),
    ("CT-18", "E-10"), # CAMINHO PARA EXPEDIÇÃO
    ("CT-19", "E-11"), # CAMINHO PARA EXPEDIÇÃO
    ("CT-20", "V-201"), # SAIDA 1
    ("CT-20", "V-43"), # SAIDA 2
    ("CT-21", "TC-3"), # CAMINHO SILOS DE EXPEDIÇÃO
    ("CT-22", "TC-3"), # CAMINHO SILOS DE EXPEDIÇÃO
    ("CT-23", "CT-16"), # CAMINHO PARA SILOS ARMAZENAMENTO 1-4
    ("CT-23", "V-60"), # CAMINHO PARA SILOS ARMAZENAMENTO 5-8 OU EXPEDIÇÃO
    ("CT-23", "V-55"), # SAIDA 1
    ("CT-59", "E-6"), # SAIDA 1
    ("CT-60", "V-61"), # SAIDA 1
    ("CT-201", "V-202"), # SAIDA 1    
]

# Adicionando todas as arestas de uma vez
G.add_edges_from(arestas_ct)

# ---------------------------------------------------ELEVADORES---------------------------------------------------
arestas_elevadores = [
    ("E-1", "V-11"), # SAIDA UNICA
    ("E-2", "V-13"), # SAIDA UNICA
    ("E-3", "V-15"), # SAIDA UNICA
    ("E-4", "V-17"), # SAIDA UNICA
    ("E-5", "V-30"), # SAIDA UNICA
    ("E-6", "V-32"), # SAIDA UNICA
    ("E-7", "V-33"), # SAIDA UNICA
    ("E-8", "V-49"), # SAIDA UNICA
    ("E-9", "V-35"), # SAIDA UNICA
    ("E-10", "V-44"), # SAIDA UNICA
    ("E-11", "V-47"), # SAIDA UNICA
]
G.add_edges_from(arestas_elevadores)


# --------------------------------------------------- MOEGAS ---------------------------------------------------
arestas_moegas = [
    ("MOEGA 1", "V-1"),
    ("MOEGA 2", "V-4"),
]
G.add_edges_from(arestas_moegas)

# --------------------------------------------------- MLP - MAQUINAS DE LIMPEZA ---------------------------------------------------
arestas_mlp = [
    ("MLP-1", "V-24"),
    ("MLP-2", "V-25"),
    ("MLP-3", "V-26"),
    ("MLP-4", "V-58"),
]
G.add_edges_from(arestas_mlp)


# ---------------------------------------------------SA - SILOS ARMAZENADORES---------------------------------------------------
arestas_sa = [
    ("SA-1", "CT-18"), # SA 1
    ("SA-2", "CT-18"), # SA 2
    ("SA-3", "CT-18"), # SA 3
    ("SA-4", "CT-18"), # SA 4

    ("SA-5", "CT-19"), # SA 5
    ("SA-6", "CT-19"), # SA 6
    ("SA-7", "CT-19"), # SA 7
    ("SA-8", "CT-19"), # SA 8
]
G.add_edges_from(arestas_sa)

# ---------------------------------------------------SP - SILOS ARMAZENADORES---------------------------------------------------
arestas_sp = [
    ("SP-01", "CT-5"), # SP 1
    ("SP-02", "CT-5"), # SP 2
    ("SP-03", "CT-5"), # SP 3
    ("SP-04", "CT-5"), # SP 4
    ("SP-05", "CT-5"), # SP 5

    ("SP-06", "CT-6"), # SP 6
    ("SP-07", "CT-6"), # SP 7
    ("SP-08", "CT-6"), # SP 8
    ("SP-09", "CT-6"), # SP 9
    ("SP-10", "CT-6"), # SP 10
]
G.add_edges_from(arestas_sp)

# ---------------------------------------------------SC - SECADORES---------------------------------------------------
arestas_sec = [
    ("SEC-1", "CT-12"), # SECADOR 1
    ("SEC-2", "CT-13"), # SECADOR 2
]
G.add_edges_from(arestas_sec)

# ---------------------------------------------------TC---------------------------------------------------
arestas_tc = [
    ("TC-1", "SEC-1"), # SAIDA 1 - VEM E-5, 6, 7, 8, 9
    ("TC-2", "SEC-2"), # SAIDA 1
    ("TC-3", "SIL-01"), # EXPEDIÇÃO
    ("TC-3", "SIL-02"), # EXPEDIÇÃO
    ("TC-3", "SIL-03"), # EXPEDIÇÃO
    ("TC-3", "SIL-04"), # EXPEDIÇÃO
    ("TC-3", "SIL-05"), # EXPEDIÇÃO
]
G.add_edges_from(arestas_tc)
# ---------------------------------------------------VALVULAS---------------------------------------------------
arestas_val = [
("V-1", "CT-1"), # SAIDA 1
("V-1", "CT-2"), # SAIDA 2
("V-4", "CT-1"), # SADIA 1
("V-4", "CT-2"), # SAIDA 2
("V-7", "E-1"), # SAIDA 1
("V-7", "E-3"), # SAIDA 2
("V-8", "E-2"), # SAIDA 1
("V-8", "E-4"), # SAIDA 2
("V-9", "E-3"), # SAIDA 1
("V-9", "E-4"), # SAIDA 2
("V-10", "E-3"), # SAIDA 1
("V-10", "E-4"), # SAIDA 2
("V-11", "V-12"), # SAIDA 1
("V-11", "CT-4"), # CT4 manda para os SP06-10
("V-12", "V-53"), # SAIDA 2
("V-12", "CT-3"), # CT3 manda para os SP01-05
("V-13", "CT-3"), # SAIDA 1 - SP1-SP5
("V-13", "V-14"), # SAIDA 2 
("V-14", "CT-4"), # SAIDA 1 - SP6-SP10
("V-14", "CT-8"), # 
("V-15", "CT-3"), # SAIDA 1 - CAMINHO PARA SP-1 - 5
("V-15", "V-16"), # SAIDA 2
("V-16", "V-54"), # SAIDA 1
("V-16", "CT-22"), # SAIDA 2
("V-17", "CT-8"), # SAIDA 1 - CAMINHO PARA MPL'S E SECADORES
("V-17", "CT-4"), # SAIDA 2 - CAMINHO PARA SP-6 - 10
("V-18", "MLP-3"), # SAIDA 1
("V-18", "MLP-1"), # SAIDA 2
("V-19", "MLP-1"), # SAIDA 1
("V-19", "V-20"), # SAIDA 2
("V-20", "CT-9"), # SAIDA 1
("V-20", "V-21"), # SAIDA 2
("V-21", "MLP-2"), # SAIDA 1
("V-21", "MLP-3"), # SAIDA 2
("V-22", "MLP-2"), # SAIDA 1
("V-22", "V-23"), # SAIDA 2
("V-23", "MLP-3"), # SAIDA 1
("V-23", "CT-10"), # SAIDA 2
("V-24", "CT-9"), # SAIDA 1
("V-24", "CT-10"), # SAIDA 2
("V-25", "CT-9"), # SAIDA 1
("V-25", "CT-10"), # SAIDA 2
("V-26", "V-27"), # SAIDA 1
("V-26", "CT-10"), # SAIDA 2
("V-27", "CT-9"), # SAIDA 1
("V-27", "CT-11"), # SAIDA 2
("V-28", "E-7"), # SAIDA 1
("V-28", "E-6"), # SAIDA 2
("V-29", "E-8"), # SAIDA 1
("V-29", "E-9"), # SAIDA 2
("V-30", "V-31"), # SAIDA 1
("V-30", "CT-22"), # SAIDA 2
("V-31", "V-56"), # SAIDA 1
("V-31", "TC-1"), # SAIDA 2 - E-5
("V-32", "V-57"), # SAIDA 1
("V-32", "TC-1"), # SAIDA 2 - E-6
("V-33", "CT-20"), # SAIDA 1
("V-33", "V-34"), # SAIDA 2
("V-34", "CT-14"), # SAIDA 1 - CT-14 É CAMINHO PARA SILOS SA 1-4
("V-34", "V-48"), # SAIDA 2
("V-35", "V-36"), # SAIDA 1
("V-35", "CT-20"), # SAIDA 2
("V-36", "V-51"), # SAIDA 1
("V-36", "CT-15"), # SAIDA 2
("V-37", "V-38"), # SAIDA 1
("V-37", "V-41"), # SAIDA 2
("V-38", "E-5"), # SAIDA 1
("V-38", "E-8"), # SAIDA 2
("V-39", "V-40"), # SAIDA 1
("V-39", "V-42"), # SAIDA 2
("V-40", "E-5"), # SAIDA 1
("V-40", "E-6"), # SAIDA 2
("V-41", "E-6"), # SAIDA 1
("V-41", "E-7"), # SAIDA 2
("V-42", "E-8"), # SAIDA 1
("V-42", "E-9"), # SAIDA 2
("V-43", "E-9"), # SAIDA 1
("V-43", "E-7"), # SAIDA 2
("V-44", "V-45"), # SAIDA 1
("V-44", "CT-16"), # SAIDA 2
("V-45", "V-46"), # SAIDA 1
("V-45", "CT-20"), # SAIDA 2
("V-46", "CT-21"), # SAIDA 1
("V-46", "CT-15"), # SAIDA 2
("V-47", "V-52"), # SAIDA 1
("V-47", "CT-17"), # SAIDA 2
("V-48", "TC-2"), # SAIDA 1 - E7
("V-48", "TC-1"), # SAIDA 2 - E7
("V-49", "V-50"), # SAIDA 1 - E7
("V-49", "CT-14"), # SAIDA 2 - E7
("V-50", "TC-2"), # SAIDA 1 - E8
("V-50", "TC-1"), # SAIDA 2 - E8
("V-51", "TC-2"), # SAIDA 1 - E9
("V-51", "TC-1"), # SAIDA 2 - E9
("V-52", "CT-21"), # SAIDA 1 - E9
("V-52", "CT-20"), # SAIDA 2 - E9
("V-53", "CT-7"), # SAIDA 1
("V-53", "CT-23"), # SAIDA 2
("V-54", "CT-7"), # SAIDA 1
("V-54", "CT-23"), # SAIDA 2
("V-55", "MLP-3"), # SAIDA 1
("V-55", "MLP-4"), # SAIDA 2
("V-56", "MLP-3"), # SAIDA 1
("V-56", "MLP-4"), # SAIDA 2
("V-57", "MLP-3"), # SAIDA 1
("V-57", "MLP-4"), # SAIDA 2
("V-58", "V-59"), # SAIDA 1 ---------- TA ESTRANHO NO DESENHO
("V-58", "CT-10"), # SAIDA 2---------- TA ESTRANHO N DESENHO
("V-59", "V-59"), # SAIDA 1 ---------- TA ESTRANHO NO DESENHO
("V-59", "CT-10"), # SAIDA 2---------- TA ESTRANHO N DESENHO
("V-60", "CT-17"), # SAIDA 1
("V-60", "CT-60"), # SAIDA 2
("V-61", "E-10"), # SAIDA 1
("V-61", "E-11"), # SAIDA 2
("V-201", "CT-201"), # SAIDA 1
("V-201", "V-18"), # SAIDA 2
("V-202", "V-7"), # SAIDA 1
("V-202", "V-8"), # SAIDA 2
]
G.add_edges_from(arestas_val)


# Rotas
rotas = [f"Rota {i+1}" for i in range(10)]
if "rotas_ativas" not in st.session_state:
    st.session_state["rotas_ativas"] = {}

if "status_rotas" not in st.session_state:
    st.session_state["status_rotas"] = {i: "parado" for i in range(len(rotas))}

if "mensagens_rotas" not in st.session_state:
    st.session_state["mensagens_rotas"] = {i: {"erro": None, "sucesso": None} for i in range(len(rotas))}

st.title("Simulador de Rotas Industriais")

for i, rota in enumerate(rotas):
    col1, col2, col3, col4, col5, col6, col7, col8 , col9, col10, col11 = st.columns([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2])

    with col1:
        st.write(f"**{rota}**")

    valor_origem = st.session_state.get(f"origem_{i}", origens[0])
    valor_prelimpeza = st.session_state.get(f"prelimpeza_{i}", limpeza[0])
    valor_destino = st.session_state.get(f"destino_{i}", destinos[0])
    valor_secador = st.session_state.get(f"origemsecador_{i}", secador[0])

    with col2:
        origem = st.selectbox("Origem", origens, index=origens.index(valor_origem) if valor_origem in origens else 0, key=f"select_origem_{i}")

    with col3:
        prelimpeza = st.selectbox("Pré Limpeza", limpeza, index=limpeza.index(valor_prelimpeza) if valor_prelimpeza in limpeza else 0, key=f"select_prelimpeza_{i}")

    with col4:
        destino = st.selectbox("Destino", destinos, index=destinos.index(valor_destino) if valor_destino in destinos else 0, key=f"select_destino_{i}")

    with col5:
        origemsecador = st.selectbox("Secador", secador, index=secador.index(valor_secador) if valor_secador in secador else 0, key=f"select_origemsecador_{i}")

    with col6:
        comentario = st.text_input("Comentário", key=f"comentario_{i}")

    with col7:
        conflitos_detectados = []
       # Substitua TODO o bloco dentro do if st.button("▶️ Executar", key=f"executar_{i}"): 
# pelo seguinte código:

        if st.button("▶️ Executar", key=f"executar_{i}"):
            if nx.has_path(G, origem, destino):
                try:
            # 1. Primeiro tenta encontrar UM caminho com A* (mais rápido)
                    caminho_final = nx.astar_path(G, origem, destino, heuristic=heuristica_no_simples)
            
            # 2. Verificação simplificada de conflitos (apenas nós críticos)
                    nos_criticos = {"CT-14", "CT-15", "CT-16", "CT-17", "CT-20", "CT-21", "CT-22", "CT-23",
                                   "V-201", "V-202", "E-10", "E-11"}  # Adicione outros nós estratégicos
            
                    conflito = False
                    rotas_ativas = st.session_state["rotas_ativas"]
            
                    for j, outro_caminho in rotas_ativas.items():
                        if i == j:
                            continue
                
                # Verifica se compartilham nós críticos
                        if any(no in nos_criticos and no in outro_caminho for no in caminho_final):
                            conflito = True
                            break
            
                    if not conflito:
                        st.session_state[f"origem_{i}"] = origem
                        st.session_state[f"destino_{i}"] = destino
                        st.session_state[f"prelimpeza_{i}"] = prelimpeza
                        st.session_state[f"origemsecador_{i}"] = origemsecador
                        st.session_state["status_rotas"][i] = "executando"
                        st.session_state["rotas_ativas"][i] = caminho_final
                        st.session_state["mensagens_rotas"][i]["erro"] = None
                        st.session_state["mensagens_rotas"][i]["sucesso"] = f"{rota}: {' → '.join(caminho_final)}"
                    else:
                        st.session_state["mensagens_rotas"][i]["erro"] = f"{rota}: Conflito em nós críticos com outra rota ativa"
                        st.session_state["status_rotas"][i] = "parado"
                
                except nx.NetworkXNoPath:
                    st.session_state["mensagens_rotas"][i]["erro"] = f"{rota}: Caminho não encontrado"
                    st.session_state["status_rotas"][i] = "parado"
            else:
                st.session_state["mensagens_rotas"][i]["erro"] = f"{rota}: Origem e destino não conectados"
                st.session_state["status_rotas"][i] = "parado"

    with col8:
        if st.button("⏸️ Pausar", key=f"pausar_{i}"):
            st.session_state["status_rotas"][i] = "pausado"

    with col9:
        if st.button("⏹️ Parar", key=f"parar_{i}"):
            st.session_state["status_rotas"][i] = "parado"
            st.session_state["rotas_ativas"].pop(i, None)
            st.session_state["mensagens_rotas"][i]["erro"] = None
            st.session_state["mensagens_rotas"][i]["sucesso"] = None

    with col10:
        status = st.session_state["status_rotas"][i]
        st.markdown("🟢" if status == "executando" else "🟡" if status == "pausado" else "🔴")

    with col11:
        erro = st.session_state["mensagens_rotas"][i]["erro"]
        sucesso = st.session_state["mensagens_rotas"][i]["sucesso"]
        if erro:
            st.error(erro)
        if sucesso:
            st.success(sucesso)
