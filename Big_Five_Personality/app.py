import streamlit as st

# Configuração de página
st.set_page_config(
    page_title='Teste de personalidade',
    page_icon=':brain:',
    layout='wide',
)

# Lendo as perguntas do arquivo
with open('questions.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()

questions = [line[6:].strip() for line in lines]
answers = []

# Inicializa um estado para controlar se o formulário foi enviado
if 'submitted' not in st.session_state:
    st.session_state.submitted = False

# Se o botão "Enviar Respostas" não foi clicado, mostra o questionário
if not st.session_state.submitted:
    with st.container():
        for question in questions:
            answer = st.radio(
                label=question,
                options=[1, 2, 3, 4, 5],
                horizontal=True,
            )
            answers.append(answer)

        # Quando o botão é clicado, muda o estado para ocultar as perguntas
        if st.button("Enviar Respostas"):
            st.session_state.submitted = True
            st.rerun()

# Se o formulário foi enviado, exibe apenas a mensagem "LEGAL!"
if st.session_state.submitted:
    st.markdown("LEGAL!")
    
