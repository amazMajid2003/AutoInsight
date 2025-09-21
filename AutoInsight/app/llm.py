import os
import json
import re
from typing import Dict, Optional
from dotenv import load_dotenv
from openai import OpenAI

from app.utils import deterministic_summary
from app.prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE

# --- ENVIRONMENT ---
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5-mini")  # Default to nano

client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

# --- HELPERS ---
def extract_json(text: str) -> Optional[dict]:
    """Extract JSON object from LLM response, ignoring markdown fences."""
    try:
        # Handle ```json fenced blocks
        m = re.search(r"```(?:json)?\n(.+?)```", text, re.S)
        if m:
            text = m.group(1)
        return json.loads(text)
    except Exception:
        try:
            # Fallback: first { ... } block
            first = text[text.index("{"): text.rindex("}") + 1]
            return json.loads(first)
        except Exception:
            return None

def generate_vin_summary(vehicle: Dict) -> Dict:
    """
    Generate VIN summary using GPT-5 Nano (via Responses API).
    Falls back to deterministic scoring if:
      - API key missing
      - LLM call fails
      - JSON parsing fails
    """
    if not OPENAI_API_KEY or client is None:
        print("⚠️ Fallback: No API key or client initialized")
        result = deterministic_summary(vehicle)
        result["source"] = "fallback"
        return result

    try:
        resp = client.responses.create(
            model=OPENAI_MODEL,
            input=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": USER_PROMPT_TEMPLATE.format(vehicle_json=json.dumps(vehicle))},
            ],
        )

        # Extract generated text
        text = resp.output_text.strip() if resp.output_text else ""
        print("LLM raw output:", text)

        parsed = extract_json(text)

        if parsed and all(k in parsed for k in ["summary", "risk_score", "reasoning"]):
            try:
                parsed["risk_score"] = max(1.0, min(10.0, float(parsed["risk_score"])))

                # Normalize reasoning into a list (safe for printing)
                if isinstance(parsed["reasoning"], str):
                    parsed["reasoning"] = [
                        line.strip("-• ").strip()
                        for line in parsed["reasoning"].splitlines()
                        if line.strip()
                    ]

            except Exception:
                parsed["risk_score"] = 5  # neutral fallback

            parsed["vin"] = vehicle.get("VIN", "")
            parsed["source"] = "llm"

            return parsed

        print("⚠️ Fallback: Missing or invalid keys in LLM response")
        fallback = deterministic_summary(vehicle)
        fallback["source"] = "fallback"
        return fallback

    except Exception as e:
        print(f"⚠️ Exception during LLM call: {e}")
        fallback = deterministic_summary(vehicle)
        fallback["source"] = "fallback"
        return fallback
