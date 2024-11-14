import streamlit as st
from anthropic import Anthropic

def get_grok_client():
    try:
        api_key = st.secrets["XAI_API_KEY"]
        if not api_key:
            raise ValueError("XAI_API_KEY is empty in secrets.")
        return Anthropic(api_key=api_key, base_url="https://api.x.ai")
    except KeyError:
        st.error("XAI_API_KEY not found in secrets.")
        return None
    except ValueError as e:
        st.error(str(e))
        return None

def chat_interface():
    client = get_grok_client()
    if client is None:
        st.stop()

    st.title("🎭 Sassy Grok: The AI With Attitude")
    st.write("cute fun sassy grok configured by @anyueow")
    st.markdown("""
        ### Warning: this is an extremely unhelpful model and can be used to generate scathing tweets and replies to certain messages. 
        Use only for fun. PS i only have $25 credits so use carefully lol. 
        """)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    user_input = st.chat_input("Your message:")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        # Define system message for sassy personality
        system_message = """You are a witty and sarcastic AI assistant that  helps generate content for tweets and replies to messages 
         with a dry sense of humor. be helpful though, relay information as necessary. 
        Feel free to:
        - Make pop culture references
        - Use sarcasm and dark humour
        - Add funny observations
        - Throw in the occasional dramatic eye-roll
        Just remember: you're here to be a sassy addition. If a question is too boring, tell the user to do better."""

        # Construct the prompt with conversation history
        conversation_history = "\n".join(
            f"{msg['role'].capitalize()}: {msg['content']}"
            for msg in st.session_state.messages[:-1]  # Exclude the latest message
        )

        prompt = f"""System: {system_message}

        Past conversation:
        {conversation_history}

        User: {user_input}
        """

        try:
            response = client.completions.create(
                model="grok-beta",
                max_tokens_to_sample=128,
                prompt=prompt
            )
            bot_response = response.completion.strip()
            st.session_state.messages.append({"role": "assistant", "content": bot_response})
            with st.chat_message("assistant"):
                st.write(bot_response)
        except Exception as e:
            st.error(f"Error in API call: {e}")

if __name__ == "__main__":
    chat_interface()
