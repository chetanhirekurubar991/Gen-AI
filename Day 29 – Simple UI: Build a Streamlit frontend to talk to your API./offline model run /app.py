import streamlit as st
import requests

st.set_page_config(page_title="AI Chat", page_icon="🤖")
st.title("🤖 AI Chat Assistant")
st.write("FastAPI + Ollama (Offline)")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("Ask something...")

if user_input:
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.write(user_input)

    with st.spinner("Thinking..."):
        try:
            response = requests.post(
                "http://localhost:8000/chat",
                json={"message": user_input}
            )

            data = response.json()
            reply = data.get("response", "No response")

            st.session_state.messages.append(
                {"role": "assistant", "content": reply}
            )

            with st.chat_message("assistant"):
                st.write(reply)

        except Exception as e:
            st.error(f"Error: {e}")
