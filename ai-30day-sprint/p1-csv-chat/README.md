# 📊 Excel/CSV Chat: Natural Language Interface for Spreadsheet Analysis

A powerful tool that enables natural language interaction with CSV data, making data analysis accessible to non-technical users through simple conversations.

## 🎯 Project Purpose

### Why This Project?
In today's data-driven world, not everyone is comfortable writing complex queries or understanding spreadsheet formulas. This project bridges that gap by allowing users to ask questions about their Excel/CSV data in plain English, making data analysis more accessible to everyone without requiring SQL or advanced Excel knowledge.

### What You'll Learn
- How to build an AI-powered natural language interface
- Working with vector databases (ChromaDB) for efficient data retrieval
- Implementing RAG (Retrieval-Augmented Generation) for accurate responses
- Creating user-friendly interfaces with Gradio
- Handling and processing tabular data with Pandas

## 🛠️ Technical Approach

### Architecture Overview
1. **Data Ingestion**: CSV files are loaded and preprocessed
2. **Vector Embedding**: Text data is converted to vector representations using sentence transformers
3. **Semantic Search**: User queries are matched with relevant data using vector similarity
4. **Response Generation**: The DeepSeek LLM generates human-like responses based on the retrieved data

### Why This Stack?
- **LangChain**: Provides the framework for chaining LLM operations
- **ChromaDB**: Lightweight, in-memory vector database for efficient similarity search
- **DeepSeek**: High-quality language model for generating accurate, context-aware responses
- **Gradio**: Simplifies building and sharing ML web apps

## 🚀 Features

- **Excel/CSV Support**: Works with both Excel (.xlsx, .xls) and CSV files
- **Natural Language Queries**: Ask questions about your spreadsheet data in plain English
- **Instant Insights**: Get quick answers without writing complex formulas or queries
- **User-Friendly Interface**: Simple, intuitive web interface for easy interaction
- **Data Privacy**: All processing happens locally (except for the LLM API call)
- **No Setup Required**: Just upload and start asking questions

## 🛠️ Tech Stack

- **Backend**: Python 3.8+
- **AI/ML**: LangChain, DeepSeek API, Sentence Transformers
- **Vector Database**: ChromaDB
- **Web Interface**: Gradio
- **Data Processing**: Pandas

## 🏃‍♂️ Quick Start

1. **Set up environment**
   ```bash
   # Create and activate virtual environment
   python -m venv venv
   .\venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

2. **Configure API Key**
   Create a `.env` file with your DeepSeek API key:
   ```
   DEEPSEEK_API_KEY=your_api_key_here
   ```

3. **Run the application**
   ```bash
   python app.py
   ```
   Open your browser to `http://localhost:7860`

## 🚀 Try It Out

1. **Live Demo**: [Try it on Hugging Face Spaces](https://huggingface.co/spaces/AzzuraM/excel-csv-chat-RAG)

## 📚 Learning Resources

1. **For Beginners**
   - [Pandas Documentation](https://pandas.pydata.org/docs/)
   - [Gradio Quickstart](https://gradio.app/quick_start/)
   
2. **Advanced Topics**
   - [LangChain Documentation](https://python.langchain.com/docs/)
   - [Vector Databases Explained](https://www.pinecone.io/learn/vector-database/)

## 🤝 Contributing

Contributions are welcome! Please read our [contributing guidelines](CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by the need for more accessible data analysis tools
- Built with amazing open-source libraries
2. [Streamlit Cloud](https://streamlit.io/cloud)
3. [PythonAnywhere](https://www.pythonanywhere.com/)

## Blog Post

Read about how this project was built: [How I Built an Excel/CSV Chatbot Without Fine-tuning](BLOG.md)

## License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.
