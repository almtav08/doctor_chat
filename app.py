import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_URL = os.environ.get("API_URL")
API_KEY = os.environ.get("API_KEY")

# Parámetros configurables
st.sidebar.title("Configuración del Chatbot")
personalidad = st.sidebar.text_input("Personalidad", "Amable y empático")
edad = st.sidebar.number_input("Edad", min_value=0, max_value=120, value=35)
sexo = st.sidebar.selectbox("Sexo", ["Femenino", "Masculino", "Otro"], index=0)
motivo_consulta = st.sidebar.text_input(
    "Motivo de consulta", "Dolor de cabeza persistente"
)
sintomas_adicionales = st.sidebar.text_input("Síntomas adicionales", "Ninguno")
antecedentes = st.sidebar.text_input(
    "Antecedentes médicos", "Sin antecedentes médicos relevantes"
)
medicacion = st.sidebar.text_input("Medicación actual", "Paracetamol ocasional")
alergias = st.sidebar.text_input("Alergias", "Ninguna")
pruebas_realizadas = st.sidebar.text_input("Pruebas realizadas", "Ninguna")
max_tokens = st.sidebar.slider("Máximo de tokens", 50, 1000, 150)

def get_system_propmt():
    return {
        "role": "system",
        "content": (
            "Actúa como un paciente en una simulación clínica.\n"
            "Tu perfil es el siguiente:\n"
            f"- Personalidad: {personalidad}\n"
            f"- Edad: {edad} años\n"
            f"- Sexo: {sexo}\n"
            f"- Motivo de consulta: {motivo_consulta}\n"
            f"- Síntomas adicionales: {sintomas_adicionales}\n"
            f"- Antecedentes personales: {antecedentes}\n"
            f"- Medicación actual: {medicacion}\n"
            f"- Alergias: {alergias}\n\n"
            f"- Pruebas realizadas: {pruebas_realizadas}\n"
            "Responde a las preguntas como si fueras este paciente.\n"
            "No hagas diagnósticos ni utilices terminología médica compleja.\n"
            "No proporciones información adicional que no esté definida explícitamente o que no sea razonable deducir como un paciente común.\n"
            "Mantén coherencia con tu perfil y responde solo cuando se te hagan preguntas, como si estuvieras en una consulta médica real."
        ),
    }

def get_response():
    messages = [get_system_propmt()]
    for msg in st.session_state.messages:
        messages.append(msg)

    data = {
        "model": "meta-llama/llama-4-maverick:free",
        "messages": messages,
        "max_tokens": max_tokens,
    }

    response = requests.post(API_URL, headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}, json=data)
    information = response.json()
    return information["choices"][0]["message"]["content"]

# Historial de mensajes
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("Chatbot Médico")

# Mostrar historial
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input del usuario
if user_input := st.chat_input("Haz tus preguntas aquí..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Aquí simulas una respuesta (puedes reemplazar con llamada a OpenAI u otro modelo)
    response = get_response()
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
