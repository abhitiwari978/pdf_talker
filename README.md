📄 Ask Questions From Your PDF
A simple Streamlit app that allows users to upload a PDF file and ask questions based on its content. The app uses Google Gemini for AI-powered question answering, LangChain for managing the pipeline, and FAISS for efficient similarity search over document contents.



🛠️ Features
Upload PDF: Upload a PDF file to the app.

Text Extraction: Extracts text from the PDF and indexes it for efficient searching.

AI-Powered Q&A: Ask questions based on the content of the PDF and get answers powered by Google Gemini.

Source Snippets: View source text snippets from the document that support the answer.



💻 Requirements
Before running the app, ensure you have the following installed:

Python 3.7 or later

Streamlit

LangChain

FAISS

Google Gemini API keys (both for embeddings and chat models)



🚀 Setup Instructions
1. Clone the Repository
First, clone this repository to your local machine:

bash
Copy
Edit
git clone <repository-url>
cd <project-directory>
2. Create and Activate Virtual Environment (optional but recommended)
Create a virtual environment for the project:

bash
Copy
Edit
python -m venv venv
Activate the virtual environment:

On Windows:

bash
Copy
Edit
venv\Scripts\activate
On macOS/Linux:

bash
Copy
Edit
source venv/bin/activate
3. Install Dependencies
Install all the required dependencies by running:

bash
Copy
Edit
pip install -r requirements.txt
🌳 Setting up the .env File
To authenticate with Google Gemini, you’ll need to set up your API keys.

Create a .env file in the root of the project directory.

Add your API key to the .env file:

env
Copy
Edit
GOOGLE_API_KEY=<your-google-api-key>
Replace <your-google-api-key> with your actual Google Gemini API key. You can obtain the key from the Google Cloud Console.



🔥 Running the App
Once everything is set up, you can run the app with:

bash
Copy
Edit
streamlit run app.py
This will start the app locally. You can access it in your browser at http://localhost:8501.

🛠️ How It Works
Upload PDF: The user uploads a PDF file through a file uploader in the app interface.

Text Extraction: The app uses the PyMuPDFLoader to extract the text from the PDF.

Vector Store: The extracted text is indexed in a FAISS vector store for fast similarity search.

Ask Questions: After processing the PDF, users can input a question, and the system uses Google Gemini to retrieve relevant text from the PDF and generate an answer.

Display Results: The app displays the answer along with source snippets from the PDF that led to the response.
