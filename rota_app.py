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
ct = [f"CT-{i}" for i in range(1, 51)]  # declarado 50 cts
rt = [f"RT-{i}" for i in range(1, 10)]  # declarado 10 rts
tc = [f"TC-{i}" for i in range(1, 10)]  # declarado 10 tcs
vr = [f"VR-{i}" for i in range(1, 10)]  # declarado 10 vrs
val = [f"VAL-{i}" for i in range(1, 10)]  # declarado 30 vals

origens = ["MOEGA 1", "MOEGA 2", "SP-01", "SP-02", "SP-03", "SP-04", "SP-05", "SP-06", "SP-07", "SP-08", "SP-09", "SP-10", "SA-01", "SA-02", "SA-03", "SA-04", "SA-05", "SA-06", "SA-07", "SA-08"]
intermediarios = vb + el + ct + rt + tc + vr + val + ["CT-201", "V-201", "V-202"]
limpeza = ["Sem Limpeza", "MLP-1", "MLP-2", "MLP-3", "MLP-4"]
secador = ["Sem Secador", "SEC-1", "SEC-2"]
destinos = ["SP-01", "SP-02", "SP-03", "SP-04", "SP-05", "SP-06", "SP-07", "SP-08", "SP-09", "SP-10", "SA-01", "SA-02", "SA-03", "SA-04", "SA-05", "SA-06", "SA-07", "SA-08", "SIL-01", "SIL-02", "SIL-03", "SIL-04", "SIL-05"]

# Adicionando os nós no grafo
G.add_nodes_from(origens + intermediarios + limpeza + secador + destinos)

# Adicionando as arestas
G.add_edge("MOEGA 1", "V-1")
G.add_edge("MOEGA 2", "V-4")

# V-1
G.add_edge("V-1", "CT-1") # SAIDA 1
G.add_edge("V-1", "CT-2") # SAIDA 2

# V-4
G.add_edge("V-4", "CT-1") # SADIA 1
G.add_edge("V-4", "CT-2") # SAIDA 2

# CT-1
G.add_edge("CT-1", "V-7")

# CT-2
G.add_edge("CT-2", "V-8")

# V-7
G.add_edge("V-7", "E-1") # SAIDA 1
G.add_edge("V-7", "E-3") # SAIDA 2

# V-8
G.add_edge("V-8", "E-2") # SAIDA 1
G.add_edge("V-8", "E-4") # SAIDA 2

# E-1
G.add_edge("E-1", "V-11")

# V11 
G.add_edge("V-11", "V-12") # SAIDA 1
G.add_edge("V-11", "Sem Limpeza") # CT4 manda para os SP06-10
G.add_edge("Sem Limpeza", "Sem Secador") # sem limpeza e sem secagem
G.add_edge("Sem Secador", "CT-04") # CT4 manda para os SP06-10

# V12 
G.add_edge("V-12", "V-53") # SAIDA 2
G.add_edge("V-12", "Sem Limpeza") # CT3 manda para os SP01-05
G.add_edge("Sem Limpeza", "Sem Secador") # sem limpeza e sem secagem
G.add_edge("Sem Secador", "CT-03") # CT3 manda para os SP01-05

# V53
G.add_edge("V-53", "CT-7") # SAIDA 1
G.add_edge("V-53", "CT-23") # SAIDA 2

# CT-7 - SAIDA UNICA
G.add_edge("CT-7", "V-19")

# V19 
G.add_edge("V-19", "MLP-1") # SAIDA 1
G.add_edge("V-19", "V-20") # SAIDA 2

# V20
G.add_edge("V-20", "CT-09") # SAIDA 1
G.add_edge("V-20", "V-21") # SAIDA 2

# V21
G.add_edge("V-21", "MLP-2") # SAIDA 1
G.add_edge("V-21", "MLP-3") # SAIDA 2

# CT-9 - SAIDA UNICA
G.add_edge("CT-9", "V-28")

# V28
G.add_edge("V-28", "E-7") # SAIDA 1
G.add_edge("V-28", "E-6") # SAIDA 2

# E-7
G.add_edge("E-7", "V-33") # SAIDA UNICA

# V-33
G.add_edge("V-33", "CT-20") # SAIDA 1
G.add_edge("V-33", "V-34") # SAIDA 2

# CT20
G.add_edge("CT-20", "V-201") # SAIDA 1
G.add_edge("CT-20", "V-43") # SAIDA 2

# V-201
G.add_edge("V-201", "CT-201") # SAIDA 1
G.add_edge("V-201", "V-18") # SAIDA 2

# CT-201
G.add_edge("CT-201", "V-202") # SAIDA 1

# V-202
G.add_edge("V-202", "V-7") # SAIDA 1
G.add_edge("V-202", "V-8") # SAIDA 2


# V-18
G.add_edge("V-18", "MLP-3") # SAIDA 1
G.add_edge("V-18", "MLP-1") # SAIDA 2

# V-43
G.add_edge("V-43", "E-9") # SAIDA 1
G.add_edge("V-43", "E-7") # SAIDA 2

# E-7
# E-9


# V-34
G.add_edge("V-34", "CT-14") # SAIDA 1 - CT-14 É CAMINHO PARA SILOS SA 1-4
G.add_edge("V-34", "V-48") # SAIDA 2

# CT-14
G.add_edge("CT-14", "CT-16") # SAIDA 1 - MANDA PARA SA1-4
G.add_edge("CT-14", "CT-17") # SAIDA 2 - MANDA PARA SA4-8

G.add_edge("CT-14", "Sem Limpeza") 
G.add_edge("Sem Limpeza", "Sem Secador") 
G.add_edge("Sem Secador", "CT-16") # SA1-4 SEM LIMPEZA E SECADOR
G.add_edge("Sem Secador", "CT-17") # SA5-8 SEM LIMPEZA E SECADOR

