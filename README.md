# Chat with Google Patents

This is a Streamlit-based web application that allows you to interact with Google Patents data. The app allows users to chat with AI-powered insights from patent documents. It integrates with OpenAI's GPT-based models and the Google Patents database to retrieve and process patent information for user queries.

## Features

- **Patent Search**: Chat with an AI model to extract and answer questions related to Google Patents data.
- **Download Chat History**: Users can download the entire chat history as a PDF for reference.
- **Patent Download**: Automatically download the relevant patent PDF file when a patent link is provided.
- **Customizable**: Allows the user to provide their own OpenAI API key and patent link for a personalized experience.

## Installation

1. Clone the repository and navigate to the
- **Backend**: OpenAI GPT Model (via Langchain)
- **File Handling**: `fpdf` for generating downloadable PDFs
- **Web Scraping**: Custom patent downloader script
- **API Integration**: Google Patents API

## Installation

To run this app locally, follow these steps:

### 1. Clone the repository

```bash
git clone https://github.com/Pooyash1998/chat_with_patent.git
cd chat_with_patent
```

### 2. Install system dependencies

Depending on your operating system, install the required system-level dependencies listed in `packages.txt`:

- For Ubuntu/Debian:
```bash
cat packages.txt | xargs sudo apt-get install -y
```

- For macOS:
```bash
cat packages.txt | xargs brew install
```

### 3. Setup Virtual Environment

You can choose any methods to set up your environmen. You may use conda or venv instead of poetry integrated venvs but make sure to install all the packages in poetry.lock manually according to your usecase.

#### Using Poetry (recommended)
```bash
# Install Poetry if you haven't already
curl -sSL https://install.python-poetry.org | python3 -

# Initialize poetry and install dependencies
poetry install

# Activate the poetry environment
poetry shell
```
