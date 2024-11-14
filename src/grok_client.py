# grok_client.py

import streamlit as st
from anthropic import Anthropic

def get_grok_client():
    # Retrieve the API key from Streamlit's secrets management
    XAI_API_KEY = st.secrets['XAI_API_KEY']
    if not XAI_API_KEY:
        raise ValueError("XAI_API_KEY is not set in secrets.")
    client = Anthropic(
        api_key=XAI_API_KEY,
        base_url="https://api.x.ai",
    )
    return client
