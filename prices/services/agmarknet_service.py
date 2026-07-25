import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("AGMARKNET_API_KEY")

RESOURCE_ID = "9ef84268-d588-465a-a308-a864a43d0070"
BASE_URL = f"https://api.data.gov.in/resource/{RESOURCE_ID}"


class AgmarknetService:

    @staticmethod
    def get_today_prices(
        state="Maharashtra",
        limit=10,
        offset=0,
    ):
        if not API_KEY:
            raise ValueError(
                "AGMARKNET_API_KEY not found in .env file."
            )

        # Request parameters
        params = {
            "api-key": API_KEY,
            "format": "json",
            "limit": limit,
            "offset": offset,
            "filters[state.keyword]": state,
        }

        
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json",
        }
        
        response = requests.get(
            BASE_URL,
            params=params,
            headers=headers,
            timeout=120,
        )

        if response.status_code != 200:
            print("Status Code:", response.status_code)
            print("Response:", response.text)
            return []

        data = response.json()

        return data.get("records", [])
    