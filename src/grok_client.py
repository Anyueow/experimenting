# grok_client.py

import os
from anthropic import Anthropic

def get_grok_client():
    XAI_API_KEY = os.getenv("XAI_API_KEY")
    if not XAI_API_KEY:
        raise ValueError("Please set the XAI_API_KEY environment variable.")
    client = Anthropic(
        api_key=XAI_API_KEY,
        base_url="https://api.x.ai",
    )
    return client
