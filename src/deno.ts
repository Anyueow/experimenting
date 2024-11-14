import { python } from "https://deno.land/x/python/mod.ts";

// Import necessary Python modules
const os = python.import("os");
const requests = python.import("requests");


// Define the Python function to interact with the xAI API
const code = `
import os
import requests

def get_grok_response(api_key):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "grok-beta",
        "messages": [
            {"role": "user", "content": "What is the meaning of life, the universe, and everything?"}
        ],
        "max_tokens": 128,
        "system": "You are Grok, a chatbot inspired by the Hitchhiker's Guide to the Galaxy.",
    }
    response = requests.post("https://api.x.ai/v1/messages", headers=headers, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.status_code, "message": response.text}
`;

// Execute the Python code
python.run(code);

// Access the defined Python function
const get_grok_response = python.globals.get("get_grok_response");

const XAI_API_KEY = Deno.env.get("XAI_API_KEY");
if (!XAI_API_KEY) {
  throw new Error("Please set the XAI_API_KEY environment variable.");
}

const response = get_grok_response(XAI_API_KEY);

if ("error" in response) {
  console.error(`Error: ${response.error} - ${response.message}`);
} else {
  console.log(response);
}
