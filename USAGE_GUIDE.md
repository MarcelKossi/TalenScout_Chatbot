# TalenScout Chatbot - Usage Guide

## Overview

The TalenScout Chatbot is an AI-powered recruitment assistant that conducts structured candidate screening interviews. It collects comprehensive information from candidates in a conversational manner and saves their profiles for review by the hiring team.

## Features

### 1. Structured Screening Process

The chatbot guides candidates through 13 essential questions covering:
- Personal contact information
- Professional experience
- Skills and qualifications
- Education background
- Availability and expectations
- Work authorization

### 2. Conversational Interface

- Natural language interactions powered by OpenAI GPT
- Friendly and professional tone
- Smooth transitions between questions
- Acknowledgment of candidate responses

### 3. Progress Tracking

- Visual progress bar in sidebar
- Question counter (e.g., "5 / 13 questions completed")
- Clear indication when screening is complete

### 4. Data Management

- Automatic saving of candidate profiles
- JSON format for easy integration
- Timestamped filenames
- Structured data validation with Pydantic

## Getting Started

### Prerequisites

1. Python 3.8 or higher
2. OpenAI API key (get one at https://platform.openai.com/)

### Installation Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/MarcelKossi/TalenScout_Chatbot.git
   cd TalenScout_Chatbot
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment:**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=sk-your-actual-api-key-here
   COMPANY_NAME=TalenScout
   ```

4. **Run the application:**
   ```bash
   streamlit run app.py
   ```

5. **Access the chatbot:**
   Open your browser to `http://localhost:8501`

## Using the Chatbot

### For Candidates

1. **Start the conversation:**
   - Open the application URL
   - Read the welcome message
   - Begin answering questions as they appear

2. **Answering questions:**
   - Type your answer in the chat input box
   - Press Enter or click Send
   - The chatbot will acknowledge your answer and ask the next question

3. **Progress tracking:**
   - Check the sidebar to see your progress
   - The progress bar shows how many questions remain

4. **Completion:**
   - After the final question, you'll see a summary of your information
   - Your profile is automatically saved
   - You'll receive confirmation that the hiring team will review your application

### For Recruiters

1. **Accessing candidate data:**
   - Candidate profiles are saved in `candidate_data/` directory
   - Each file is named: `[Name]_[Timestamp].json`
   - Example: `John_Doe_20240116_143022.json`

2. **Reviewing profiles:**
   - Open JSON files with any text editor
   - All information is structured and easy to read
   - Use the data for further screening or interviews

## Screening Questions

The chatbot asks candidates about:

1. **Full Name** - Basic identification
2. **Email Address** - Primary contact method
3. **Phone Number** - Secondary contact method
4. **Position Applied** - Role they're interested in
5. **Years of Experience** - Professional experience level
6. **Current Role** - Most recent job title
7. **Skills** - Technical and professional competencies
8. **Education** - Highest degree and field of study
9. **Location** - Current location and relocation preferences
10. **Work Authorization** - Legal authorization to work
11. **Availability** - When they can start
12. **Notice Period** - Current notice period (if applicable)
13. **Salary Expectations** - Expected compensation range

## Customization

### Modifying Questions

Edit the `QUESTIONS` list in `app.py`:

```python
QUESTIONS = [
    {
        "id": "unique_id",
        "question": "Your question text here?",
        "field": "profile_field_name",
        "required": True
    },
    # Add more questions...
]
```

### Changing Company Name

Update the `COMPANY_NAME` in your `.env` file:
```
COMPANY_NAME=YourCompanyName
```

### Adjusting LLM Behavior

Modify the `get_llm_response()` function in `app.py`:
- Change the `model` parameter (e.g., "gpt-4" for better responses)
- Adjust `temperature` (0.0-2.0, higher = more creative)
- Modify the system prompt for different tone/style

### Styling the UI

Customize the Streamlit interface:
```python
st.set_page_config(
    page_title="Your Title",
    page_icon="🎯",
    layout="wide"
)
```

## Data Format

Candidate profiles are saved in JSON format:

```json
{
  "name": "Jane Smith",
  "email": "jane.smith@example.com",
  "phone": "+1-555-123-4567",
  "position_applied": "Software Engineer",
  "years_of_experience": 5,
  "current_role": "Senior Developer",
  "skills": ["Python", "JavaScript", "React"],
  "education": "Bachelor's in Computer Science",
  "availability": "2 weeks",
  "expected_salary": "$100,000 - $120,000",
  "location": "New York, NY",
  "work_authorization": "Yes",
  "notice_period": "2 weeks"
}
```

## Troubleshooting

### Common Issues

**Issue: "OpenAI API error"**
- Check that your API key is correct in `.env`
- Verify you have API credits available
- Ensure your API key has proper permissions

**Issue: "Module not found"**
- Run `pip install -r requirements.txt` again
- Check that you're using Python 3.8 or higher

**Issue: "Port already in use"**
- Stop other Streamlit applications
- Or run on a different port: `streamlit run app.py --server.port 8502`

**Issue: "Candidate data not saving"**
- Check file permissions in the application directory
- Ensure the application has write access
- The `candidate_data/` directory is created automatically

## Best Practices

### For Deployment

1. **Security:**
   - Never commit `.env` file with real API keys
   - Use environment variables in production
   - Implement rate limiting for API calls
   - Add authentication for access control

2. **Data Privacy:**
   - Comply with GDPR, CCPA, and other data protection regulations
   - Implement data encryption for sensitive information
   - Have a clear privacy policy
   - Provide candidates with data deletion options

3. **Scalability:**
   - Consider using a database instead of JSON files
   - Implement caching for frequently accessed data
   - Use a production-grade web server
   - Monitor API usage and costs

4. **User Experience:**
   - Test thoroughly with real candidates
   - Gather feedback and iterate
   - Ensure mobile responsiveness
   - Provide clear instructions

## Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Review existing issues and discussions
- Submit pull requests for improvements

## License

This project is available for use under standard open-source practices.
