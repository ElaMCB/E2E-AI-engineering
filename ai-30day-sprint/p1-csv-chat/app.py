import os
import pandas as pd
import gradio as gr
from typing import List, Optional
from langchain.document_loaders import CSVLoader
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize global variables
vector_store = None
df = None

def load_csv(file_path: str) -> str:
    """Load and process the CSV file."""
    global df, vector_store
    
    try:
        # Load CSV into pandas
        df = pd.read_csv(file_path)
        
        # Save to temporary CSV for LangChain
        temp_path = "temp_data.csv"
        df.to_csv(temp_path, index=False)
        
        # Load documents
        loader = CSVLoader(file_path=temp_path, encoding="utf-8")
        documents = loader.load()
        
        # Create embeddings and vector store
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vector_store = Chroma.from_documents(documents, embeddings)
        
        # Clean up
        if os.path.exists(temp_path):
            os.remove(temp_path)
            
        return "CSV file loaded successfully! You can now ask questions about the data."
    except Exception as e:
        return f"Error loading CSV: {str(e)}"

def query_data(question: str) -> str:
    """Query the loaded CSV data."""
    global vector_store, df
    
    if vector_store is None or df is None:
        return "Please load a CSV file first."
    
    try:
        # Create QA chain
        qa_chain = RetrievalQA.from_chain_type(
            llm=OpenAI(temperature=0),
            chain_type="stuff",
            retriever=vector_store.as_retriever(),
            return_source_documents=True
        )
        
        # Get response
        result = qa_chain({"query": question})
        return result["result"]
    except Exception as e:
        return f"Error processing your question: {str(e)}"

# Create Gradio interface
def create_interface():
    with gr.Blocks(title="CSV Chat") as demo:
        gr.Markdown("# 📊 CSV Chat")
        gr.Markdown("Upload a CSV file and ask questions about your data!")
        
        with gr.Row():
            with gr.Column():
                file_input = gr.File(label="Upload CSV File", type="filepath")
                load_btn = gr.Button("Load Data")
                status = gr.Textbox(label="Status", interactive=False)
                
                gr.Examples(
                    examples=[["What are the column names?"],
                             ["Show me summary statistics"],
                             ["What is the average value of column X?"]],
                    inputs=gr.Textbox(placeholder="Ask a question about your data...", label="Question")
                )
                
            with gr.Column():
                question = gr.Textbox(placeholder="Ask a question about your data...", label="Question")
                ask_btn = gr.Button("Ask")
                answer = gr.Textbox(label="Answer", interactive=False, lines=5)
        
        load_btn.click(fn=load_csv, inputs=file_input, outputs=status)
        ask_btn.click(fn=query_data, inputs=question, outputs=answer)
    
    return demo

if __name__ == "__main__":
    # Check for OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable not set.")
        print("Please create a .env file with your OpenAI API key.")
        exit(1)
    
    # Launch the app
    app = create_interface()
    app.launch(share=False)
