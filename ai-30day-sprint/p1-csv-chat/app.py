import os
import json
import requests
import pandas as pd
import gradio as gr
from typing import List, Optional, Dict, Any
from langchain.document_loaders import CSVLoader
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.llms.base import LLM
from langchain.callbacks.manager import CallbackManagerForLLMRun
from pydantic import Field
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize global variables
vector_store = None
df = None


def public_share_enabled() -> bool:
    """Return True only when public Gradio sharing is explicitly enabled."""
    return os.getenv("GRADIO_SHARE", "").strip().lower() in {"1", "true", "yes", "on"}


def load_csv(file_path: str) -> str:
    """Load and process the CSV or Excel file."""
    global df, vector_store
    
    try:
        # Determine file type and load into pandas
        if file_path.lower().endswith(('.xlsx', '.xls')):
            # Read Excel file
            df = pd.read_excel(file_path, engine='openpyxl')
            # Save to temporary CSV for LangChain
            temp_path = "temp_data.csv"
            df.to_csv(temp_path, index=False)
            # Load documents from the temporary CSV
            loader = CSVLoader(file_path=temp_path, encoding="utf-8")
        else:
            # Handle CSV files
            df = pd.read_csv(file_path)
            temp_path = "temp_data.csv"
            df.to_csv(temp_path, index=False)
            loader = CSVLoader(file_path=temp_path, encoding="utf-8")
        
        # Load documents
        documents = loader.load()
        
        # Create embeddings and vector store
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vector_store = Chroma.from_documents(documents, embeddings)
        
        # Clean up
        if 'temp_path' in locals() and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception as e:
                print(f"Warning: Could not remove temporary file: {e}")
            
        return "File loaded successfully! You can now ask questions about your data."
    except Exception as e:
        return f"Error loading CSV: {str(e)}"

class DeepSeekLLM(LLM):
    """Custom LLM wrapper for DeepSeek API."""
    
    model_name: str = "deepseek-chat"
    temperature: float = 0.1
    max_tokens: int = 2000
    
    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        """Call the DeepSeek API."""
        url = "https://api.deepseek.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {os.getenv('DEEPSEEK_API_KEY')}"
        }
        
        payload = {
            "model": self.model_name,
            "messages": [
                {"role": "system", "content": "You are a helpful AI assistant that answers questions about data."},
                {"role": "user", "content": prompt}
            ],
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            return f"Error calling DeepSeek API: {str(e)}"
    
    @property
    def _llm_type(self) -> str:
        return "deepseek"

def query_data(question: str) -> str:
    """Query the loaded CSV data."""
    global vector_store, df
    
    if vector_store is None or df is None:
        return "Please load a CSV file first."
    
    try:
        # Create QA chain with DeepSeek
        qa_chain = RetrievalQA.from_chain_type(
            llm=DeepSeekLLM(),
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
    with gr.Blocks(title="Excel/CSV Chat") as demo:
        gr.Markdown("# 📊 Excel/CSV Chat")
        gr.Markdown("Upload an Excel or CSV file and ask questions about your data in plain English!")
        
        with gr.Row():
            with gr.Column():
                file_input = gr.File(label="Upload Excel/CSV File", type="file")
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
    # Check for DeepSeek API key
    if not os.getenv("DEEPSEEK_API_KEY"):
        print("Error: DEEPSEEK_API_KEY environment variable not set.")
        print("Please set it in a .env file or as an environment variable.")
        print("You can get an API key from https://platform.deepseek.com/")
        exit(1)

    # Create interface and launch locally by default.
    demo = create_interface()
    demo.launch(share=public_share_enabled())
