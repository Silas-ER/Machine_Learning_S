import streamlit as st
from main import get_personality

# Configuração de página
st.set_page_config(
    page_title='Teste de personalidade',
    page_icon=':brain:',
    layout='wide',
)

# configurações de css
st.markdown(
    """
    <style>
        p {
            text-align: center !important; 
        }
        h1 {
            text-align: center !important; 
        }
        #stWidgetLabel{
            text-align: center !important; 
        }
        .st-emotion-cache-ue6h4q {
            justify-content: center;
        }
        .st-ae{
            justify-content: center !important;
        }
        .stButton > button {
            display: block;
            margin: 0 auto;
        }
    </style>
    """, unsafe_allow_html=True)

# Lendo as perguntas do arquivo
with open('questions.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()

questions = [line[5:].strip() for line in lines]
answers = []

# Inicializa um estado para controlar se o formulário foi enviado
if 'submitted' not in st.session_state:
    st.session_state.submitted = False

# Inicializa o estado para armazenar as respostas
if 'answers' not in st.session_state:
    st.session_state.answers = [None] * len(questions)

st.markdown('# BIG FIVE PERSONALITY')
if not st.session_state.submitted:
    with st.container():
        for i in range(0, len(questions), 5):
            cols = st.columns(5)
            for j in range(5):
                if i + j < len(questions):
                    with cols[j]:
                        st.session_state.answers[i + j] = st.radio(
                            label=questions[i + j],
                            options=[1, 2, 3, 4, 5],
                            horizontal=True,
                            key=f"{i + j}"
                        )
                        #answers.append(answer)
        st.markdown("")

        # Quando o botão é clicado, muda o estado para ocultar as perguntas
        if st.button("Enviar Respostas"):
            st.session_state.submitted = True
            st.rerun()

# Se o formulário foi enviado, exibe os resultados:
if st.session_state.submitted:
    st.markdown("Resultados: ")
    get_personality(st.session_state.answers)

    if st.button("Voltar"):
        st.session_state.submitted = False
        st.session_state.answers = [None] * len(questions)
        st.rerun()
