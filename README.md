📄 Ask Questions From Your PDF
A Streamlit app that allows users to upload a PDF and ask questions based on its content, powered by Google Gemini, LangChain, and FAISS.

🚀 Features
Upload a PDF file

Extract and index text from the PDF

Ask questions and get AI-powered answers

View source snippets supporting the answers

💻 Requirements
Python 3.7+

Streamlit

LangChain

FAISS

Google Gemini API key

🛠️ Setup
1. Clone the Repository
bash
Copy
Edit
git clone <repository-url>
cd <project-directory>
2. Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
3. Setup .env File
Create a .env file in the project root and add your Google API key:

env
Copy
Edit
GOOGLE_API_KEY=<your-google-api-key>
🔥 Running the App
bash
Copy
Edit
streamlit run app.py
Access the app at http://localhost:8501.

📄 Files
app.py: Streamlit app code

requirements.txt: Dependencies list

.env: Google API key configuration
