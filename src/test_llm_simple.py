from openai import OpenAI
import streamlit as st
import os
from dotenv import load_dotenv


# take environment variables from .env.
load_dotenv()
# ----------------------------
# ------- App Settings -------
# ----------------------------
MODUS_IS_DEVELOPMENT = False


def add_divider():
    st.write('')
    st.divider()
    st.write('')


with st.sidebar:
    st.header('Input Settings', divider='violet')  # rainbow
    # ------------------------
    # ------- Settings -------
    # ------------------------
    openai_api_key = st.text_input("OpenAI API Key", key="chat_bot_api_key", type="password")
    if MODUS_IS_DEVELOPMENT:
        openai_api_key = os.environ.get("OPENAI_API_KEY")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    with st.expander("Further Input Settings:"):
        model_selected = st.selectbox(
            'Models available',
            ('gpt-3.5-turbo', 'tbd', 'tbd'))
        st.write('Model selected: ', model_selected)
        add_divider()
        model_selected = st.selectbox(
            'Other Setting',
            ('aaa', 'bbb', 'ccc'))
        add_divider()
        temperature = st.slider('Temperature (not yet live)', 0.0, 1.0, 0.0, 0.1)
        st.write("Temperature: ", temperature)
        st.write('')
    # Overwriting Section
    prompt_addition = st.text_input('Prompt Addition', 'and btw, what is 1 + 3?')
    prompt_addition = ' ' + prompt_addition


# --------------------------------
# ------- Initial Messages -------
# --------------------------------
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "assistant", "content": "How can I help you?"},
    ]
    # "temperature": 0.7
    # st.session_state["temperature"] = temperature


# -------------------------
# ------- Main Page -------
# -------------------------
st.title("💬 Daniel's Little Helper")
st.caption("🚀")

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    # -------------------------------------------------------
    # ------- Waiting here - Waiting for API-Response -------
    # -------------------------------------------------------
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    client = OpenAI(api_key=openai_api_key)
    st.session_state.messages.append({"role": "user", "content": prompt + prompt_addition})
    st.chat_message("user").write(prompt)
    # -------------------------------------------------------
    # ------- Waiting here - Waiting for API-Response -------
    # -------------------------------------------------------
    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    msg = response.choices[0].message.content
    # save & write API-response into the session-state
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)


with st.sidebar:
    # --------------------------------
    # ------- Message Overview -------
    # --------------------------------
    st.header('Message Overview', divider='violet')

    with st.expander("Latest [-1] saved MESSAGE - in SessionState:'"):
        st.write(st.session_state["messages"][-1])

    with st.expander("Current SessionState - ALL MESSAGES"):
        st.write('The following goes into the API call as message:')
        st.write(st.session_state["messages"])
        st.write('The above, plus the input-PROMPT, goes into the API-call. Looks like:')
        prompt_form = {"role": "user", "content": "<<prompt>>"}
        st.write(prompt_form)
    # ----------------------------
    # ------- API Response -------
    # ----------------------------
    try:
        # response
        str_length_choices = len(response.choices)
        str_completion_tokens = response.usage.completion_tokens
        str_prompt_tokens = response.usage.prompt_tokens
        str_total_tokens = response.usage.total_tokens
    except NameError:
        # if not response_exists:
        str_length_choices = '-'
        str_completion_tokens = '-'
        str_prompt_tokens = '-'
        str_total_tokens = '-'

    st.write('')
    st.header('Tokens of the last API-Call:', divider='violet')
    st.write('completion_tokens: ', str_completion_tokens)
    st.write('prompt_tokens: ', str_prompt_tokens)
    st.write('total_tokens: ', str_total_tokens)
    st.write('')
    st.header('Quality Checks / Expectations:', divider='violet')
    st.write('Length of Response Choices (expected to be 1): ', str_length_choices)
