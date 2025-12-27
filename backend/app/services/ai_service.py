import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()


class AIService:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model = None
        if self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel("gemini-2.5-flash")
            except Exception as e:
                print(f"AI Service Error: {e}")

    # -------------------------------------------------
    # FILE / TEXT ANALYSIS (Explainable)
    # -------------------------------------------------
    async def analyze_text(self, text: str, filename: str):
        if not self.model:
            return self._mock_response()

        prompt = f"""
        Analyze the following file content for cybersecurity threats.

        Filename: {filename}
        Content (truncated):
        {text[:8000]}

        Respond ONLY in valid JSON (no markdown, no backticks):
        {{
            "risk_score": (integer 0-100),
            "summary": "Brief executive summary",
            "threats": ["list", "of", "specific", "threats"],
            "why_flagged": "Explain why this content is risky",
            "confidence": (float between 0 and 1)
        }}
        """

        try:
            response = self.model.generate_content(prompt)
            clean = response.text.replace("```json", "").replace("```", "").strip()
            ai_data = json.loads(clean)
            return self._finalize(ai_data)
        except Exception as e:
            print(f"Gemini Analysis Failed: {e}")
            return self._mock_response()

    # -------------------------------------------------
    # QR TEXT ANALYSIS
    # -------------------------------------------------
    async def analyze_qr_content(self, content: str):
        if not self.model:
            return self._mock_response()

        prompt = f"""
        Analyze the following QR-decoded content for security threats.

        Content: "{content}"

        Respond ONLY in valid JSON:
        {{
            "risk_score": (integer 0-100),
            "summary": "Analysis summary",
            "threats": ["list of threats"],
            "why_flagged": "Reason for classification",
            "confidence": (float between 0 and 1)
        }}
        """

        try:
            response = self.model.generate_content(prompt)
            clean = response.text.replace("```json", "").replace("```", "").strip()
            return self._finalize(json.loads(clean))
        except Exception as e:
            print(f"Gemini QR Text Analysis Failed: {e}")
            return self._mock_response()

    # -------------------------------------------------
    # IMAGE / QR IMAGE ANALYSIS
    # -------------------------------------------------
    async def analyze_image(self, image_bytes: bytes, mime_type: str):
        if not self.model:
            return self._mock_response()

        prompt = """
        Analyze this image for cybersecurity threats.
        If a QR code is present, extract and analyze its content.

        Respond ONLY in valid JSON:
        {
            "risk_score": (integer 0-100),
            "summary": "Image and QR analysis",
            "threats": ["list of threats"],
            "why_flagged": "Reason for classification",
            "confidence": (float between 0 and 1)
        }
        """

        try:
            image_part = {"mime_type": mime_type, "data": image_bytes}
            response = self.model.generate_content([prompt, image_part])
            clean = response.text.replace("```json", "").replace("```", "").strip()
            return self._finalize(json.loads(clean))
        except Exception as e:
            print(f"Gemini Image Analysis Failed: {e}")
            return self._mock_response()

    # -------------------------------------------------
    # CHAT (unchanged, safe)
    # -------------------------------------------------
    def chat(self, message: str, context: str = ""):
        if not self.model:
            return "SIMBA (Offline): AI Core is not connected. Check API Key."

        try:
            prompt = f"""
            System Context: {context}
            User: {message}

            Act as SIMBA, a cybersecurity expert AI.
            Be concise, technical, and helpful.
            """
            res = self.model.generate_content(prompt)
            return res.text
        except Exception as e:
            return f"Error: {str(e)}"

    # -------------------------------------------------
    # FINAL DECISION LOGIC (Explainable)
    # -------------------------------------------------
    def _finalize(self, ai_data: dict):
        score = int(ai_data.get("risk_score", 0))

        if score >= 70:
            verdict = "Malicious"
        elif score >= 40:
            verdict = "Suspicious"
        else:
            verdict = "Normal"

        return {
            "risk_score": score,
            "summary": ai_data.get("summary", ""),
            "threats": ai_data.get("threats", []),
            "why_flagged": ai_data.get("why_flagged", "Heuristic + AI assessment"),
            "confidence": round(float(ai_data.get("confidence", 0.7)), 2),
            "verdict": verdict
        }

    # -------------------------------------------------
    # MOCK MODE (Offline / API failure)
    # -------------------------------------------------
    def _mock_response(self):
        return {
            "risk_score": 55,
            "summary": "AI operating in mock mode. Potentially suspicious patterns detected.",
            "threats": ["Obfuscation Detected", "Unknown Source"],
            "why_flagged": "Pattern similarity to known malicious payloads",
            "confidence": 0.65,
            "verdict": "Suspicious"
        }


ai_service = AIService()
