import streamlit as st
import google.generativeai as genai

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

# Retrieve the Gemini API key from `secrets.toml`.
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
            "Custom Writer",
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
            "John Steinbeck (Clear prose about human dignity and social issues)",
            "Agatha Christie (Mysteries with tightly-plotted twists)",
            "Franz Kafka (Existential, absurd narratives about alienation)",
            "Emily Dickinson (Concise, contemplative poetry about life and death)",
            "E.M. Forster (Explorations of social and personal conflicts)",
            "Arthur Conan Doyle (Victorian detective stories with detailed settings)",
            "Willa Cather (Lyrical descriptions of the American Midwest)",
            "Khaled Hosseini (Narratives on family, tragedy, and cultural displacement)",
            "Chinua Achebe (Clear, impactful prose addressing colonialism)",
            "C.S. Lewis (Philosophical allegory blending Christian themes)",
            "Philip K. Dick (Speculative fiction questioning reality and identity)",
            "Alice Walker (Poetic, emotional narratives about race and identity)",
            "Zora Neale Hurston (Folk stories with African American themes)",
            "Jean-Paul Sartre (Existential prose focusing on individual freedom)",
            "Louise Erdrich (Family sagas with Native American culture)",
            "David Foster Wallace (Verbose, humorous explorations of modern alienation)",
            "Chimamanda Ngozi Adichie (Engaging narratives with Nigerian culture and feminism)",
            "William Faulkner (Southern Gothic, focusing on race and history)",
            "Mario Vargas Llosa (Prose blending politics, identity, and Latin American society)"
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
    "Custom Writer": "Custom style specified by the user.",
    "William Shakespeare": "Poetic, dramatic language with rich metaphors and iambic pentameter.",
    "Mark Twain": "Humorous, colloquial prose with social commentary on human nature.",
    "Hemingway": "Sparse, direct prose often focusing on themes of masculinity and human struggle.",
    "F. Scott Fitzgerald": "Elegant, lyrical prose capturing the glamour and disillusionment of the Jazz Age.",
    "Charles Dickens": "Detailed descriptions with a focus on social critique and memorable characters.",
    "Leo Tolstoy": "Philosophical and moral, with a deep focus on family, morality, and Russian society.",
    "Virginia Woolf": "Stream-of-consciousness narrative with a focus on inner emotional experiences.",
    "Ernest Hemingway": "Short, direct prose with deep underlying themes of heroism and despair.",
    "James Joyce": "Complex, experimental language with a focus on consciousness and interior monologue.",
    "J.K. Rowling": "Richly detailed narratives filled with magic, imagination, and moral choices.",
    "Haruki Murakami": "Surreal and philosophical with a blend of the ordinary and the supernatural.",
    "Kurt Vonnegut": "Darkly humorous, satirical, often anti-war in theme with a fragmented narrative style.",
    "J.R.R. Tolkien": "Epic fantasy with detailed world-building and high-stakes adventure.",
    "George R.R. Martin": "Richly detailed, morally complex character-driven narratives within political intrigue.",
    "Sylvia Plath": "Introspective, poetic prose, often exploring themes of mental health, death, and identity.",
    "Margaret Atwood": "Complex, speculative fiction with themes of societal control, feminism, and dystopia.",
    "Toni Morrison": "Lyrical, rich prose exploring African American experiences and societal issues.",
    "Ray Bradbury": "Imaginative, often speculative prose with a focus on individualism and censorship.",
    "Harper Lee": "Direct, poignant prose exploring themes of morality, justice, and racial issues.",
    "Gabriel García Márquez": "Magical realism with vibrant prose and exploration of Latin American history.",
    "Oscar Wilde": "Witty, satirical, and often ironic, with a focus on beauty and social critique.",
    "Dostoevsky": "Philosophical and psychological, exploring deep existential themes, guilt, and redemption.",
    "John Steinbeck": "Clear, direct prose focused on social issues and the dignity of the human spirit.",
    "Agatha Christie": "Mysterious and methodical, with tightly-plotted narratives filled with twists and suspense.",
    "Franz Kafka": "Existential and surreal prose often centered around alienation and absurdity.",
    "Emily Dickinson": "Concise, contemplative poetry with an introspective look at life, death, and nature.",
    "E.M. Forster": "Sensitive explorations of social and personal conflicts, with a focus on character development.",
    "Arthur Conan Doyle": "Masterful detective stories often set against detailed Victorian backdrops.",
    "Willa Cather": "Simple, rural prose capturing the beauty of the American Midwest with lyrical imagery.",
    "Khaled Hosseini": "Rich narratives blending familial bonds, tragedy, and cultural displacement.",
    "Chinua Achebe": "Sparse, clear prose addressing the cultural and social consequences of colonialism.",
    "C.S. Lewis": "Philosophical yet accessible, blending Christian allegory with moral teachings in a fictional context.",
    "Philip K. Dick": "Speculative fiction questioning reality, identity, and individualism within a dystopian future.",
    "Alice Walker": "Vibrant, deeply emotional prose often focusing on African American women’s experiences.",
    "Ralph Waldo Emerson": "Philosophical essays blending natural observation with spiritual introspection.",
    "Jack London": "Adventure-filled prose with an emphasis on survival, nature, and the human spirit.",
    "Maya Angelou": "Poetic, deeply personal narratives that explore race, identity, and resilience.",
    "Zora Neale Hurston": "Rich dialect and folklore, with themes of identity and the African American experience.",
    "Jean-Paul Sartre": "Existential prose, focusing on individual freedom, anxiety, and the absurdity of existence.",
    "Louise Erdrich": "Complex family sagas rooted in Native American culture, with themes of identity and history.",
    "David Foster Wallace": "Dense, verbose, and often humorous prose with an exploration of postmodern alienation.",
    "Chimamanda Ngozi Adichie": "Crisp, engaging narratives blending Nigerian culture with a modern, feminist viewpoint.",
    "William Faulkner": "Complex, multi-layered prose reflecting the Southern Gothic style, often focusing on race and history.",
    "Mario Vargas Llosa": "Rich prose with a focus on politics, identity, and the complexities of Latin American society."
}


        style_context = author_description.get(
        st.session_state.selected_author.split(" (")[0], ""
    )


        system_message = (
            f"You are a writer crafting in the style of {st.session_state.selected_author.split(' (')[0]}. "
            f"Keep the response aligned with this description: {style_context}"
        )

        # Generate a response using the Gemini API.
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