# CT-16 - SA1 AO 4
G.add_edge("CT-16", "SA-01")
G.add_edge("CT-16", "SA-02")
G.add_edge("CT-16", "SA-03")
G.add_edge("CT-16", "SA-04")

# CT-17 - SA5 AO 8
G.add_edge("CT-16", "SA-05")
G.add_edge("CT-16", "SA-06")
G.add_edge("CT-16", "SA-07")
G.add_edge("CT-16", "SA-08")



# caminho para SP06 - 10
G.add_edge("CT-04", "SP-06")
G.add_edge("CT-04", "SP-07")
G.add_edge("CT-04", "SP-08")
G.add_edge("CT-04", "SP-09")
G.add_edge("CT-04", "SP-10")

# caminho para SP01-05

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
        if st.button("▶️ Executar", key=f"executar_{i}"):

        # Lógica de construção do caminho completo
            rota_completa = [origem]
        if prelimpeza != "Sem Limpeza":
            rota_completa.append(prelimpeza)
        if origemsecador != "Sem Secador":
            rota_completa.append(origemsecador)
        rota_completa.append(destino)

        # Verificação do caminho válido no grafo, só após pressionar o botão
        rota_valida = all(nx.has_path(G, rota_completa[j], rota_completa[j + 1]) for j in range(len(rota_completa) - 1))

        if rota_valida:
            caminho = []
            conflito = False

            for j in range(len(rota_completa) - 1):
                origem_trecho = rota_completa[j]
                destino_trecho = rota_completa[j + 1]

                trecho_conflitante = True
                subcaminhos = []

                # Primeiro tenta o caminho mais curto
                try:
                    subcaminhos.append(nx.shortest_path(G, origem_trecho, destino_trecho))
                except nx.NetworkXNoPath:
                    pass

                if subcaminhos:
                    for sub in subcaminhos:
                        pares_arestas = set(zip(sub, sub[1:]))
                        conflito_local = any(
                            pares_arestas & set(zip(outro, outro[1:]))
                            for k, outro in st.session_state["rotas_ativas"].items() if k != i
                        )
                        if not conflito_local:
                            trecho_conflitante = False
                            if j > 0:
                                sub = sub[1:]
                            caminho.extend(sub)
                            break

                if trecho_conflitante:
                    # Se o caminho mais curto estiver com conflito, tenta alternativas
                    try:
                        for alt_sub in nx.all_simple_paths(G, origem_trecho, destino_trecho, cutoff=10):
                            pares_arestas = set(zip(alt_sub, alt_sub[1:]))
                            conflito_local = any(
                                pares_arestas & set(zip(outro, outro[1:]))
                                for k, outro in st.session_state["rotas_ativas"].items() if k != i
                            )
                            if not conflito_local:
                                trecho_conflitante = False
                                if j > 0:
                                    alt_sub = alt_sub[1:]
                                caminho.extend(alt_sub)
                                break
                    except nx.NetworkXNoPath:
                        pass

                if trecho_conflitante:
                    # Se mesmo as alternativas falharem, tenta a heurística
                    try:
                        sub = nx.astar_path(G, origem_trecho, destino_trecho, heuristic=heuristica_no_simples)
                        pares_arestas = set(zip(sub, sub[1:]))
                        conflito_local = any(
                            pares_arestas & set(zip(outro, outro[1:]))
                            for k, outro in st.session_state["rotas_ativas"].items() if k != i
                        )
                        if not conflito_local:
                            if j > 0:
                                sub = sub[1:]
                            caminho.extend(sub)
                            trecho_conflitante = False
                    except nx.NetworkXNoPath:
                        pass

                if trecho_conflitante:
                    conflito = True
                    # Inicializando mensagens de erro se não existir
                    if i not in st.session_state["mensagens_rotas"]:
                        st.session_state["mensagens_rotas"][i] = {}
                    st.session_state["mensagens_rotas"][i]["erro"] = f"⚠️ Conflito no trecho: {origem_trecho} → {destino_trecho}"
                    st.session_state["status_rotas"][i] = "parado"
                    break

            if not conflito:
                # Inicializando as mensagens de sucesso se não existir
                if i not in st.session_state["mensagens_rotas"]:
                    st.session_state["mensagens_rotas"][i] = {}

                st.session_state[f"origem_{i}"] = origem
                st.session_state[f"destino_{i}"] = destino
                st.session_state[f"prelimpeza_{i}"] = prelimpeza
                st.session_state[f"origemsecador_{i}"] = origemsecador
                st.session_state["status_rotas"][i] = "executando"
                st.session_state["rotas_ativas"][i] = caminho
                st.session_state["mensagens_rotas"][i]["erro"] = None
                st.session_state["mensagens_rotas"][i]["sucesso"] = f"{rota}: {' → '.join(caminho)}"
        else:
            # Inicializando as mensagens de erro se não existir
            if i not in st.session_state["mensagens_rotas"]:
                st.session_state["mensagens_rotas"][i] = {}
            st.session_state["mensagens_rotas"][i]["erro"] = f"{rota}: Caminho inválido"
            st.session_state["status_rotas"][i] = "parado"


    # Exibição de status e mensagens
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
        if status == "executando":
            st.markdown("🟢")
        elif status == "pausado":
            st.markdown("🟡")
        else:
            st.markdown("🔴")

    with col11:
        mensagem_erro = st.session_state["mensagens_rotas"][i]["erro"]
        mensagem_sucesso = st.session_state["mensagens_rotas"][i]["sucesso"]
        if mensagem_erro:
            st.error(mensagem_erro)
        elif mensagem_sucesso:
            st.success(mensagem_sucesso)
