import os
import re
import streamlit as st
from dotenv import load_dotenv

from langchain.vectorstores import FAISS
from langchain.document_loaders import PyMuPDFLoader
from langchain.chains import RetrievalQA
from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    GoogleGenerativeAIEmbeddings
)

# Load environment variables (API keys, etc.)
load_dotenv()

# Initialize LLM and Embedding models from Gemini
embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.2)

# Configure Streamlit UI
st.set_page_config(page_title="PDF Q&A with Gemini", page_icon="📄")
st.title("📄 Ask Questions From Your PDF")
st.caption("Powered by Google Gemini + FAISS + LangChain")

# Upload section
uploaded_file = st.file_uploader("📁 Upload your PDF file", type="pdf")

@st.cache_resource(show_spinner=False)
def process_pdf(file_bytes, file_name):
    """Extract text from PDF and build a vector store index."""
    temp_path = f"temp_{file_name}"
    with open(temp_path, "wb") as f:
        f.write(file_bytes)

    loader = PyMuPDFLoader(temp_path)
    documents = loader.load()

    # Create vector index from documents
    vectorstore = FAISS.from_documents(documents, embedding=embedding_model)

    # Remove temporary file
    os.remove(temp_path)

    return vectorstore

def create_qa_chain(vectorstore):
    """Create a question-answering chain using the vector store."""
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 2})
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )
    return qa

def clean_snippet(text):
    """Remove excess formatting and line breaks for cleaner display."""
    text = re.sub(r'\n+', ' ', text)           # Replace multiple newlines with space
    text = re.sub(r'\s{2,}', ' ', text)        # Replace multiple spaces with one
    return text.strip()

def display_source_snippets(source_documents):
    """Display source text from which the answer was generated."""
    with st.expander("📚 Source Snippet(s)", expanded=False):
        for doc in source_documents:
            page = doc.metadata.get("page", "?")
            snippet = clean_snippet(doc.page_content)
            short_snippet = snippet[:700] + ("..." if len(snippet) > 700 else "")
            st.markdown(f"🔹 **Page {page}**")
            st.write(short_snippet)

# Main logic
if uploaded_file:
    file_name = uploaded_file.name
    st.success(f"✅ {file_name} uploaded successfully!")

    with st.spinner("🔍 Processing your PDF..."):
        vectorstore = process_pdf(uploaded_file.read(), file_name)
        qa_chain = create_qa_chain(vectorstore)
        st.success("✅ Your PDF is ready for questions!")

    # Text input for questions
    question = st.text_input("💬 Ask a question:")

    if question:
        with st.spinner("🤖 Thinking..."):
            result = qa_chain.invoke({"query": question})
            st.markdown(f"**🧠 Answer:** {result['result']}")
            display_source_snippets(result["source_documents"])
else:
    st.info("👆 Upload a PDF to get started.")
