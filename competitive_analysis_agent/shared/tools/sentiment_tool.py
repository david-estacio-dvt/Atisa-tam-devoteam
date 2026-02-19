import vertexai
from vertexai.generative_models import GenerativeModel, Part
import os

class SentimentTool:
    def __init__(self, project_id=None, location="us-central1"):
        self.project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT")
        self.location = location
        
        if self.project_id:
            try:
                vertexai.init(project=self.project_id, location=self.location)
                # Updated to Gemini 3.0 as requested
                # Updated to Gemini 2.5 Pro as requested (Feb 2026 stable)
                self.model = GenerativeModel("gemini-2.5-pro")
                self.enabled = True
            except Exception as e:
                print(f"Error initializing Vertex AI: {e}")
                self.enabled = False
        else:
            print("Warning: GOOGLE_CLOUD_PROJECT not set. Sentiment Tool disabled.")
            self.enabled = False

    def analyze(self, text, prompt_template=None):
        """
        Analyzes the sentiment of the provided text snippet.
        Returns: Positive, Negative, or Neutral.
        """
        if not self.enabled:
            return "Neutral (Mock)"

        if prompt_template:
            prompt = prompt_template.replace("{text}", text)
        else:
            # Fallback default
            prompt = f"Analyze sentiment of: {text}. Return Positive, Negative, or Neutral."
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"Error analyzing sentiment: {e}")
            return "Error"
