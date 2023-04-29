import requests

# View our quick start guide to get your API key:
# https://www.voiceflow.com/api/dialog-manager#section/Quick-Start
api_key = "VF.DM.644d8602c20a470007df07d8.1vclXovmNPCOqCoG"

user_id = "user_123"  # Unique ID used to track conversation state
user_input = "Hello world!"  # User's message to your Voiceflow assistant

body = {"action": {"type": "text", "payload": "Hello world!"}}

# Start a conversation
response = requests.post(
    f"https://general-runtime.voiceflow.com/state/user/{user_id}/interact",
    json=body,
    headers={"Authorization": api_key},
)

# Log the response
print(response.json())