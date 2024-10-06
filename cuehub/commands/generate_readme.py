import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

class GeminiAPI:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.base_url = "https://generativelanguage.googleapis.com/v1/models/gemini-1.0-pro:generateContent"

    def generate_content(self, prompt):
        headers = {
            "Content-Type": "application/json"
        }
        
        data = {
            "contents": [{"parts":[{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.7,
                "topK": 1,
                "topP": 1,
                "maxOutputTokens": 2048,
                "stopSequences": []
            }
        }
        
        params = {
            "key": self.api_key
        }
        
        response = requests.post(self.base_url, headers=headers, params=params, json=data)
        
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"Error: {response.status_code}, {response.text}"

    def generate_readme(self, project_info):
        prompt = """
        Generate a comprehensive README.md file for the following project:

        {project_info}

        Please include the following sections:
        1. Project Title and Description
        2. Features
        3. Installation
        4. Usage
        5. Configuration (if applicable)
        6. Contributing (if open-source)
        7. License (suggest an appropriate license if open-source)
        8. Contact Information

        Ensure the README is informative, well-structured, and follows best practices for the project type (open-source or closed-source).
        The README should be in Markdown format.
        """
        prompt = prompt.format(project_info=project_info)
        return self.generate_content(prompt)