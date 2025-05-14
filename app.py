import streamlit as st
import requests

# --- Page Configuration ---
st.set_page_config(
    page_title='Personalized Learning Assistant',
    page_icon="📚",
    layout="wide"
)

# --- API Setup ---
OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
PEXELS_API_KEY = st.secrets["PEXELS_API_KEY"]

MODEL_NAME = "deepseek/deepseek-chat-v3-0324:free"

# --- API Functions ---
def query_llm(user_prompt_details):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": "You are an expert AI Learning Assistant. Your goal is to provide personalized learning recommendations and concise topic explanations based on user preferences. Be encouraging and clear."},
            {"role": "user", "content": user_prompt_details}
        ]
    }
    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", json=data, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {e}")
        st.error(f"Response content: {response.text if 'response' in locals() else 'No response object'}")
        return None
    except KeyError:
        st.error("Unexpected API response format.")
        st.error(f"Response content: {response.json() if 'response' in locals() and response.content else 'No response content'}")
        return None

def fetch_topic_image(topic_query):
    headers = {"Authorization": PEXELS_API_KEY}
    params = {"query": topic_query, "per_page": 1, "orientation": "landscape"}
    try:
        response = requests.get("https://api.pexels.com/v1/search", headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data["photos"]:
            return data["photos"][0]["src"]["medium"]
        else:
            return None
    except requests.exceptions.RequestException as e:
        st.sidebar.error(f"Pexels API Error: {e}")
        return None
    except (KeyError, IndexError):
        st.sidebar.error("Error parsing Pexels API response or no photos found.")
        return None

# --- Session State Initialization ---
if "history" not in st.session_state:
    st.session_state.history = []
if "current_topic_image" not in st.session_state:
    st.session_state.current_topic_image = None
if "current_topic_image_attempted" not in st.session_state: # Added for better image handling
    st.session_state.current_topic_image_attempted = False


# --- UI Layout ---
with st.sidebar:
    st.image("test1.png", width=400)
    st.title("⚙Your Preferences")
    st.markdown("Customize your learning journey!")

    style_options = ["Visual (diagrams, videos)", "Auditory (podcasts, lectures)", "Kinesthetic (hands-on, interactive)", "Reading/Writing", "Mixed"]
    difficulty_options = ["Beginner", "Intermediate", "Advanced"]

    style = st.selectbox(
        "Preferred learning style:",
        style_options,
        key="learning_style_selector"
    )
    difficulty = st.selectbox(
        "Your current understanding level:",
        difficulty_options,
        key="difficulty_level_selector"
    )
    num_recommendations = st.slider(
        "Number of recommendations:",
        min_value=1, max_value=5, value=3,
        key="num_recs_slider"
    )
    topic = st.text_input(
        "What topic are you trying to learn?",
        placeholder="e.g., Quantum Physics, Linear Algebra",
        key="topic_input_field"
    )

    if st.button("🚀 Get Personalized Recommendation", type="primary", use_container_width=True):
        st.session_state.current_topic_image_attempted = False
        if not topic:
            st.warning("Please enter a topic to learn.")
        else:
            with st.spinner('Finding an inspiring image for your topic...'):
                image_url = fetch_topic_image(topic)
                st.session_state.current_topic_image = image_url
                st.session_state.current_topic_image_attempted = True
            prompt_details = f"""
            The user wants to learn about: "{topic}".
            Their preferred learning style is: '{style}'.
            Their current understanding level is: '{difficulty}'.

            Please provide:
            1. A brief and simple explanation of '{topic}', tailored for a '{difficulty}' level.
            2. Suggest {num_recommendations} diverse educational resources (e.g., articles, videos, interactive simulations, courses, books) for this topic.
               - Prioritize resources that align with the '{style}' learning style.
               - Ensure the suggested resources are suitable for a '{difficulty}' learner.
               - For each resource, provide a very brief description of why it's suitable.
            Keep the tone encouraging and helpful.
            """
            with st.spinner(f'🧠 Generating personalized content for "{topic}"...'):
                result = query_llm(prompt_details)
                if result:

                    new_entry = {
                        "topic": topic,
                        "style": style,
                        "difficulty": difficulty,
                        "result": result,
                        "image_url": image_url,
                        "num_recommendations": num_recommendations # Storing for completeness
                    }
                    st.session_state.history.insert(0, new_entry)
                    st.success("✨ Your personalized content is ready!")
                    st.rerun()


    st.markdown("---")

# Main Area for Content Display
st.title("📚 Personalized Learning Assistant")
st.markdown("Welcome! Get customized learning content powered by AI. Set your preferences in the sidebar and enter a topic to begin.")
st.markdown("---")

# Display Latest Recommendation (if any, from the button click)
if st.session_state.history: # Check if history is not empty
    latest_entry = st.session_state.history[0]
    if latest_entry.get("topic") == st.session_state.get("topic_input_field") and \
       latest_entry.get("style") == st.session_state.get("learning_style_selector") and \
       latest_entry.get("difficulty") == st.session_state.get("difficulty_level_selector"):
        # This condition means the top history item matches the current inputs, implying it was just generated
        st.subheader(f"Your Plan for: {latest_entry.get('topic', 'N/A')}")
        active_topic_for_image = st.session_state.get("topic_input_field", "your topic")
        if st.session_state.current_topic_image:
            st.markdown(
                f"""
                <div style='text-align: center;'>
                    <img src="{st.session_state.current_topic_image}" alt="Visual for {active_topic_for_image}" style="width: 80%; max-width: 600px; border-radius: 10px;" />
                    <p style="font-weight: bold;">Visual for {active_topic_for_image}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        elif st.session_state.current_topic_image_attempted and active_topic_for_image:  # Check if an attempt was made for a valid topic
            st.info(f"No specific image found for '{active_topic_for_image}'.")

        st.markdown(f"*Learning Style: {latest_entry.get('style', 'N/A')} | Difficulty: {latest_entry.get('difficulty', 'N/A')}*")
        with st.container(border=True):
            st.markdown(latest_entry.get('result', 'No result available.'))
        st.markdown("---")


# Learning History Section
st.subheader("📜 Your Learning History")
if st.session_state.history:
    if st.button("🗑️ Clear All History"):
        st.session_state.history = []
        st.session_state.current_topic_image = None
        st.session_state.current_topic_image_attempted = False
        st.rerun()

    for i, entry in enumerate(st.session_state.history):
        # Use .get() with default values to prevent KeyError
        topic_display = entry.get('topic', 'Unknown Topic')
        style_display = entry.get('style', 'N/A')
        difficulty_display = entry.get('difficulty', 'N/A')
        image_url_display = entry.get('image_url') # Will be None if not present

        expander_title = f"{i+1}. {topic_display} (Style: {style_display}, Difficulty: {difficulty_display})"
        with st.expander(expander_title):
            if image_url_display:
                st.image(image_url_display, width=300)
            st.markdown(entry.get('result', 'No content available for this entry.'))
else:
    st.info("Your learning journey will be recorded here. Start by selecting a topic and getting a recommendation!")


# Footer
st.markdown("---")
st.caption(
    "🛠️ Developed by **Vignesh S** | Powered by Streamlit & OpenRouter AI\n\n"
    '<a href="https://www.linkedin.com/in/vignesh-s-9b86a7243" target="_blank">Connect on LinkedIn</a>',
    unsafe_allow_html=True
)





# import streamlit as st
# import requests
# from click import prompt
#
# st.set_page_config(page_title='Personalized Learning Assistant')
#
# # API Setup
# OPENROUTER_API_KEY = "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"  # 🔒 Replace with your key
# MODEL_NAME = "deepseek/deepseek-chat-v3-0324:free"
#
# # Chatbot Functionality
# def query_operator(user_prompt):
#     headers = {
#         "Authorization": f"Bearer {OPENROUTER_API_KEY}",
#         "Content-Type": "application/json",
#     }
#
#     data = {
#         "model": MODEL_NAME,
#         "messages": [
#             {"role": "system", "content": "You are a helpful educational assistant. Recommend learning content based on user input."},
#             {"role": "user", "content": user_prompt}
#         ]
#     }
#
#     response = requests.post("https://openrouter.ai/api/v1/chat/completions", json=data, headers=headers)
#
#     if response.status_code == 200:
#         return response.json()["choices"][0]["message"]["content"]
#     else:
#         st.error("API Error: " + response.text)
#         return None
#
# # Session state to store the chat
# if "history" not in st.session_state:
#     st.session_state.history = []
#
# # Streamlit UI
# st.title("Personalized Learning Assistant")
# st.markdown("Get customized learning content powered by Deepseek AI")
#
# st.subheader("Your Preferences")
# style = st.selectbox("Your preferred learning style:", ["Visual", "Auditory", "Kinesthetic", "Mixed"])
# topic = st.text_input("What topic are you trying to learn? (e.g., Pysics, Quantum Computing, Linear Algebra)")
#
# if st.button("Get Personalized Recommendation"):
#     if not topic:
#         st.warning("Please enter a topic.")
#     else:
#         prompt = f"""
#         The user prefers '{style}' learning style.
#         Suggest 2-3 education resources (text, video or activity-based) for the topic: {topic}.
#         Also explain the topic briefly in simple terms.
# """
#         with st.spinner('Generating personalized content...'):
#             result = query_operator(prompt)
#             if result:
#                 st.success("📚 Here's your personalized content:")
#                 st.markdown(result)
#                 st.session_state.history.append({"topic": topic, "result":result})
#
# # History
# st.subheader("Your learning history")
#
# if st.session_state.history:
#     for i, entry in enumerate(reversed(st.session_state.history)):
#         with st.expander(f"{entry['topic']}"):
#             st.markdown(entry['result'])
# else:
#     st.info("No content viewed yet. Start by selecting a topic!")
#
# st.markdown("---")
# st.caption(
#     "🛠️ Developed by **Vignesh S**\n"
#     '<a href="https://www.linkedin.com/in/vignesh-s-9b86a7243" target="_blank">Connect on LinkedIn</a>',
#     unsafe_allow_html=True
# )
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
