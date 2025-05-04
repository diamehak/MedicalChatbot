import streamlit as st
import google.generativeai as gen_ai
import fitz  # PyMuPDF
import requests
import re
GOOGLE_API_KEY = "YOUR_API_KEY_HERE"

# Set up Google Gemini-Pro AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')

st.set_page_config(
    page_title="Medical Diagnosis ChatBot",
    page_icon=":brain:",  # Favicon emoji
)

# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role

# Function to fetch medical terms from UMLS Metathesaurus
def fetch_medical_terms():
    umls_url = "https://download.nlm.nih.gov/umls/kss/mrconso.zip"
    response = requests.get(umls_url)
    with open("mrconso.zip", "wb") as f:
        f.write(response.content)
    # Extract and process the downloaded file to get medical terms
    # Your code to extract and process the downloaded file goes here
    medical_terms = [...]  # Processed medical terms from the UMLS database
    return medical_terms

# Load medical terms
medical_terms = fetch_medical_terms()

# Function to check if the user's query is medical-related
def is_medical_query(query):
    common_medical_terms = [
        "blood pressure", "hypertension", "hypotension", "heart rate", "heart rhythm",
        "diabetes", "insulin", "glucose", "cholesterol", "stroke", "heart attack",
        "asthma", "bronchitis", "pneumonia", "COPD", "emphysema", "lung cancer",
        "arthritis", "rheumatoid arthritis", "osteoarthritis", "fibromyalgia",
        "depression", "anxiety", "bipolar disorder", "schizophrenia", "PTSD",
        "Alzheimer's disease", "dementia", "Parkinson's disease", "epilepsy", "seizures",
        "migraine", "headache", "concussion", "multiple sclerosis", "MS",
        "thyroid", "hormone", "menopause", "PMS", "endometriosis", "PCOS",
        "pregnancy", "menstruation", "menstrual cycle", "ovulation", "contraception", "birth control",
        "STD", "STI", "HIV", "AIDS", "gonorrhea", "chlamydia", "syphilis",
        "cancer", "breast cancer", "colon cancer", "lung cancer", "prostate cancer", "skin cancer",
        "nutrition", "diet", "exercise", "weight loss", "obesity", "vitamins", "minerals",
        "sleep", "insomnia", "apnea", "snoring", "restless leg syndrome"
    ]
    query_words = re.findall(r'\w+', query.lower())
    medical_word_count = sum(1 for word in query_words if word in medical_terms or word in common_medical_terms)
    total_words = len(query_words)
    medical_word_percentage = medical_word_count / total_words
    return medical_word_percentage >= 0.3  # Minimum 30% of words should be medical terms

# Function to extract text from PDF
def extract_text_from_pdf(file):
    pdf_document = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text += page.get_text()
    return text

# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Display the chatbot's title on the page
st.title("🧠 Medical Diagnosis ChatBot")

# Display a disclaimer
st.markdown("""
**Disclaimer**: This chatbot provides information for educational purposes only and is not a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.
""")

# Display the chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)

# Input field for user's message
user_prompt = st.chat_input("Describe your symptoms or ask a medical question...")
if user_prompt:
    # Add user's message to chat and display it
    st.chat_message("user").markdown(user_prompt)
    
    # Check if the user's query is medical-related
    if is_medical_query(user_prompt):
        # Send user's message to Gemini-Pro and get the response
        gemini_response = st.session_state.chat_session.send_message(user_prompt)
        
        # Display Gemini-Pro's response
        with st.chat_message("assistant"):
            st.markdown(gemini_response.text)
    else:
        # Display error message for non-medical queries
        with st.chat_message("assistant"):
            st.markdown("Sorry, I can only assist with medical-related questions. Please describe your symptoms or ask a medical question.")

# File uploader for medical reports
uploaded_file = st.file_uploader("Upload a PDF medical report", type="pdf")
if uploaded_file is not None:
    with st.spinner('Processing your medical report...'):
        # Extract text from PDF
        report_text = extract_text_from_pdf(uploaded_file)
        
        # Store the extracted text in the session state
        st.session_state.medical_report_text = report_text
        
        # Notify the user that the report has been processed
        st.success("Medical report processed. You can now ask questions related to your report.")

# If a medical report has been processed, prompt the user to ask questions about it
if "medical_report_text" in st.session_state:
    user_query = st.chat_input("Ask a question about your medical report...")
    if user_query:
        # Add user's message to chat and display it
        st.chat_message("user").markdown(user_query)
        
        # Create a combined context of the report and the user's query
        combined_context = st.session_state.medical_report_text + "\n\nUser query: " + user_query
        
        # Send the combined context to Gemini-Pro and get the response
        gemini_response = st.session_state.chat_session.send_message(combined_context)
        
        # Display Gemini-Pro's response
        with st.chat_message("assistant"):
            st.markdown(gemini_response.text)
