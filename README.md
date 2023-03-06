# Big News!

There's now an official ChatGPT API!!!

Watch the walk-through video for this repo here:

[![ChatGPT API Walkthrough](https://img.youtube.com/vi/k-ieXU3apBY/0.jpg)](https://youtu.be/k-ieXU3apBY)

If you want to look at the old code for this project Simply clone the repo and checkout the `davinci-version` branch.

```
git checkout davinci-version
```

Otherwise, just use the default `main` branch and you'll be plugged into the official ChatGPT API!

# Command Line ChatGPT Bot

This is a simple chat-bot that uses the OpenAI ChatGPT API.

You can watch the original video walkthrough that uses the davinci-model [here](https://youtu.be/jQFhtFMDz1s). There will be a new video coming shortly to match the new code.

# Setup

Make sure you have python3 installed:

```
python3 --version
```

Create a virtual environment and install the dependencies:

### Linux/Mac:

```
python3 -m venv venv
. ./venv/bin/activate
pip install -r requirements.txt
```

### Windows:

```
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
```

# Configuration

Copy `env.sample` to `.env` and add your OpenAI API key to the file.

```
OPENAI_API_KEY=<<YOUR_API_KEY>>
```

Edit `main.py` and replace `<<PUT THE PROMPT HERE>>` with your prompt:

e.g. Create a simple AI cocktail assistant

```
INSTRUCTIONS = """You are an AI assistant that is an expert in alcoholic beverages.
You know about cocktails, wines, spirits and beers.
You can provide advice on drink menus, cocktail ingredients, how to make cocktails, and anything else related to alcoholic drinks.
If you are unable to provide an answer to a question, please respond with the phrase "I'm just a simple barman, I can't help with that."
Please aim to be as helpful, creative, and friendly as possible in all of your responses.
Do not use any external URLs in your answers. Do not refer to any blogs in your answers.
Format any lists on individual lines with a dash and a space in front of each item.
"""
```

# Running

To run just do the following:

### Linux/Mac:

```
. ./venv/bin/activate
python main.py
```

### Windows:

```
venv\Scripts\activate.bat
python main.py
```
