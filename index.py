# meant for Python 3, will not work with Python 2
import requests # pip install requests
import streamlit as st
from streamlit_chat import message

api_key = "VF.DM.644d8602c20a470007df07d8.1vclXovmNPCOqCoG" # it should look like this: VF.DM.XXXXXXX.XXXXXX... keep this a secret!

# Storing the chat
if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

attrs = ['resume', 'job_desc', 'uploaded', 'is_running', 'key']
values = [None, None, False, True, 0]

for attr, value in zip(attrs, values):
    if attr not in st.session_state:
        st.session_state[attr] = value

# user_id defines who is having the conversation, e.g. steve, john.doe@gmail.com, username_464
def interact(user_id, request):
    response = requests.post(
        f'https://general-runtime.voiceflow.com/state/user/{user_id}/interact',
        json={ 'request': request },
        headers={ 'Authorization': api_key },
    )
    res = []
    for trace in response.json():
        if trace['type'] == 'speak' or trace['type'] == 'text':
            resp = trace['payload']['message']
            res.append(resp)
        elif trace['type'] == 'end':
            # an end trace means the the voiceflow dialog has ended
            return None, False
    return ' '.join(res), True

# We will get the user's input by calling the get_text function
def get_text(message: str, key: str = str(st.session_state.key)):
    input_text = st.text_input("You: ", message, key=key)
    if input_text == message:
        input_text = ""
    st.session_state.key += 1
    return input_text

if not st.session_state.job_desc:
    st.session_state.job_desc = get_text("Please paste the job description", "job_desc")
    if st.session_state.job_desc:
        output = interact("user", {'type': 'text', 'payload': st.session_state.job_desc})
        st.session_state.past.append(st.session_state.job_desc)
        st.session_state.generated.append(output)
        message(output)
        st.session_state.uploaded = True

        if not st.session_state.resume:
            st.session_state.resume = get_text("Please paste your resume", "resume")
        
        if st.session_state.resume:
            if st.session_state.generated and st.session_state.is_running:
                user_input = get_text("")
                if user_input:
                    output, st.session_state.is_running = interact("user", {'type': 'text', 'payload': user_input})
                    st.session_state.past.append(user_input)
                    st.session_state.generated.append(output)
                    
                    gen_len = len(st.session_state.generated)
                    past_len = len(st.session_state.past)
                    first = min(gen_len, past_len)
                    for i in range(first):
                        message(st.session_state.generated[i], key=str(i) + str(st.session_state.key) + "_message")
                        message(st.session_state.past[i], is_user=True, key=str(i) + str(st.session_state.key) + "_user")
                    for i in range(first, gen_len):
                        message(st.session_state.generated[i], key=str(i) + str(st.session_state.key) + "_message")
                    for i in range(first, past_len):
                        message(st.session_state.past[i], key=str(i) + str(st.session_state.key) + "_user")

