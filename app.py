import streamlit as st
import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
)


st.set_page_config(page_title="Finance LLM Chatbot", page_icon="💸")

with st.spinner("Downloading the models (might take a while)..."):
    model = AutoModelForCausalLM.from_pretrained("./results/model")
    tokenizer = AutoTokenizer.from_pretrained("./results/model")
    model.to("cpu")

st.title("Finance LLM Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if question := st.chat_input("What to do with my money?"):
    st.chat_message("user").markdown(question)
    st.session_state.messages.append({"role": "user", "content": question})

    text = f"Question: {question}"
    device = "cuda" if torch.cuda.is_available() else "cpu"
    inputs = tokenizer(text, return_tensors="pt").to(device)
    outputs = model.generate(**inputs, max_new_tokens=512)
    with st.spinner("Thinking..."):
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
