# gui.py
import streamlit as st
import requests

st.set_page_config(page_title="vLLM Playground")
st.title("vLLM Playground")

# 1. Inputs
prompt = st.text_area("Prompt", value="Hello, world!")
max_tokens   = st.slider("Max tokens",   1, 2048, 50)
temperature  = st.slider("Temperature", 0.0,   1.0, 0.7)

# 2. Trigger generation
if st.button("Generate"):
    if not prompt.strip():
        st.error("Please enter a non-empty prompt.")
    else:
        with st.spinner("Generating…"):
            payload = {
                "prompt": prompt,
                "max_tokens": max_tokens,
                "temperature": temperature
            }
            try:
                r = requests.post("http://localhost:8000/generate",
                                  json=payload, timeout=30)
                r.raise_for_status()
                data = r.json()
            except Exception as e:
                st.error(f"Request failed: {e}")
            else:
                st.subheader("Output")
                # vLLM returns data["outputs"] as a list of strings
                for i, out in enumerate(data.get("outputs", [])):
                    st.code(out, language="text")
                st.sidebar.subheader("Usage")
                st.sidebar.json(data.get("usage", {}))
