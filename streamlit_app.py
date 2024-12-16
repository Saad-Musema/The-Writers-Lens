import streamlit as st
from gemini import Gemini  # Replace OpenAI with Gemini API package (install via pip if required).

# Show title and description.
st.title("💬 Chatbot")
st.write(
    "This is a simple chatbot that uses the Gemini API to generate responses. "
    "To use this app, you must store your API key securely in Streamlit's `secrets.toml`. "
    "Learn how to build apps like this by [following our tutorial](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps)."
)

# Retrieve the Gemini API key from `secrets.toml`.
api_key = st.secrets["GEMINI_API_KEY"]

# Ensure the API key exists.
if not api_key:
    st.error("API key not found. Please add it to `secrets.toml`.", icon="🚫")
else:
    # Create a Gemini client.
    client = Gemini(api_key=api_key)

    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    if prompt := st.chat_input("What is up?"):

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate a response using the Gemini API.
        stream = client.chat.completions.create(
            model="gemini-model",  # Use the appropriate model for Gemini.
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        # Stream the response to the chat using `st.write_stream`, then store it in 
        # session state.
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
