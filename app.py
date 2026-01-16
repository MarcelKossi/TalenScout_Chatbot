"""
TalenScout Chatbot - LLM-powered recruitment chatbot for candidate screening
"""

import streamlit as st
import openai
import json
import os
import re
from datetime import datetime
from typing import Dict, List, Optional
from dotenv import load_dotenv
from pydantic import BaseModel, Field

# Load environment variables
load_dotenv()

# Configure OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")
COMPANY_NAME = os.getenv("COMPANY_NAME", "TalenScout")


class CandidateProfile(BaseModel):
    """Structured candidate information"""
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    position_applied: Optional[str] = None
    years_of_experience: Optional[int] = None
    current_role: Optional[str] = None
    skills: List[str] = Field(default_factory=list)
    education: Optional[str] = None
    availability: Optional[str] = None
    expected_salary: Optional[str] = None
    location: Optional[str] = None
    work_authorization: Optional[str] = None
    notice_period: Optional[str] = None


class ScreeningQuestion:
    """Represents a structured screening question"""
    
    QUESTIONS = [
        {
            "id": "greeting",
            "question": f"Hello! I'm the {COMPANY_NAME} recruitment assistant. I'll be helping you through the initial screening process. May I have your full name?",
            "field": "name",
            "required": True
        },
        {
            "id": "contact_email",
            "question": "Thank you! Could you please provide your email address?",
            "field": "email",
            "required": True
        },
        {
            "id": "contact_phone",
            "question": "Great! And your phone number?",
            "field": "phone",
            "required": True
        },
        {
            "id": "position",
            "question": "Which position are you applying for?",
            "field": "position_applied",
            "required": True
        },
        {
            "id": "experience_years",
            "question": "How many years of professional experience do you have in this field?",
            "field": "years_of_experience",
            "required": True
        },
        {
            "id": "current_role",
            "question": "What is your current or most recent job title?",
            "field": "current_role",
            "required": True
        },
        {
            "id": "skills",
            "question": "Please list your key technical skills and competencies relevant to this position (separated by commas).",
            "field": "skills",
            "required": True
        },
        {
            "id": "education",
            "question": "What is your highest level of education? Please include the degree and field of study.",
            "field": "education",
            "required": True
        },
        {
            "id": "location",
            "question": "Where are you currently located? Are you open to relocation?",
            "field": "location",
            "required": True
        },
        {
            "id": "work_authorization",
            "question": "Are you legally authorized to work in the country where this position is located?",
            "field": "work_authorization",
            "required": True
        },
        {
            "id": "availability",
            "question": "When would you be available to start if offered the position?",
            "field": "availability",
            "required": True
        },
        {
            "id": "notice_period",
            "question": "What is your current notice period (if applicable)?",
            "field": "notice_period",
            "required": False
        },
        {
            "id": "salary",
            "question": "What are your salary expectations for this role?",
            "field": "expected_salary",
            "required": True
        }
    ]


def initialize_session_state():
    """Initialize Streamlit session state variables"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "candidate_profile" not in st.session_state:
        st.session_state.candidate_profile = CandidateProfile()
    if "current_question_index" not in st.session_state:
        st.session_state.current_question_index = 0
    if "screening_complete" not in st.session_state:
        st.session_state.screening_complete = False


def get_llm_response(user_message: str, context: str = "") -> str:
    """Get response from OpenAI LLM"""
    try:
        system_prompt = f"""You are a professional recruitment assistant for {COMPANY_NAME}. 
        You are conducting an initial screening interview with a candidate.
        Be professional, friendly, and encouraging. Keep responses concise and conversational.
        {context}"""
        
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=200
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"I apologize, but I'm having technical difficulties. Error: {str(e)}"


def process_answer(answer: str, question: Dict) -> None:
    """Process candidate's answer and update profile"""
    field = question["field"]
    candidate = st.session_state.candidate_profile
    
    if field == "skills":
        # Parse comma-separated skills
        skills_list = [s.strip() for s in answer.split(",") if s.strip()]
        candidate.skills = skills_list
    elif field == "years_of_experience":
        # Extract numeric value
        try:
            # Try to extract number from text
            numbers = re.findall(r'\d+', answer)
            if numbers:
                candidate.years_of_experience = int(numbers[0])
            else:
                candidate.years_of_experience = 0
        except (ValueError, TypeError):
            candidate.years_of_experience = 0
    else:
        # Set field directly
        setattr(candidate, field, answer)


def get_next_question() -> Optional[Dict]:
    """Get the next screening question"""
    if st.session_state.current_question_index < len(ScreeningQuestion.QUESTIONS):
        return ScreeningQuestion.QUESTIONS[st.session_state.current_question_index]
    return None


