for i, rota in enumerate(rotas):
    with st.form(key=f"form_rota_{i}"):
        col1, col2, col3, col4 = st.columns([1, 3, 3, 4])
        
        with col1:
            st.write(f"**{rota}**")
        
        with col2:
            origem = st.selectbox(
                f"Origem {rota}", list(G.nodes),
                index=list(G.nodes).index(st.session_state.get(f"origem_{i}", list(G.nodes)[0])),
                key=f"select_origem_{i}"
            )
        
        with col3:
            destino = st.selectbox(
                f"Destino {rota}", list(G.nodes),
                index=list(G.nodes).index(st.session_state.get(f"destino_{i}", list(G.nodes)[1])),
                key=f"select_destino_{i}"
            )

        with col4:
            submit = st.form_submit_button(f"Mostrar")

        if submit:
            st.session_state[f"origem_{i}"] = origem
            st.session_state[f"destino_{i}"] = destino

            if nx.has_path(G, origem, destino):
                caminho = nx.shortest_path(G, origem, destino)
                st.success(f"{rota}: {origem} → {destino}: {' → '.join(caminho)}")
                desenha_rota(caminho)
            else:
                st.error(f"{rota}: Sem caminho entre {origem} e {destino}")
