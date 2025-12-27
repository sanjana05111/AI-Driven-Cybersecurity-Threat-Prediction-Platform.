import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()


class StorageService:
    def __init__(self):
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_KEY")
        self.client: Client = None

        if self.url and self.key:
            try:
                self.client = create_client(self.url, self.key)
            except Exception as e:
                print(f"Supabase Connection Error: {e}")

    def save_analysis(self, data: dict):
        """
        Save analysis results to Supabase.
        Matches the analysis_results table schema exactly.
        """
        if not self.client:
            print("Supabase client not initialized")
            return None

        try:
            record = {
                "filename": data.get("filename", "UNKNOWN"),
                "risk_score": data.get("risk_score", 0),
                "summary": data.get("summary", ""),
                "source": data.get("source", "AI"),
                "details": {
                    # Explainable AI fields
                    "verdict": data.get("verdict"),
                    "confidence": data.get("confidence"),
                    "why_flagged": data.get("why_flagged"),
                    "threats": data.get("threats"),

                    # Optional deeper data
                    "technical_details": data.get("technical_details"),
                    "packet_intelligence": data.get("intelligence"),
                }
            }

            return self.client.table("analysis_results").insert(record).execute()

        except Exception as e:
            print(f"Error saving to Supabase: {e}")
            return None


storage_service = StorageService()
