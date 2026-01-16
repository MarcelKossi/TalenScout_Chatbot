# TalenScout Chatbot - Architecture & Flow

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    TalenScout Chatbot                       │
│                                                             │
│  ┌─────────────┐      ┌──────────────┐      ┌───────────┐ │
│  │  Streamlit  │ ───> │  Chatbot     │ ───> │  OpenAI   │ │
│  │     UI      │ <─── │   Logic      │ <─── │    API    │ │
│  └─────────────┘      └──────────────┘      └───────────┘ │
│         │                     │                            │
│         │                     │                            │
│         v                     v                            │
│  ┌─────────────┐      ┌──────────────┐                    │
│  │  Progress   │      │   Pydantic   │                    │
│  │   Tracker   │      │  Validation  │                    │
│  └─────────────┘      └──────────────┘                    │
│                              │                             │
│                              v                             │
│                       ┌──────────────┐                     │
│                       │     JSON     │                     │
│                       │   Storage    │                     │
│                       └──────────────┘                     │
└─────────────────────────────────────────────────────────────┘
```

## Conversation Flow

```
┌──────────────────────┐
│   Candidate Opens    │
│     Application      │
└──────────┬───────────┘
           │
           v
┌──────────────────────┐
│  Welcome Message &   │
│   First Question     │
└──────────┬───────────┘
           │
           v
    ┌──────────────┐
    │   Question   │<─────────┐
    │   Loop       │          │
    └──────┬───────┘          │
           │                  │
           v                  │
    ┌──────────────┐          │
    │  Candidate   │          │
    │   Answers    │          │
    └──────┬───────┘          │
           │                  │
           v                  │
    ┌──────────────┐          │
    │   Process &  │          │
    │   Validate   │          │
    └──────┬───────┘          │
           │                  │
           v                  │
    ┌──────────────┐          │
    │  LLM Ack &   │          │
    │ Next Question│──────────┘
    └──────┬───────┘
           │
    ┌──────┴────────┐
    │  More         │
    │  Questions?   │
    │  Yes → Loop   │
    │  No ↓         │
    └───────────────┘
           │
           v
    ┌──────────────┐
    │  Generate    │
    │   Summary    │
    └──────┬───────┘
           │
           v
    ┌──────────────┐
    │  Save to     │
    │    JSON      │
    └──────┬───────┘
           │
           v
    ┌──────────────┐
    │   Display    │
    │  Summary &   │
    │   Complete   │
    └──────────────┘
```

## Data Flow

```
User Input
    │
    v
┌────────────────┐
│ Streamlit Chat │
│     Input      │
└───────┬────────┘
        │
        v
┌────────────────┐
│   Process      │
│   Answer       │
│  - Skills→List │
│  - Years→Int   │
└───────┬────────┘
        │
        v
┌────────────────┐
│   Update       │
│ CandidateProfile│
│   (Pydantic)   │
└───────┬────────┘
        │
        v
┌────────────────┐
│  Get LLM       │
│  Response      │
│  (OpenAI API)  │
└───────┬────────┘
        │
        v
┌────────────────┐
│ Next Question  │
│   or Summary   │
└───────┬────────┘
        │
        v
┌────────────────┐
│  Save to JSON  │
│ (if complete)  │
└────────────────┘
```

## Key Components

### 1. CandidateProfile (Pydantic Model)
- Validates data types
- Ensures required fields
- Provides serialization

### 2. ScreeningQuestion Class
- Defines question flow
- Maps to profile fields
- Marks required questions

### 3. Session State Management
- Tracks current question
- Stores conversation history
- Maintains candidate profile

### 4. LLM Integration
- Natural acknowledgments
- Conversational transitions
- Professional tone

### 5. Data Persistence
- JSON file format
- Timestamped filenames
- Structured storage

## Technology Stack

```
┌──────────────────────────────────────┐
│         Frontend Layer               │
│  - Streamlit (UI Framework)          │
│  - HTML/CSS (via Streamlit)          │
└──────────────────────────────────────┘
                 │
                 v
┌──────────────────────────────────────┐
│        Application Layer             │
│  - Python 3.8+                       │
│  - Session State Management          │
│  - Conversation Flow Logic           │
└──────────────────────────────────────┘
                 │
                 v
┌──────────────────────────────────────┐
│         Data Layer                   │
│  - Pydantic (Validation)             │
│  - JSON (Storage)                    │
│  - File System                       │
└──────────────────────────────────────┘
                 │
                 v
┌──────────────────────────────────────┐
│       External Services              │
│  - OpenAI GPT-3.5-turbo             │
│  - Python-dotenv (Config)            │
└──────────────────────────────────────┘
```

## Screening Questions Workflow

```
Question ID         Field Name             Processing
───────────────────────────────────────────────────────
greeting       →    name                →  Direct
contact_email  →    email               →  Direct
contact_phone  →    phone               →  Direct
position       →    position_applied    →  Direct
experience_years →  years_of_experience →  Extract numeric
current_role   →    current_role        →  Direct
skills         →    skills              →  Parse comma-separated
education      →    education           →  Direct
location       →    location            →  Direct
work_auth      →    work_authorization  →  Direct
availability   →    availability        →  Direct
notice_period  →    notice_period       →  Direct (optional)
salary         →    expected_salary     →  Direct
```

## Error Handling

```
Try Block
    │
    ├─> LLM API Call
    │       │
    │       ├─> Success → Return response
    │       └─> Error → Return friendly message
    │
    ├─> Numeric Parsing (years of experience)
    │       │
    │       ├─> Valid number → Set value
    │       └─> Invalid → Default to 0
    │
    └─> Data Serialization
            │
            ├─> Success → Save to file
            └─> Error → Log and notify
```

## Session State Variables

```python
session_state = {
    "messages": [],                    # Chat history
    "candidate_profile": CandidateProfile(),  # Current profile
    "current_question_index": 0,       # Progress tracker
    "screening_complete": False        # Completion flag
}
```

## Future Enhancements

- Multi-language support
- Custom question sets per role
- Integration with ATS systems
- Analytics dashboard
- Email notifications
- Calendar integration
- Video interview scheduling
- Resume parsing integration
- Skills assessment integration
