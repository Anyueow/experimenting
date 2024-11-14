import streamlit as st
from anthropic import Anthropic



def get_grok_client():
    try:
        api_key = st.secrets["XAI_API_KEY"]
        st.write("API Key retrieved successfully.")
    except KeyError:
        st.write("XAI_API_KEY not found in secrets.")

    if not api_key:
        raise ValueError("XAI_API_KEY is not set in secrets.")

    client = Anthropic(
        api_key=api_key,
        base_url="https://api.x.ai",
    )

    return client
