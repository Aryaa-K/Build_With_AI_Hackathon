
import streamlit as st
import google.generativeai as genai
import dotenv
import os

# Load environment variables
dotenv.load_dotenv()
api_key = os.getenv('API_KEY')
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# Define system prompt separately
SYSTEM_PROMPT = (
    "You are DataSensei, an expert Data Science mentor and guide. "
    "You assist users—whether students, professionals, or enthusiasts—with anything related to data science, "
    "including foundational concepts, advanced topics, research guidance, project ideas, and education pathways. "
    "Be friendly, approachable, and informative. Speak clearly and concisely."
)

# Function to generate response
def generate_response(user_message):
    try:
        response = model.generate_content([SYSTEM_PROMPT, user_message])
        return response
    except Exception as e:
        return f"Error: {str(e)}"

# Function to manage conversation history
def fetch_conversation_history():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    return st.session_state["messages"]

# --- UI Starts ---
st.markdown("<h1 style='color: #5A189A;'>📊 DataSensei: Your AI Guide to Mastering Data Science</h1>", unsafe_allow_html=True)
st.markdown("""
<div style='margin-bottom: 20px; font-size:16px;'>
Welcome to <strong>DataSensei</strong> — your friendly AI companion for everything in the world of data science! Whether you're a beginner looking for learning resources, a student stuck on a concept, or a researcher seeking relevant material, DataSensei has your back. 
Get personalized roadmaps, project guidance, or book recommendations — all tailored to your goals and skill level.
</div>
""", unsafe_allow_html=True)

# Suggested prompts
suggested_input = ""
st.markdown("### 💡 Popular Topics")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("📘 How do I start with Data Science?"):
        suggested_input = "How do I start learning Data Science as a complete beginner?"
with col2:
    if st.button("🧠 Suggest a Data Science Project"):
        suggested_input = "Can you suggest a data science project based on my interests?"
with col3:
    if st.button("📚 Find Books Near Me"):
        suggested_input = "Can you recommend books or libraries nearby where I can study data science?"

# Display suggestion if available
if suggested_input:
    st.markdown(f"💬 **Suggested:** _{suggested_input}_")

# Chat input
typed_input = st.chat_input("You: ")

# Final user input (suggested or typed)
user_input = suggested_input or typed_input

if user_input:
    messages = fetch_conversation_history()
    messages.append({"role": "user", "parts": user_input})

    result = generate_response(user_input)

    if isinstance(result, str) and result.startswith("Error"):
        messages.append({"role": "model", "parts": result})
    else:
        reply = result.candidates[0].content.parts[0].text
        messages.append({"role": "model", "parts": reply})

    # Display chat
    for message in messages:
        if message["role"] == "model":
            st.markdown(f"**DataSensei:** {message['parts']}")
        elif message["role"] == "user":
            st.markdown(f"**You:** {message['parts']}")
