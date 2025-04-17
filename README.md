# 🧠 Medical Diagnosis ChatBot
A conversational AI chatbot built with Streamlit and Google Gemini-Pro that provides medical information, analyzes uploaded medical reports (PDF), and intelligently filters medical queries to deliver relevant health insights.

⚠️ Disclaimer: This chatbot is intended for educational and informational purposes only. It is not a replacement for professional medical advice, diagnosis, or treatment.

# 💡 Features
🔍 Medical Query Analysis
Understands and responds to a wide range of medical-related queries.

Uses a built-in keyword detection system to ensure queries are medically relevant before providing AI-generated responses.

Filters out non-medical questions to maintain focused, high-quality assistance.

🤖 Gemini-Pro Integration
Powered by Google's Gemini-Pro (gemini-pro) large language model.

Capable of advanced, contextual medical conversations.

Preserves chat history during the session for a seamless experience.

📄 PDF Medical Report Processing
Users can upload PDF medical reports (like prescriptions, diagnoses, or lab results).

The app uses PyMuPDF (fitz) to extract and read the full text content of the medical report.

Users can then ask follow-up questions specifically about the uploaded report.

💬 Streamlit Chat Interface
Clean, user-friendly chat layout using st.chat_message.

Two dedicated chat inputs:

General medical queries

Questions about uploaded medical reports

🚀 Getting Started
Prerequisites

Ensure you have the following Python libraries installed:

bash
 Copy
 Edit
pip install streamlit google-generativeai pymupdf requests
Run the App
bash
Copy
Edit
streamlit run app.py
🔑 API Configuration
This app requires a Google API Key for Gemini-Pro. You can set this by replacing the following line in your code:

python
Copy
Edit
GOOGLE_API_KEY = "YOUR_API_KEY_HERE"
Or use an environment variable for security:

python
Copy
Edit
import os
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
#🧠 How It Works
1. Query Filtering:
Uses a predefined list of common medical terms and optionally processes terms from the UMLS Metathesaurus.

Only responds to queries where at least 30% of the words are medically relevant.

2. AI Chat Response:
Gemini-Pro handles query responses.

Chat history is preserved within a session (st.session_state.chat_session).

3. PDF Upload + Q&A:
Users upload a medical report.

Text is extracted using PyMuPDF.

Users can then ask questions about the uploaded content for tailored answers.

# 📁 Project Structure
bash
Copy
Edit
├── app.py                  # Main Streamlit app
├── README.md               # Project documentation
├── requirements.txt        # Python dependencies (optional)
✅ Example Use Cases
Understanding symptoms like headache, fatigue, or irregular heartbeats.

Uploading a blood test report and asking, “Is my hemoglobin level normal?”

Asking about treatments for hypertension or thyroid disorders.

Understanding medical terminology in a report.

🔐 Security Note
API keys are sensitive. Do not share them publicly.

Consider storing them using .env files and python-dotenv.

🙋‍♀️ Future Enhancements
🔐 Authentication system

🌐 Multilingual medical query support

📊 Visual summary of lab results

🧬 Genomic data-based drug recommendations

# 👩‍⚕️ Built With
Streamlit

Google Generative AI

PyMuPDF

UMLS Metathesaurus (NIH)

📬 Contact
Author: Dia Mehak
Email: diamehak96@gmail.com
GitHub: @diamehak

