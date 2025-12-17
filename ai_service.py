"""AI service using Google Gemini."""
import time
import google.generativeai as genai
from rich.console import Console

console = Console()


class AIService:
    """Service for AI content generation using Gemini."""
    
    def __init__(self, api_key):
        if not api_key:
            raise ValueError("API key is required but was not provided")
        
        if not isinstance(api_key, str) or len(api_key.strip()) == 0:
            raise ValueError("API key must be a non-empty string")
        
        genai.configure(api_key=api_key)
        self.model = self._initialize_model()
    
    def _initialize_model(self):
        """Connect to Gemini model."""
        # Try models in order of preference (most stable/common first)
        models = ['gemini-2.5-flash', 'gemini-2.5-pro', 'gemini-pro', 'models/gemini-pro']
        errors = []
        
        for name in models:
            try:
                model = genai.GenerativeModel(name)
                # Test connection with a simple request
                response = model.generate_content("Hello")
                if response and response.text:
                    console.print(f"[green]✓[/green] Connected to {name}")
                    return model
            except Exception as e:
                error_msg = f"{name}: {str(e)}"
                errors.append(error_msg)
                console.print(f"[yellow]⚠[/yellow] Failed to connect to {name}: {str(e)}")
                continue
        
        error_details = "\n".join(errors)
        raise ValueError(
            f"Could not connect to any Gemini model.\n"
            f"Errors:\n{error_details}\n\n"
            f"Troubleshooting steps:\n"
            f"1. Verify your GEMINI_API_KEY is valid and set in .env file\n"
            f"2. Check your internet connectivity\n"
            f"3. Ensure your API key has access to Gemini models\n"
            f"4. Update google-generativeai: pip install --upgrade google-generativeai\n"
            f"5. Check if you're behind a VPN or firewall blocking API access"
        )
    
    def generate(self, prompt, max_retries=3):
        """Generate content with retry logic."""
        for attempt in range(max_retries):
            try:
                response = self.model.generate_content(prompt)
                return response.text
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep((attempt + 1) * 2)
                else:
                    raise e
