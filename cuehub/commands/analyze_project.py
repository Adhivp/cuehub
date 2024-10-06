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

    def analyze_project_structure(self, file_structure):
        prompt = """

You are an expert software developer and project architect. Your task is to analyze the following file structure and contents of a software project. Based on this analysis, provide an evaluation of the project structure, highlighting any potential issues or areas for improvement.

Project Structure: {file_structure}

Please perform the following tasks:

Identify the type of project (e.g., web application, mobile app, data analysis project, etc.) based on the file structure and contents.

Evaluate the overall organization of the project:

Is it following best practices for the identified project type?
Are there clear separations of concerns (e.g., frontend/backend, data/logic/presentation layers)?
Assess the naming conventions and consistency across the project.

Identify any missing crucial components or files that are typically expected in this type of project.

Look for potential security issues based on the file structure (e.g., exposed sensitive information, lack of proper configuration files).

Evaluate the project's scalability and maintainability based on its current structure.

Suggest improvements or reorganizations that could enhance the project's quality, readability, or efficiency. Focus solely on the identified issues, providing clear explanations and suggestions for improvement.

Please provide your analysis in a clear, structured format, emphasizing the areas needing improvement. No README or markdown file outputs are allowed.
        """
        prompt = prompt.format(file_structure=file_structure)
        return self.generate_content(prompt)