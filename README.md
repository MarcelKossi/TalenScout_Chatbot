TALENTSCOUT HIRING ASSISTANT CHATBOT
=====================================================================
This project implements an AI-assisted technical screening chatbot designed to guide candidates through an initial recruitment interview. The chatbot collects essential profile information, validates it, extracts the candidate’s tech stack, and generates technical questions tailored to their skills.
The goal is to automate the first evaluation phase while keeping the interaction structured, consistent, and professional.

=====================================================================
1. Project Overview
The chatbot performs the following core tasks:
Greets the user and begins a structured information-collection process
Collects seven mandatory fields in order:
- Full name
- Email
- Phone number
- Years of experience
- Desired position(s)
- Location
- Tech stack
Validates user inputs with deterministic logic
Normalizes the tech stack (deduplicated and ready for question generation)
Generates technical questions using OpenAI (default model: gpt-4o-mini) based on the candidate’s skills
Prompts the candidate for final notes
Ends the interview gracefully
The flow is intentionally deterministic to avoid hallucinations, maintain control, and ensure reliability.
=====================================================================
2. Project Structure
TalenScout_Chatbot/
│
├── app.py                          # Main Streamlit application
│
├── prompts/
│   ├── system_prompt.txt           # Base assistant behavior rules
│   ├── informations.txt            # Information collection specification
│   ├── questions.txt               # Technical question generation rules based on the candidate profile
│
├── utils/
│   ├── __init__.py
│   ├── validators.py               # Input validation functions
│   ├── tech_stack_class.py         # Tech stack normalization and categorization
│   ├── state_manager.py            # Finite-state conversation controller
│   ├── resume_parser.py            # (Future) Extract fields from uploaded CV
│   ├── scoring_engine.py           # (Future) Candidate scoring & difficulty levels
│   ├── sentiment.py                # (Future) Tone analysis for adaptive responses
│
├── models/
│   ├── __init__.py
│   ├── llm_interface.py            # Wrapper for GPT-4/llm calls
│
├── data/
│   ├── __init__.py
│   ├── candidate_structure.json     # Fixed structure of candidate profile
│
├── static/
│   ├── style.css                   # css injection for Streamlit app
│
├── README.md
├── requirements.txt
└── .gitignore

=====================================================================
3. Features Implemented
Deterministic Information Flow
The chatbot collects candidate information one step at a time using a finite-state machine.
This eliminates ambiguity and ensures the conversation stays on track.

Input Validation
Custom validators ensure correct formatting for:
- name
- email
- phone number
- years of experience
- positions
- location
- tech stack
This guarantees clean and reliable data before any processing.

Tech Stack Categorization
Technologies listed by the candidate are cleaned, normalized, deduplicated, and assigned to categories such as:
- languages
- frameworks
- databases
- tools
- cloud providers

GPT-4 / llm Question Generation
Once all data is collected, the chatbot uses GPT-4/llm to generate a structured set of technical questions based on the candidate’s skills.

Final Confirmation Step
After question generation, the candidate is asked whether they want to add anything else.
This allows additional notes or clarifications before the session ends.

=====================================================================
4. Installation
A-Clone the repository
git clone <your-repo-url>
cd TalenScout_Chatbot

B- Install dependencies
pip install -r requirements.txt

C-Create a .env file
OPENAI_API_KEY=sk-your_openai_key_here

D- Run the application
streamlit run app.py

=====================================================================
5. How It Works (Step-by-Step)
a- When the app loads, a new conversation state is initialized.
b- The chatbot asks the user for their full name.
c- The user response is validated and stored.
d- The chatbot moves to the next field.
e- Once all required fields are collected, the tech stack is processed.
f- OpenAI generates customized technical questions (default: gpt-4o-mini).
g- The chatbot asks if the candidate wants to add anything.
h- The session ends gracefully.
This flow ensures consistency across users and reduces LLM unpredictability.

=====================================================================
6. Future Improvements (Already Prepared in the Structure)
The project includes placeholders for enhancements that can be added later without changing the core architecture of the chatbot:
    a- Resume Upload & Parsing (resume_parser.py)
        . Candidate Scoring & Difficulty Levels (scoring_engine.py)
        . Tone Analysis for Adaptive Responses (sentiment.py)
        . Planned features:
            - Accept PDF or TXT CV uploads
            - Extract name, email, skills, and experience
            - Autofill missing candidate fields

    b- Candidate Scoring & Difficulty Adjustment (scoring_engine.py)
    Future scoring will consider:
        . experience alignment
        . tech stack breadth
        . consistency of answers

This will allow dynamic question difficulty (beginner / intermediate / advanced).

c- Sentiment Analysis (sentiment.py)
Lightweight tone detection to:
        . adapt bot responses
        . support stressed candidates
        . improve UX

=====================================================================
7. Security Notes
- API keys are loaded from environment variables
- .env is excluded via .gitignore
- No personal data is permanently stored
- All candidate information exists only in session memory
- This keeps the system safe, private, and compliant with basic data-handling expectations.

=====================================================================
8. License
This project is submitted as part of a technical assessment for intership recruitment at PG-AGI company.
Use is restricted to evaluation and educational purposes. 
For any other use, please contact me for permission. If else, all rights reserved.