for i, rota in enumerate(rotas):
    with st.form(key=f"form_rota_{i}"):
        col1, col2, col3, col4, col5, col6, col7, col8 , col9, col10, col11 = st.columns([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2])

        with col1:
            st.write(f"**{rota}**")

        with col2:
            origem = st.selectbox(
                "Origem", origens,
                index=origens.index(st.session_state.get(f"origem_{i}", origens[0])),
                key=f"select_origem_{i}"
            )

        with col3:
            prelimpeza = st.selectbox(
                "Pré Limpeza", limpeza,
                index=limpeza.index(st.session_state.get(f"prelimpeza_{i}", limpeza[0])),
                key=f"select_prelimpeza_{i}"
            )

        with col4:
            destino = st.selectbox(
                "Destino", destinos,
                index=destinos.index(st.session_state.get(f"destino_{i}", destinos[0])),
                key=f"select_destino_{i}"
            )

        with col5:
            origemsecador = st.selectbox(
                "Secador", secador,
                index=secador.index(st.session_state.get(f"origemsecador_{i}", secador[0])),
                key=f"select_origemsecador_{i}"
            )

        with col6:
            comentario = st.text_input("Comentário", key=f"comentario_{i}")

        with col7:
            executar = st.form_submit_button("▶️")

        with col8:
            pausar = st.form_submit_button("⏸️")

        with col9:
            parar = st.form_submit_button("⏹️")

        with col10:
            status = st.session_state["status_rotas"][i]
            if status == "executando":
                st.markdown("🟢")
            elif status == "pausado":
                st.markdown("🟡")
            else:
                st.markdown("🔴")

        with col11:
            if executar:
                if nx.has_path(G, origem, destino):
                    caminho = nx.shortest_path(G, origem, destino)

                    conflito = False
                    for j, outro_caminho in st.session_state["rotas_ativas"].items():
                        if i == j:
                            continue
                        if set(zip(caminho, caminho[1:])) & set(zip(outro_caminho, outro_caminho[1:])):
                            conflito = True
                            st.session_state["status_rotas"][i] = "parado"
                            st.error(f"⚠️ Conflito com {rotas[j]}!")
                            break

                    if not conflito:
                        st.session_state[f"origem_{i}"] = origem
                        st.session_state[f"destino_{i}"] = destino
                        st.session_state["status_rotas"][i] = "executando"
                        st.session_state["rotas_ativas"][i] = caminho
                        st.success(f"{rota}: {' → '.join(caminho)}")
                else:
                    st.session_state["status_rotas"][i] = "parado"
                    st.error(f"{rota}: Caminho inválido")

            elif pausar:
                st.session_state["status_rotas"][i] = "pausado"

            elif parar:
                st.session_state["status_rotas"][i] = "parado"
                st.session_state["rotas_ativas"].pop(i, None)
