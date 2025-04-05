import os
import pickle
from dotenv import load_dotenv

from langchain.vectorstores import FAISS
from langchain.document_loaders import PyMuPDFLoader
from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings

# Load environment variables
load_dotenv()

# Constants
PDF_PATH = "effective-pandas.pdf"
INDEX_PATH = "faiss_index"
TEXTS_PATH = "texts.pkl"

# === 1. Load Google Embeddings Model (instead of HuggingFace) ===
embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# === 2. Load Gemini Pro LLM ===
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0.2
)

def load_or_create_documents(pdf_path):
    """Extract documents from PDF using LangChain."""
    loader = PyMuPDFLoader(pdf_path)
    return loader.load()

def create_or_load_vectorstore(docs):
    """Create or load FAISS vector index."""
    if os.path.exists(f"{INDEX_PATH}.faiss") and os.path.exists(TEXTS_PATH):
        print("✅ Loading existing FAISS index...")
        vectorstore = FAISS.load_local(INDEX_PATH, embeddings=embedding_model)
        with open(TEXTS_PATH, "rb") as f:
            texts = pickle.load(f)
    else:
        print("🔄 Creating new FAISS index...")
        vectorstore = FAISS.from_documents(docs, embedding=embedding_model)
        vectorstore.save_local(INDEX_PATH)

        texts = [doc.page_content for doc in docs]
        with open(TEXTS_PATH, "wb") as f:
            pickle.dump(texts, f)

    return vectorstore

def create_qa_chain(vectorstore):
    """Build RetrievalQA chain using Gemini + FAISS retriever."""
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 1})
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )
    return qa_chain

def main():
    try:
        docs = load_or_create_documents(PDF_PATH)
        vectorstore = create_or_load_vectorstore(docs)
        qa_chain = create_qa_chain(vectorstore)

        print("\n📘 Gemini + Vertex AI Embeddings ready. Ask a question or type 'exit'.")

        while True:
            query = input("\n🧑 USER: ")
            if query.lower() == "exit":
                break

            print("\n🤖 Generating AI response...\n")
            result = qa_chain.invoke({"query": query})
            print("🧠 AI:", result['result'])

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
