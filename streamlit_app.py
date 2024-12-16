import streamlit as st
from gemini_ai import GeminiAI  # Replace OpenAI with Gemini API package (install via pip if required).

# Show title and description.
st.title("📚 The Writer's Lens Chatbot")
st.write(
    "Welcome to 'The Writer's Lens,' a chatbot that mimics the writing styles of famous authors. "
    "Choose an author, provide a topic, and enjoy creatively styled responses! "
    "Learn more about literary styles or test your skills with our guessing game!"
)

# Retrieve the Gemini API key from `secrets.toml`.
# api_key = st.secrets["GEMINI_API_KEY"]
api_key = "AIzaSyASnkyIRB2Abu4qUY8yfI8K_2sYLqhh5io"

# Ensure the API key exists.
if not api_key:
    st.error("API key not found. Please add it to `secrets.toml`.", icon="🚫")
else:
    # Create a Gemini client.
    client = GeminiAI(api_key=api_key)

    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "selected_author" not in st.session_state:
        st.session_state.selected_author = ""

    if "learning_mode" not in st.session_state:
        st.session_state.learning_mode = False

    # Sidebar for user options.
    with st.sidebar:
        st.header("Choose an Author Style")
        author = st.selectbox(
            "Select a writing style:",
            [
                "Edgar Allan Poe (Gothic, mysterious)",
                "Jane Austen (Romantic, witty, Regency-era)",
                "George Orwell (Analytical, dystopian)",
                "Custom Writer"
            ]
        )
        st.session_state.selected_author = author

        # Learning Mode Toggle
        st.session_state.learning_mode = st.checkbox("Learning Mode", value=False)

        if st.session_state.learning_mode:
            st.write("### Author Style Details")
            if "Edgar Allan Poe" in author:
                st.write(
                    "Poe's style often includes a dark atmosphere, gothic themes, and elaborate descriptions."
                )
            elif "Jane Austen" in author:
                st.write(
                    "Austen's works feature wit, romantic tension, and detailed depictions of social manners in Regency-era England."
                )
            elif "George Orwell" in author:
                st.write(
                    "Orwell is known for his clear, concise prose and themes of societal critique, particularly regarding dystopian futures."
                )
            elif "Custom Writer" in author:
                st.write(
                    "You can provide your own description of a writing style for the chatbot to mimic!"
                )

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    if prompt := st.chat_input("Enter a topic or sentence:"):

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Prompt engineering to integrate author style.
        author_description = {
            "Edgar Allan Poe": "Gothic and mysterious prose with vivid imagery.",
            "Jane Austen": "Witty and romantic style reflecting Regency-era social settings.",
            "George Orwell": "Analytical and concise prose with dystopian undertones.",
            "Custom Writer": "Custom style specified by the user."
        }

        style_context = author_description.get(
            st.session_state.selected_author.split(" (")[0], ""
        )

        system_message = (
            f"You are a writer crafting in the style of {st.session_state.selected_author.split(' (')[0]}. "
            f"Keep the response aligned with this description: {style_context}"
        )

        # Generate a response using the Gemini API.
        stream = client.chat.completions.create(
            model="gemini-model",  # Use the appropriate model for Gemini.
            messages=[
                {"role": "system", "content": system_message}
            ] + [
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
