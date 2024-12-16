import streamlit as st
import google.generativeai as genai

author_descriptions = {
    "Edgar Allan Poe": "Poe's style often includes a dark atmosphere, gothic themes, and elaborate descriptions.",
    "Jane Austen": "Austen's works feature wit, romantic tension, and detailed depictions of social manners in Regency-era England.",
    "George Orwell": "Orwell is known for his clear, concise prose and themes of societal critique, particularly regarding dystopian futures.",
    "Custom Writer": "You can provide your own description of a writing style for the chatbot to mimic!",
    "Mark Twain": "Twain’s writing is characterized by humor, colloquial speech, and sharp social commentary, often focusing on issues of race and class.",
    "Shakespeare": "Shakespeare’s writing is rich in poetry, character depth, and exploration of complex human emotions, often using iambic pentameter.",
    "Hemingway": "Hemingway is known for his concise and understated prose, focusing on themes of existentialism, human struggle, and the beauty of simplicity.",
    "F. Scott Fitzgerald": "Fitzgerald’s style is lush and descriptive, exploring themes of decadence, the American Dream, and disillusionment, with a particular emphasis on the Jazz Age.",
    "Leo Tolstoy": "Tolstoy’s writing often features detailed psychological portraits of characters and extensive social and philosophical commentary on Russian society.",
    "Franz Kafka": "Kafka's writing is marked by themes of alienation, bureaucracy, and the absurdity of existence, often set in nightmarish, surreal environments.",
    "Dostoevsky": "Dostoevsky is known for exploring complex psychological states, morality, and themes of existential suffering and redemption, often set in tense, dramatic narratives."
}


temperature_options = {
    "Very Creative": 1.0,
    "Creative": 0.7,
    "Balanced": 0.5,
    "Realistic": 0.3,
    "More Realistic": 0.2
}

max_length_options = {
    "Very Short": 50,   # Shortest response
    "Short": 100,       # A bit more concise
    "Balanced": 150,    # Balanced length
    "Long": 200,        # Longer response
    "Very Long": 300    # Maximal response
}

# Show title and description.
st.title("📚 The Writer's Lens Chatbot")
st.write(
    "Welcome to 'The Writer's Lens,' a chatbot that mimics the writing styles of famous authors. "
    "Choose an author, provide a topic, and enjoy creatively styled responses! "
)

api_key = "AIzaSyASnkyIRB2Abu4qUY8yfI8K_2sYLqhh5io"

# Ensure the API key exists.
if not api_key:
    st.error("API key not found. Please add it to `secrets.toml`.", icon="🚫")
else:
    # Configure Gemini AI client.
    genai.configure(api_key=api_key)

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
        # Temperature selection
        temperature_label = st.selectbox(
            "Choose creativity of the response:",
            list(temperature_options.keys())
        )
        temperature = temperature_options[temperature_label]

        # Max length selection
        max_length_label = st.selectbox(
            "Choose response length:",
            list(max_length_options.keys())
        )
        max_length = max_length_options[max_length_label]

        # Show selected settings
        st.write(f"**Selected Temperature:** {temperature_label} ({temperature})")
        st.write(f"**Selected Max Length:** {max_length_label} ({max_length} tokens)")
        
        st.header("Choose an Author Style")
        author = st.selectbox(
            "Select a writing style:",
           [
            "Edgar Allan Poe (Gothic, mysterious)",
            "Jane Austen (Romantic, witty, Regency-era)",
            "George Orwell (Analytical, dystopian)",
            "William Shakespeare (Poetic, dramatic with iambic pentameter)",
            "Mark Twain (Humorous, colloquial, social commentary)",
            "Hemingway (Sparse, direct prose focusing on masculinity and human struggle)",
            "F. Scott Fitzgerald (Elegant, lyrical prose capturing the Jazz Age)",
            "Charles Dickens (Social critique with memorable characters)",
            "Leo Tolstoy (Philosophical, focusing on family and Russian society)",
            "Virginia Woolf (Stream-of-consciousness, emotional focus)",
            "Ernest Hemingway (Short, direct prose with deep themes)",
            "James Joyce (Complex, experimental, focusing on consciousness)",
            "J.K. Rowling (Richly detailed, with magic and moral choices)",
            "Haruki Murakami (Surreal, blending the ordinary and supernatural)",
            "Kurt Vonnegut (Dark humor, satirical, anti-war themes)",
            "J.R.R. Tolkien (Epic fantasy with world-building and adventure)",
            "George R.R. Martin (Morally complex narratives with political intrigue)",
            "Sylvia Plath (Introspective, poetic, exploring mental health and identity)",
            "Margaret Atwood (Complex, speculative fiction exploring societal control)",
            "Toni Morrison (Lyrical prose focused on African American experiences)",
            "Ray Bradbury (Speculative, focusing on individualism and censorship)",
            "Harper Lee (Poignant, exploring morality, justice, and race)",
            "Gabriel García Márquez (Magical realism with vivid prose)",
            "Oscar Wilde (Witty, satirical with social critique)",
            "Dostoevsky (Philosophical, focusing on existential themes)",
        ]
        )
        st.session_state.selected_author = author

        # Learning Mode Toggle
        st.session_state.learning_mode = st.checkbox("Learning Mode", value=False)

        if st.session_state.learning_mode:
            st.write("### Author Style Details")
            # Look up the description for the selected author
            style_context = author_descriptions.get(
            st.session_state.selected_author.split(" (")[0], ""
            
            # Display the corresponding description
            st.write(style_context)

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

        style_context = author_descriptions.get(
        st.session_state.selected_author.split(" (")[0], ""
    )


        system_message = (
            f"You are a writer crafting in the style of {st.session_state.selected_author.split(' (')[0]}. "
            f"Keep the response aligned with this description: {style_context}"
        )

        # Generate a response
        model = genai.GenerativeModel("gemini-1.5-flash")
        # response = model.generate_content(
        #     f"{system_message}\n\nUser: {prompt}"
        # )
        
        response = model.generate_content(
        f"{system_message}\n\nUser: {prompt}",
        generation_config = genai.types.GenerationConfig(
            temperature = temperature,
            max_output_tokens = max_length
        )
)


        # Display the assistant's response.
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})