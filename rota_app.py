import streamlit as st
import networkx as nx

st.set_page_config(page_title="Simulador de Rotas", layout="wide")

G = nx.DiGraph()

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

rotas = [f"Rota {i+1}" for i in range(10)]

if "rotas_ativas" not in st.session_state:
    st.session_state["rotas_ativas"] = {}
if "status_rotas" not in st.session_state:
    st.session_state["status_rotas"] = {i: "parado" for i in range(len(rotas))}
if "mensagens_rotas" not in st.session_state:
    st.session_state["mensagens_rotas"] = {i: {"erro": None, "sucesso": None} for i in range(len(rotas))}

st.title("Simulador de Rotas Industriais")

for i, rota in enumerate(rotas):
    col1, col2, col3, col4, col5, col6, col7, col8 , col9, col10, col11 = st.columns([1]*10 + [2])

    with col1:
        st.write(f"**{rota}**")

    valor_origem = st.session_state.get(f"origem_{i}", origens[0])
    valor_prelimpeza = st.session_state.get(f"prelimpeza_{i}", limpeza[0])
    valor_destino = st.session_state.get(f"destino_{i}", destinos[0])
    valor_secador = st.session_state.get(f"origemsecador_{i}", secador[0])

    with col2:
        origem = st.selectbox("Origem", origens, index=origens.index(valor_origem), key=f"select_origem_{i}")
    with col3:
        prelimpeza = st.selectbox("Pré Limpeza", limpeza, index=limpeza.index(valor_prelimpeza), key=f"select_prelimpeza_{i}")
    with col4:
        destino = st.selectbox("Destino", destinos, index=destinos.index(valor_destino), key=f"select_destino_{i}")
    with col5:
        origemsecador = st.selectbox("Secador", secador, index=secador.index(valor_secador), key=f"select_origemsecador_{i}")
    with col6:
        comentario = st.text_input("Comentário", key=f"comentario_{i}")

    with col7:
        executar = st.button("▶️ Executar", key=f"executar_{i}")
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
        msg_erro = st.session_state["mensagens_rotas"][i]["erro"]
        msg_sucesso = st.session_state["mensagens_rotas"][i]["sucesso"]
        if msg_erro:
            st.error(msg_erro)
        elif msg_sucesso:
            st.success(msg_sucesso)

    if executar:
        rota_completa = [origem]
        if prelimpeza != "Sem Limpeza":
            rota_completa.append(prelimpeza)
        if origemsecador != "Sem Secador":
            rota_completa.append(origemsecador)
        rota_completa.append(destino)

        rota_valida = all(nx.has_path(G, rota_completa[k], rota_completa[k+1]) for k in range(len(rota_completa)-1))

        if rota_valida:
            caminho = []
            conflito = False
            for j in range(len(rota_completa) - 1):
                origem_trecho = rota_completa[j]
                destino_trecho = rota_completa[j + 1]
                try:
                    for sub in nx.all_shortest_paths(G, origem_trecho, destino_trecho):
                        pares_arestas = set(zip(sub, sub[1:]))
                        conflito_local = any(
                            pares_arestas & set(zip(outra, outra[1:]))
                            for k2, outra in st.session_state["rotas_ativas"].items() if k2 != i
                        )
                        if not conflito_local:
                            if j > 0:
                                sub = sub[1:]
                            caminho.extend(sub)
                            break
                    else:
                        conflito = True
                        st.session_state["mensagens_rotas"][i]["erro"] = f"⚠️ Conflito no trecho: {origem_trecho} → {destino_trecho}"
                        st.session_state["status_rotas"][i] = "parado"
                        break
                except nx.NetworkXNoPath:
                    conflito = True
                    st.session_state["mensagens_rotas"][i]["erro"] = f"❌ Sem caminho de {origem_trecho} para {destino_trecho}"
                    st.session_state["status_rotas"][i] = "parado"
                    break

            if not conflito:
                st.session_state[f"origem_{i}"] = origem
                st.session_state[f"destino_{i}"] = destino
                st.session_state[f"prelimpeza_{i}"] = prelimpeza
                st.session_state[f"origemsecador_{i}"] = origemsecador
                st.session_state["status_rotas"][i] = "executando"
                st.session_state["rotas_ativas"][i] = caminho
                st.session_state["mensagens_rotas"][i]["erro"] = None
                st.session_state["mensagens_rotas"][i]["sucesso"] = f"{rota}: {' → '.join(caminho)}"
        else:
            st.session_state["mensagens_rotas"][i]["erro"] = f"{rota}: Caminho inválido"
            st.session_state["status_rotas"][i] = "parado"
