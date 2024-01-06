from openai import OpenAI
import streamlit as st


def add_divider():
    st.write('')
    st.divider()
    st.write('')


if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]


with st.sidebar:
    st.header('Input Settings', divider='rainbow')
    # ------------------------
    # ------- Settings -------
    # ------------------------
    openai_api_key = st.text_input("OpenAI API Key", key="chat_bot_api_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    with st.expander("Further Input Settings:"):
        model_selected = st.selectbox(
            'Models available',
            ('gpt-3.5-turbo', 'tbd', 'tbd'))
        st.write('Model selected:', model_selected)
        add_divider()
        model_selected = st.selectbox(
            'Other Setting',
            ('aaa', 'bbb', 'ccc'))
        st.write('')

# -------------------------
# ------- Main Page -------
# -------------------------
st.title("💬 Daniel's Little Helper")
st.caption("🚀")

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    client = OpenAI(api_key=openai_api_key)
    st.session_state.messages.append({"role": "user", "content": prompt})
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
    st.header('Message Overview', divider='rainbow')
    st.write('Latest [-1] saved MESSAGE - in SessionState:')
    st.write(st.session_state["messages"][-1])
    st.write('The following goes into the API call as message:')
    with st.expander("Current SessionState - MESSAGES"):
        st.write(st.session_state["messages"])
        st.write('The above, plus the input-PROMPT, goes into the API-call. Looks like:')
        prompt_form = {"role": "user", "content": "<<prompt>>"}
        st.write(prompt_form)