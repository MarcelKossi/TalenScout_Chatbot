# TalenScout_Chatbot

An LLM-powered recruitment chatbot designed for structured candidate screening and information gathering.

## 🎯 Features

- **Structured Screening Process**: Guides candidates through a comprehensive set of screening questions
- **LLM-Powered Conversations**: Uses OpenAI's GPT to provide natural, conversational interactions
- **Information Gathering**: Collects essential candidate information including:
  - Contact details (name, email, phone)
  - Professional background (experience, current role, skills)
  - Education and qualifications
  - Availability and expectations
  - Work authorization status
- **Data Persistence**: Saves candidate profiles in structured JSON format
- **Progress Tracking**: Visual progress indicator for candidates
- **Professional Summary**: Generates comprehensive screening summaries

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- OpenAI API key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/MarcelKossi/TalenScout_Chatbot.git
cd TalenScout_Chatbot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=your_actual_api_key_here
COMPANY_NAME=TalenScout
```

### Running the Application

Start the Streamlit application:
```bash
streamlit run app.py
```

The chatbot will be available at `http://localhost:8501`

## 📖 Usage

1. Open the application in your web browser
2. Answer the screening questions as they are presented
3. The chatbot will guide you through the entire process
4. Progress is shown in the sidebar
5. Upon completion, your information is saved and a summary is displayed

## 📁 Project Structure

```
TalenScout_Chatbot/
├── app.py                 # Main application file
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore rules
├── README.md             # This file
└── candidate_data/       # Directory for storing candidate profiles (created automatically)
```

## 🔧 Configuration

You can customize the chatbot by modifying the following in `app.py`:

- **Screening Questions**: Edit the `QUESTIONS` list in the `ScreeningQuestion` class
- **Company Name**: Set in `.env` file
- **LLM Model**: Change the model parameter in `get_llm_response()` function
- **Response Style**: Adjust the system prompt in `get_llm_response()` function

## 💾 Data Storage

Candidate data is automatically saved to the `candidate_data/` directory in JSON format. Each file is named with the candidate's name and timestamp:
```
candidate_data/John_Doe_20240116_143022.json
```

## 🔒 Security Considerations

- Never commit your `.env` file with actual API keys
- Store candidate data securely and comply with data protection regulations
- Review and implement appropriate access controls for production use
- Consider encryption for sensitive candidate information

## 🛠️ Tech Stack

- **Streamlit**: Web application framework
- **OpenAI API**: LLM for conversational interactions
- **Pydantic**: Data validation and settings management
- **Python-dotenv**: Environment variable management

## 📝 License

This project is available for use under standard open-source practices.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## 📧 Contact

For questions or support, please open an issue on GitHub.