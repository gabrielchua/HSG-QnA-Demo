import streamlit as st
import requests
import time

API_URL = st.secrets["API_URL"]
API_KEY = st.secrets["API_KEY"]
HEADERS = {
  "Content-Type": "application/json",
  "Authorization": f"Bearer {API_KEY}"
}

def query(payload: dict):
  response = requests.post(url=API_URL, headers=HEADERS, json=payload)
  return response.json()
  
#####################################
st.title("Demo Q&A Bot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if question := st.chat_input("Ask something"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": question})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(question)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        result = query({
            "flow_id": "Flow_Sample_Q_A_Bot_YTI3MWU0ZTctNjk0",
            "inputs": [{
                "question": question + " If the answer to my question is not in the context, just return 'Sorry, I do not have the answer to your question.'"
            }]
        })

        assistant_response = result['data'][0]['llm_response']["content"]

        # Simulate stream of response with milliseconds delay
        for chunk in assistant_response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
