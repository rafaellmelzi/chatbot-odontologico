import httpx


class ChatbotService:
    def __init__(self):
        self.api_key = "AIzaSyDWSTxEkYXUOBNKGlwltbbZepz94osZRJo"
        self.url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-001:generateContent"
    
    async def generate_response(self, message: str) -> str:
        try:
            payload = {
                "contents": [{
                    "parts": [{"text": message}]
                }],
                "generationConfig": {
                    "temperature": 0.7,
                    "maxOutputTokens": 200
                }
            }
            
            url_with_key = f"{self.url}?key={self.api_key}"
            
            async with httpx.AsyncClient(timeout=30) as client:
                resp = await client.post(url_with_key, json=payload)
                
                if resp.status_code != 200:
                    return f"Erro: {resp.status_code}"
                
                data = resp.json()
                text = data["candidates"][0]["content"]["parts"][0]["text"]
                return text.strip()
        
        except Exception as e:
            return f"Erro: {str(e)}"


chatbot_service = ChatbotService()
