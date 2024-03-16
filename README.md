## Summarize Branch Changes (compared with main) With AI (ChatGPT)

This is a simple utility for summarizing the changes on the current PR / branch that you are working on as related to the "main" branch of your project.

### Setup

1. Copy [summarize_changes.py](summarize_changes.py) and the empty [pr-summaries](pr-summaries) folder to the root of your project for which you want to summarize your changes.
2. If you already have a `.env` file in your project:
   1. Add `OPENAI_API_KEY=your api key` to your `.env` file. If that `.env` is not in the root of your project, you will need to change the `ENV_PATH` in [summarize_changes.py](summarize_changes.py) to point at your `.env` file.
3. If you don't already have a `.env` file in your project:
   1. Create one in the root of your project and add `OPENAI_API_KEY=your api key` to it.
4. Install Python dependencies `requests` and `python-dotenv`. I recommend creating a virtual environment in the root of your project for this if you do not already have one: `python3 -m venv venv`. Then activate it with `source venv/bin/activate` (or `source venv/Scripts/activate` on Windows). Then install your dependencies with `pip install requests python-dotenv`.
5. Modify your `.gitignore`:
   1. If you do not already have a `.gitignore` file in your project, create one.
   2. Add `pr-summaries`, `venv` and `.env` to your `.gitignore` file on separate lines to prevent your PR summaries, virtual environment, and API key from being included in version control. You will likely also want to add the `summarize_changes.py` script if you don't want it included in your project's version control.

### Usage

1. Work as normal by creating a new branch off of your main branch, e.g., `git checkout -b my-new-feature`.
2. After you finish coding/testing/documenting, stage and commit your changes.
3. Run `python summarize_changes.py` (to run, you'll need to either have your virtual environment activated or you need `requests` and `python-dotenv` installed globally).

Note: OpenAI API keys can be obtained from [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys).

# Example:

I actually used this utility to generate a PR summary for the first PR on this project, which you can find here: [https://github.com/austinjhunt/summarize-pr-with-ai/pull/1](https://github.com/austinjhunt/summarize-pr-with-ai/pull/1).

You'll notice I did not gitignore the `pr-summaries` folder for this project for the sake of keeping the example content, but you should gitignore it on yours.
