import streamlit as st
from dotenv import load_dotenv
import os
import random
import html

from utils.state_manager import ConversationState
from utils.validators import Validators
from utils.tech_stack_class import TechStackClassifier
from models.llm_interface import LLMInterface

# Proper absolute path for .env loading
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

def load_prompt(relative_path):
    abs_path = os.path.join(BASE_DIR, relative_path)
    with open(abs_path, "r", encoding="utf-8") as f:
        return f.read()

try:
    SYSTEM_PROMPT = load_prompt("prompts/system_prompt.txt")
    QUESTIONS_PROMPT = load_prompt("prompts/questions.txt")
except FileNotFoundError:
    st.error("❌ Missing prompt files. Ensure prompts/ directory contains system_prompt.txt and questions.txt")
    st.stop()

#  LOAD CUSTOM CSS

def load_css():
    css_file = os.path.join(BASE_DIR, "static/style.css")
    if os.path.exists(css_file):
        with open(css_file, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.set_page_config(page_title="TalentScout AI Hiring Assistant", layout="centered")
load_css()
st.title("TalentScout Hiring Assistant Chatbot")


#  SESSION INITIALIZATION
if "state" not in st.session_state:
    st.session_state.state = ConversationState()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "llm" not in st.session_state:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or not isinstance(api_key, str) or not api_key.strip() or not api_key.strip().startswith("sk-"):
        st.error("OpenAI API key is missing or invalid. Please set OPENAI_API_KEY in your .env file.")
        st.stop()

    try:
        st.session_state.llm = LLMInterface(model_name="gpt-4o-mini")
    except Exception:
        st.error("OpenAI API key is missing or invalid. Please set OPENAI_API_KEY in your .env file.")
        st.stop()

if "questions_generated" not in st.session_state:
    st.session_state.questions_generated = False


state = st.session_state.state
history = st.session_state.chat_history
llm = st.session_state.llm


#  MESSAGE RENDERING

ACKS = ["Great!", "Perfect!", "Got it!", "Thanks!", "Awesome!", "Understood!", "Sounds good!"]

def render_chat(role, text):
    with st.chat_message(role):
        bubble = "chat-bubble-user" if role == "user" else "chat-bubble-bot"
        safe_text = html.escape(str(text))
        raw_text = str(text)
        stripped = raw_text.lstrip()
        looks_like_json = stripped.startswith("{") or stripped.startswith("[")
        if role == "assistant" and looks_like_json and "\n" in raw_text:
            st.markdown(
                f"<div class='{bubble}'><pre style='margin:0; white-space:pre-wrap; word-break:break-word;'>{safe_text}</pre></div>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(f"<div class='{bubble}'>{safe_text}</div>", unsafe_allow_html=True)

def bot_say(text):
    history.append(("assistant", text))
    render_chat("assistant", text)

def user_say(text):
    history.append(("user", text))
    render_chat("user", text)


#  DISPLAY PRIOR CHAT HISTORY

for role, message in history:
    render_chat(role, message)

#  INITIAL GREETING

if not history:
    bot_say("Hello! I’m TalentScout. I’ll ask you a few quick questions to better understand your profile. Let’s begin : what’s your full name?")


#  HANDLE USER INPUT
user_input = st.chat_input("Type your message Here...")

if user_input:

    user_say(user_input)

    # Global exit
    if state.detect_exit_intent(user_input):
        bot_say("Thank you. Your information has been recorded. Have a great day!")
        st.stop()

    # FINAL CONFIRMATION PHASE
    if state.needs_final_confirmation():
        lower = user_input.lower().strip()
        if lower in ["no", "none", "nothing", "nah", "nope"]:
            bot_say("Thank you for your time. We will contact you shortly.")
            state.is_complete = True
            st.stop()
        else:
            state.store_response("additional_notes", user_input)
            bot_say("Thanks for the additional details. We will contact you shortly.")
            st.stop()

    # VALIDATION PHASE
    field = state.current_field
    is_valid = False
    cleaned = None

    if field == "name":
        is_valid, cleaned = Validators.validate_name(user_input)
    elif field == "email":
        is_valid, cleaned = Validators.validate_email(user_input)
    elif field == "phone":
        is_valid, cleaned = Validators.validate_phone(user_input)
    elif field == "experience_years":
        is_valid, cleaned = Validators.validate_experience(user_input)
    elif field == "desired_positions":
        is_valid, cleaned = Validators.validate_positions(user_input)
    elif field == "location":
        is_valid, cleaned = Validators.validate_location(user_input)
    elif field == "tech_stack":
        is_valid, cleaned = Validators.validate_tech_stack(user_input)
    else:
        is_valid, cleaned = True, user_input

    if not is_valid:
        bot_say(cleaned)
        st.stop()

    # Store the validated response
    state.store_response(field, cleaned)

    # GENERATE TECHNICAL QUESTIONS
    if state.ready_for_questions() and not state.final_confirmation_stage and not st.session_state.questions_generated:

        bot_say("Perfect. I have all the information I need. Wait a while, I'm generating some technical questions for you! Please stay Patient...")

        try:
            # Convert list into readable string
            tech_list = state.collected_data["tech_stack"]
            tech_str = ", ".join(tech_list)
            
            # Build full prompt
            user_prompt = f"Candidate technologies: {tech_str}\n\n{QUESTIONS_PROMPT}"

            with st.spinner("Analyzing your profile…"):
                questions = llm.generate_response(SYSTEM_PROMPT, user_prompt)

            bot_say("Here are some technical questions based on your background, please answer them carefully:")
            bot_say(questions)

            st.session_state.questions_generated = True

            # Mark final confirmation phase
            state.final_confirmation_stage = True
            bot_say(state.get_current_question())

        except Exception:
            bot_say("I’m having trouble generating questions right now. You may add any final details you feel are important.")
            state.final_confirmation_stage = True
            bot_say(state.get_current_question())

        st.stop()

    # ASK NEXT QUESTION
    next_question = state.get_current_question()

    if len(history) > 2:
        bot_say(f"{random.choice(ACKS)} {next_question}")
    else:
        bot_say(next_question)
