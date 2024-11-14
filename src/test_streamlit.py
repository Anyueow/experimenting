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


def chat_interface():
    client = get_grok_client()

    st.title("Grok AI Chatbot")
    st.write("Ask Grok anything!")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        st.write(f"**{message['role'].capitalize()}:** {message['content']}")

    user_input = st.text_input("You:", key="user_input")
    if st.button("Send") and user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.write(f"**User:** {user_input}")

        messages = [{"role": msg["role"], "content": msg["content"]} for msg in st.session_state.messages]

        try:
            response = client.messages.create(
                model="grok-beta",
                max_tokens=128,
                system="You are Grok, a chatbot inspired by the Hitchhiker's Guide to the Galaxy.",
                messages=messages,
            )
            bot_response = response.content.strip()
            st.session_state.messages.append({"role": "assistant", "content": bot_response})
            st.write(f"**Grok:** {bot_response}")
        except Exception as e:
            st.error(f"Error: {e}")

if __name__ == "__main__":
    chat_interface()
