import os
from anthropic import Anthropic

print("debug")
# Set your xAI API key
XAI_API_KEY ='xai-WKzfiKaQIqb0GCnADNPfi2lvFWQwr5JYmMvExlbkWSUY3eLBxwsjXWdcWXFwebhEZzLbIxJ5U9iPD2HO'
if not XAI_API_KEY:
    raise ValueError("Please set the XAI_API_KEY environment variable.")

# Initialize the Anthropic client with xAI's base URL
client = Anthropic(
    api_key=XAI_API_KEY,
    base_url="https://api.x.ai",
)

# Define the conversation
messages = [
    {
        "role": "user",
        "content": "make this funnier & sassier:For those not participating in BeerioKart or spectating (boo…..jk), and for those who will "
                   "claim an early loss and be kicked out of the bracket faster than they entered (aka me), "
                   "here are some casual happy hour spots for todayyy: ",

    },
]

# Create a chat completion
message = client.messages.create(
    model="grok-beta",
    max_tokens=128,
    system="You are Grok,a voice of the people's heinous tweets.",
    messages=messages,
)

# Print the assistant's response
print(message.content)
