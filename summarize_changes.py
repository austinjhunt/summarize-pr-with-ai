"""
Austin Hunt
3/16/2024
Created in conjunction with ChatGPT support.
This script uses the OpenAI GPT-4 model to summarize the changes in a pull request.
It fetches the diff of the current branch from the default branch (e.g., main) and sends it to the OpenAI API to generate a summary in less than 1000 words in markdown format.
Ideal for small PRs.
Requires paying for OpenAI API access.

"""
import os
import subprocess
import requests
from dotenv import load_dotenv

ENV_PATH = os.path.join(os.path.dirname(__file__), ".env")

# Replace 'main' with your default branch if it's named differently, e.g., "master"
DEFAULT_BRANCH_NAME = "main"


class ChatGPTPRSummarizer:
    def __init__(self, openai_api_key=None):
        print("Initializing ChatGPTPRSummarizer...")
        self.openai_api_key = openai_api_key
        self.session = requests.Session()
        self.session.headers = {
            "Authorization": f"Bearer {self.openai_api_key}",
            "Content-Type": "application/json",
        }


    def fetch_diff(self, branch_name):
        """ Fetch the diff of the current branch from the default branch """
        print(f"Fetching diff of {branch_name} from {DEFAULT_BRANCH_NAME}...")
        # Replace 'main' with your default branch if it's named differently
        cmd = ["git", "diff", f"{DEFAULT_BRANCH_NAME}...{branch_name}"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.stdout


    def get_current_branch_name(self):
        print("Getting the current branch name...")
        command = ["git", "rev-parse", "--abbrev-ref", "HEAD"]
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode == 0:  # Check if the command was successful
            return result.stdout.strip()  # Strip to remove any newline characters
        else:
            raise Exception("Failed to get current branch name")

    def _build_message_payload(self, diff_text=""):
        """ prepare the payload for the OpenAI API using the diff text to summarize """
        return {
            "model": "gpt-4",  # Update the model if needed
            "messages": [
                {
                    "role": "user",
                    "content": f"Concisely summarize the following code changes in LESS THAN 1000 WORDS IN MARKDOWN FORMAT:\n\n{diff_text}",
                }
            ],
            "temperature": 0.7,
        }


    def get_chatgpt_summary(self, diff_text, api_key):
        """
        Uses OpenAI's GPT-4 model to summarize the diff text in markdown format with a maximum of 1000 words (not using max_tokens to avoid truncation)
        """
        print("Making API call to OpenAI to summarize the changes...")
        data = self._build_message_payload(diff_text)
        response = self.session.post("https://api.openai.com/v1/chat/completions", json=data)
        return response.json().get("choices", [{}])[0].get("message", {}).get("content", "")


    def summarize_pull_request(self, branch_name=None, api_key=None):
        """ Summarize the changes in the pull request """
        print("Summarizing the changes in the pull request...")
        if not branch_name:
            branch_name = self.get_current_branch_name()
            print("Branch name not provided. Using the current branch: {}".format(branch_name))
        if not branch_name or not api_key:
            print("Branch name and API key are required")
            raise ValueError("Branch name and API key are required")
        diff_text = self.fetch_diff(branch_name)
        summary = self.get_chatgpt_summary(diff_text, api_key)
        self.save_summary(summary=summary, branch_name=branch_name)


    def save_summary(self, summary="", branch_name=""):
        """ Save the summary to a file in pr-summaries folder """
        clean_branch_name = branch_name.replace("/", "slash")
        summary_file = f"pr-summaries/summary-{clean_branch_name}.txt"
        print(f"Saving summary to {summary_file}")
        with open(summary_file, "w") as file:
            file.write(summary)


if __name__ == "__main__":
    # verify that pr-summaries folder exists and .env file is present
    if not os.path.exists(ENV_PATH):
        raise FileNotFoundError(f"Environment file {ENV_PATH} file not found. You may need to create one or change the ENV_PATH of this script.")
    load_dotenv(dotenv_path=ENV_PATH, verbose=True)
    api_key = os.getenv("OPENAI_API_KEY", None)
    if not api_key:
        raise ValueError("OpenAI API key not found in .env file")

    summarizer = ChatGPTPRSummarizer(openai_api_key=api_key)
    summarizer.summarize_pull_request(api_key=api_key)
