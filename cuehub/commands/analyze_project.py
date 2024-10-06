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
You are an expert software developer and project architect. Your task is to analyze the following file structure and contents of a software project. Based on this analysis, provide an evaluation of the project structure, highlighting its strengths and identifying any potential issues or areas for improvement.

Project Structure:
```
{file_structure}
```

Please perform the following tasks:

1. Identify the type of project (e.g., web application, mobile app, data analysis project, etc.) based on the file structure and contents.

2. Evaluate the overall organization of the project:
   - Is it following best practices for the identified project type?
   - Are there clear separations of concerns (e.g., frontend/backend, data/logic/presentation layers)?

3. Assess the naming conventions and consistency across the project.

4. Identify any missing crucial components or files that are typically expected in this type of project.

5. Look for potential security issues based on the file structure (e.g., exposed sensitive information, lack of proper configuration files).

6. Evaluate the project's scalability and maintainability based on its current structure.

7. Suggest improvements or reorganizations that could enhance the project's quality, readability, or efficiency.

8. If the project structure appears to be well-organized and follows best practices, explicitly state that it looks good and explain why.

Please provide your analysis in a clear, structured format. If the project structure is good, praise its strong points. If there are issues, list them out clearly with explanations and suggestions for improvement.

Your response should be thorough yet concise, focusing on the most important aspects of the project structure.
        """
        prompt = prompt.format(file_structure=file_structure)
        return self.generate_content(prompt)