import streamlit as st

try:
    api_key = st.secrets["XAI_API_KEY"]
    st.write("API Key retrieved successfully.")
except KeyError:
    st.write("XAI_API_KEY not found in secrets.")
