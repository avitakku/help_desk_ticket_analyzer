# Installation Guide for Help Desk Ticket Analyzer

Follow these steps to get Help Desk Ticket Analyzer up and running on your local machine.

## Set up:

Install [Python](https://www.python.org/downloads/) if you don't have it already

## Getting API Key

### OpenAI API Key

Get OpenAI API key from the [OpenAI website](https://openai.com/blog/openai-api)

## API Key safety:

Follow these [steps](https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety) OR

Create a config.py file with the following code:
```python
api_key = INSERT_YOUR_ACTUAL_API_KEY_HERE
```

## Running the code:
**Step 1:**
Download all requirements from the requirements.txt file

**Step 2:**
To run the code locally, run the following command in your Command Line Interface (ensure you are in the directory where all the files are present):
```python
  python server.py
```

**Step 3:**
Open the link that shows up in your browser!
