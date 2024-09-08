import streamlit as st
import torch
from peft import LoraConfig, get_peft_model
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
)

# TODO: figure out how to use a custom model on cpu

st.set_page_config(page_title="Finance LLM Chatbot", page_icon="💸")
lora_config = LoraConfig.from_pretrained("./results/model")
access_token = st.secrets["ACCESS_TOKEN"]
model_name = "mistralai/Mistral-7B-V0.3"
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    quantization_config=bnb_config,
    device_map="auto",
    trust_remote_code=True,
    token=access_token,
)
model = get_peft_model(model, lora_config)
tokenizer = AutoTokenizer.from_pretrained(model_name, token=access_token)
tokenizer.pad_token = tokenizer.eos_token

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
