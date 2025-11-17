# How I Built an Excel/CSV Chatbot Without Fine-tuning

In this post, I'll walk you through how I created a natural language interface for Excel and CSV files using modern AI techniques. This project was part of my 30-day AI engineering sprint, where I explore different AI applications.

## The Problem

Working with spreadsheet data often requires writing complex formulas or queries, which can be a barrier for non-technical users. I wanted to create a solution that would allow anyone to ask questions about their data in plain English and get accurate answers without needing to write code or understand complex query languages.

## The Solution

I built a web application that combines several powerful technologies:

1. **Retrieval-Augmented Generation (RAG)**: This approach allows the system to find relevant information from the data before generating a response, leading to more accurate answers.

2. **Vector Database (ChromaDB)**: Stores document embeddings for fast similarity search, enabling the system to quickly find relevant parts of your data.

3. **DeepSeek API**: Powers the language model that understands natural language queries and generates responses.

4. **Gradio**: Provides a simple web interface for users to upload files and ask questions.

## How It Works

1. **Data Ingestion**: Users upload an Excel or CSV file through the web interface.

2. **Data Processing**: The application reads the file, generates embeddings for the content, and stores them in ChromaDB.

3. **Query Processing**: When a user asks a question, the system:
   - Converts the question into an embedding
   - Finds the most relevant parts of the data
   - Uses the DeepSeek model to generate a natural language answer

4. **Response Generation**: The system presents the answer in a user-friendly format, often including relevant data points from the file.

## Technical Stack

- **Backend**: Python
- **AI/ML**: LangChain, DeepSeek API, Sentence Transformers
- **Vector Database**: ChromaDB
- **Web Interface**: Gradio
- **Data Processing**: Pandas, OpenPyXL

## Key Features

- **Natural Language Interface**: Ask questions in plain English
- **Multiple File Formats**: Supports both Excel (.xlsx, .xls) and CSV files
- **No Data Leaves Your Machine**: All processing happens locally (except for the LLM API call)
- **Responsive Web Interface**: Easy to use on any device
- **Open Source**: The code is available on GitHub for anyone to use and improve

## Challenges and Learnings

1. **File Format Handling**: Supporting both Excel and CSV required careful handling of different data structures and edge cases.

2. **Efficient Searching**: Implementing RAG with ChromaDB allowed for fast similarity searches even with large datasets.

3. **Prompt Engineering**: Crafting effective prompts for the DeepSeek model was crucial for getting accurate and relevant responses.

4. **Deployment**: Setting up the application on Hugging Face Spaces required careful management of dependencies and environment variables.

## Future Improvements

- Add support for more file formats (e.g., Google Sheets, database connections)
- Implement caching for faster responses to similar queries
- Add visualization capabilities to better present data in responses
- Support for multi-file analysis
- Add user authentication for private data

## Try It Yourself

You can try out the live demo on [Hugging Face Spaces](https://huggingface.co/spaces/AzzuraM/excel-csv-chat-RAG). The complete source code is available on [GitHub](https://github.com/ElaMCB/E2E-AI-engineering/tree/main/ai-30day-sprint/p1-csv-chat).

## Conclusion

This project demonstrates how modern AI can make data analysis more accessible to everyone. By combining RAG with large language models, we can create powerful interfaces that understand natural language and provide meaningful insights from structured data.

I'm excited to see how this technology evolves and how it can be applied to other domains. If you have any questions or suggestions, feel free to reach out!
