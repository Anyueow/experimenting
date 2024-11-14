# grok_client.py

import streamlit as st
from anthropic import Anthropic

def get_grok_client():
    # Retrieve the API key from Streamlit's secrets management
    XAI_API_KEY = "xai-WKzfiKaQIqb0GCnADNPfi2lvFWQwr5JYmMvExlbkWSUY3eLBxwsjXWdcWXFwebhEZzLbIxJ5U9iPD2HO"
    if not XAI_API_KEY:
        raise ValueError("XAI_API_KEY is not set in secrets.")
    client = Anthropic(
        api_key=XAI_API_KEY,
        base_url="https://api.x.ai",
    )
    return client