def save_candidate_data():
    """Save candidate profile to JSON file"""
    # Create directory if it doesn't exist
    os.makedirs("candidate_data", exist_ok=True)
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    candidate_name = st.session_state.candidate_profile.name or "unknown"
    safe_name = "".join(c for c in candidate_name if c.isalnum() or c in (' ', '_')).strip().replace(' ', '_')
    filename = f"candidate_data/{safe_name}_{timestamp}.json"
    
    # Save to file
    with open(filename, 'w') as f:
        json.dump(st.session_state.candidate_profile.model_dump(), f, indent=2)
    
    return filename


def generate_screening_summary() -> str:
    """Generate a summary of the screening"""
    profile = st.session_state.candidate_profile
    
    summary = f"""
### 📋 Candidate Screening Summary

**Personal Information:**
- **Name:** {profile.name or 'N/A'}
- **Email:** {profile.email or 'N/A'}
- **Phone:** {profile.phone or 'N/A'}
- **Location:** {profile.location or 'N/A'}

**Professional Background:**
- **Position Applied:** {profile.position_applied or 'N/A'}
- **Current Role:** {profile.current_role or 'N/A'}
- **Experience:** {profile.years_of_experience or 'N/A'} years
- **Education:** {profile.education or 'N/A'}

**Skills:**
{', '.join(profile.skills) if profile.skills else 'N/A'}

**Employment Details:**
- **Availability:** {profile.availability or 'N/A'}
- **Notice Period:** {profile.notice_period or 'N/A'}
- **Expected Salary:** {profile.expected_salary or 'N/A'}
- **Work Authorization:** {profile.work_authorization or 'N/A'}
"""
    return summary


def main():
    """Main application"""
    st.set_page_config(
        page_title=f"{COMPANY_NAME} Recruitment Chatbot",
        page_icon="💼",
        layout="wide"
    )
    
    st.title(f"💼 {COMPANY_NAME} Recruitment Chatbot")
    st.markdown("---")
    
    # Initialize session state
    initialize_session_state()
    
    # Sidebar with info
    with st.sidebar:
        st.header("ℹ️ About")
        st.write(f"""
        Welcome to the {COMPANY_NAME} recruitment chatbot!
        
        This AI-powered assistant will guide you through the initial screening process.
        
        **What to expect:**
        - Structured questions about your background
        - 10-15 minutes to complete
        - Your responses will be saved securely
        """)
        
        st.markdown("---")
        st.header("📊 Progress")
        progress = (st.session_state.current_question_index / len(ScreeningQuestion.QUESTIONS)) * 100
        st.progress(progress / 100)
        st.write(f"{st.session_state.current_question_index} / {len(ScreeningQuestion.QUESTIONS)} questions completed")
        
        if st.session_state.screening_complete:
            st.success("✅ Screening Complete!")
    
    # Main chat interface
    chat_container = st.container()
    
    with chat_container:
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Show screening complete message and summary
        if st.session_state.screening_complete:
            with st.chat_message("assistant"):
                st.markdown(f"""
                Thank you for completing the screening process! 🎉
                
                Your information has been recorded and our recruitment team will review your profile.
                We'll be in touch soon regarding the next steps.
                
                {generate_screening_summary()}
                
                You can now close this window. Good luck! 🍀
                """)
        
        # If first time, show welcome message
        if len(st.session_state.messages) == 0 and not st.session_state.screening_complete:
            question = get_next_question()
            if question:
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": question["question"]
                })
                st.rerun()
    
    # Chat input
    if not st.session_state.screening_complete:
        if prompt := st.chat_input("Type your answer here..."):
            # Add user message to chat
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Process the answer
            current_question = ScreeningQuestion.QUESTIONS[st.session_state.current_question_index]
            process_answer(prompt, current_question)
            
            # Move to next question
            st.session_state.current_question_index += 1
            
            # Check if screening is complete
            if st.session_state.current_question_index >= len(ScreeningQuestion.QUESTIONS):
                st.session_state.screening_complete = True
                # Save candidate data
                filename = save_candidate_data()
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"Data saved to {filename}"
                })
            else:
                # Get next question
                next_question = get_next_question()
                if next_question:
                    # Add some conversational acknowledgment using LLM
                    context = f"The candidate just answered: '{prompt}'. Acknowledge their answer briefly and naturally transition to the next question."
                    transition = get_llm_response(prompt, context)
                    
                    response = f"{transition}\n\n{next_question['question']}"
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response
                    })
            
            st.rerun()


if __name__ == "__main__":
    main()
