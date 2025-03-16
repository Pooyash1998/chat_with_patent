# Chat with Google Patents

This is a Streamlit-based web application that allows you to interact with Google Patents data. The app allows users to chat with AI-powered insights from patent documents. It integrates with OpenAI's GPT-based models and the Google Patents database to retrieve and process patent information for user queries.

## Features

- **Patent Search**: Chat with an AI model to extract and answer questions related to Google Patents data.
- **Download Chat History**: Users can download the entire chat history as a PDF for reference.
- **Patent Download**: Automatically download the relevant patent PDF file when a patent link is provided.
- **Customizable**: Allows the user to provide their own OpenAI API key and patent link for a personalized experience.

## Usage
This app is deployed on Streamlit Cloud and can be accessed via this link: [http://chat-with-patent.streamlit.app](http://chat-with-patent.streamlit.app/).

If you wish to run it locally, please note the following:

1. **SQLite3 Compatibility**: Streamlit's SQLite3 is not updated, so the app imports `pysqlite3` instead. The `pysqlite3` package is added to the `requirements.txt` (which Streamlit uses), but when running the app locally, you should only use `poetry.lock` or avoid installing `pysqlite3` manually.

2. **Chromium Version**: Due to version issues, the Chromium version that Streamlit uses is fixed. Make sure to install the appropriate Chromium version based on your operating system before proceeding. Additionally, in the `patent_download.py` class, you should update the `driver_version` to be compatible with your Chromium version.

## Installation

To run this app locally, follow these steps:

### 1. Clone the repository

```bash
git clone https://github.com/Pooyash1998/chat_with_patent.git
cd chat_with_patent
```

### 2. Setup Virtual Environment

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
