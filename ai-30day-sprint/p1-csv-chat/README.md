# CSV-Chat: Natural Language Querying for Spreadsheets

A simple yet powerful tool that lets you ask natural language questions about your CSV data.

## Features

- Upload any CSV file
- Ask questions in natural language
- Get instant answers with relevant data
- Simple and intuitive interface

## Tech Stack

- Python 3.8+
- LangChain
- Chroma DB
- Sentence Transformers
- Gradio
- Pandas
- OpenAI API

## Quick Start

1. Clone the repository
2. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python app.py
   ```
5. Open your browser to `http://localhost:7860`

## Testing

Run the test suite:
```bash
python -m pytest test_app.py -v
```

## Deployment

This application can be deployed on any platform that supports Python applications. For quick deployment, we recommend:

1. [Hugging Face Spaces](https://huggingface.co/spaces)
2. [Streamlit Cloud](https://streamlit.io/cloud)
3. [PythonAnywhere](https://www.pythonanywhere.com/)

## Blog Post

Read about how this project was built: [How I Turned a CSV into a Chatbot Without Fine-tuning]()

## License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.
