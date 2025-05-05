import streamlit as st

# Inicialização de variáveis e setup (definição de origem e destino)
rotas = ['Rota 1', 'Rota 2', 'Rota 3', 'Rota 4']
origens = ['MOEGA 1', 'MOEGA 2']
destinos = ['SP1', 'SP2', 'SP3', 'SP4', 'SP5', 'SP6', 'SP7', 'SP8', 'SP9', 'SP10']

# Loop para cada rota
for i, rota in enumerate(rotas):
    with st.form(key=f"form_{i}"):  # Criando o formulário para cada rota
        # Origem e destino
        origem = st.selectbox(f"Origem da {rota}:", origens, key=f"origem_{i}")
        destino = st.selectbox(f"Destino para {rota}:", destinos, key=f"destino_{i}")
        
        # Botões de controle (Play, Pause, Stop)
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            play_button = st.button(f"▶️ Iniciar {rota}", key=f"play_{i}")
        with col2:
            pause_button = st.button(f"⏸️ Pausar {rota}", key=f"pause_{i}")
        with col3:
            stop_button = st.button(f"⏹️ Parar {rota}", key=f"stop_{i}")

        # LED status
        if play_button:
            st.session_state[f"status_{i}"] = "iniciada"
        elif pause_button:
            st.session_state[f"status_{i}"] = "pausada"
        elif stop_button:
            st.session_state[f"status_{i}"] = "parada"

        # Exibindo o LED de status
        if f"status_{i}" in st.session_state:
            status = st.session_state[f"status_{i}"]
            if status == "iniciada":
                st.write(f"LED da {rota}: 🔴 (Iniciada)")
            elif status == "pausada":
                st.write(f"LED da {rota}: 🟡 (Pausada)")
            elif status == "parada":
                st.write(f"LED da {rota}: 🟢 (Parada)")

        # Botão de envio do formulário
        submit_button = st.form_submit_button(f"▶️ Iniciar Rota {i}")

        if submit_button:
            st.session_state[f"rota_{i}_config"] = (origem, destino)
            st.success(f"Rota {i} configurada: {origem} -> {destino}")
