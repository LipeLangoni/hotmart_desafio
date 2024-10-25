import json
import requests
import streamlit as st

st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://samadhidigital.com.br/wp-content/uploads/2024/04/como-funciona-a-hotmart.png");
        background-size: cover;
    }
    </style>
    """,
    unsafe_allow_html=True
)



pergunta1 = "Um produtor pode ser um blogueiro?"
pergunta2 = "Como funciona a hotmart?"
pergunta3 = "Como Vender com a Hotmart?"

perguntas = [pergunta1,pergunta2,pergunta3]

def extract_history(window):
    return "\n\n".join([f"{message['role']}:{message['content']}\n" for message in st.session_state.messages[-window:]])


st.title("Hotmart Chat")

st.info("""Disclaimer: Apenas para fins de teste""")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "first_interaction" not in st.session_state:
    st.session_state.first_interaction = False

if "is_processing" not in st.session_state:
    st.session_state.is_processing = False

for message in st.session_state.messages:
    if message["role"] == "assistant":
        st.chat_message(message["role"]).write(message["content"])
    else:
        st.chat_message(message["role"]).write(message["content"])
       
if not st.session_state.first_interaction:
    for pergunta in perguntas:
        if st.button(pergunta):
            st.chat_message("user").write(pergunta)
            st.session_state.is_processing = True
            st.session_state.current_prompt = pergunta
            st.rerun()

if prompt := st.chat_input("Digite sua pergunta sobre emendas orçamentárias", disabled=st.session_state.is_processing):
    st.session_state.is_processing = True
    st.session_state.current_prompt = prompt
    st.rerun()

if st.session_state.is_processing and 'current_prompt' in st.session_state:
    st.chat_message("user").write(st.session_state.current_prompt)
    
    with st.spinner("Pensando..."):
        response = requests.post(url="http://service1:8000/chat",json={"text":st.session_state.current_prompt})


    st.session_state.messages.append({"role": "user", "content": st.session_state.current_prompt})
    
    st.chat_message("assistant").write(json.loads(response.content.decode('utf-8'))["result"]["content"])

    st.session_state.messages.append({"role": "assistant", "content": json.loads(response.content.decode('utf-8'))["result"]["content"]})
    st.session_state.first_interaction = True
    st.session_state.is_processing = False
    del st.session_state.current_prompt
    st.rerun()
st.write("<p style='padding-bottom: 50px;'></p>", unsafe_allow_html=True)

