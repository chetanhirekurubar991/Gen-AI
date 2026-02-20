import streamlit as st
import requests
# response=requests.post(
#     "http://localhost:8000",
#     json={
#         "message":"Hello",
#         "model":"3:4b"
#     }
# )
# data=response.json()
st.title("AI Chat Assistant..!")
st.write("Connected to FasrAPI Backend")
if 'messages' not in st.session_state:
    st.session_state.messages=[]
st.session_state.messages.append({"role":"user","content":"Hello"})
for msg in st.session_state.messages:
    st.write(msg["content"])
user_input=st.text_input("Ask me anything")
if user_input:
    st.write(f"You Asked {user_input}")

