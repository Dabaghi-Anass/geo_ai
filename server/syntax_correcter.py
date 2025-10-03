import os
import requests

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

GEMINI_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

def correct_syntax(text: str) -> str:
    """
    Calls Gemini 2.0 to correct the syntax of the given text.
    Returns the corrected text on success, or raises on error.
    """
    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": GEMINI_API_KEY
    }

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": (
                            "You are a syntax and grammar correcter. "
                            "Correct the following sentence, generate text format with one single suggestion that is grammatically and syntaxically and lexically correct, respond only with the suggestion:\n\n"
                            f"{text}"
                        )
                    }
                ]
            }
        ]
    }

    resp = requests.post(GEMINI_ENDPOINT, json=payload, headers=headers)
    resp.raise_for_status()
    data = resp.json()

    return data["candidates"][0]["content"]["parts"][0]["text"]
