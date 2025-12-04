import time
import requests
from django.conf import settings

# ----------------------------------
#   CONFIG
# ----------------------------------

HF_API_KEY = settings.HF_API_KEY
HF_API_URL = "https://router.huggingface.co"        # Updated REQUIRED URL
DEFAULT_SUMMARY_MODEL = settings.HF_SUMMARY_MODEL   # e.g. "facebook/bart-large-cnn"

HEADERS = {
    "Authorization": f"Bearer {HF_API_KEY}",
    "Content-Type": "application/json"
}


# ----------------------------------
#   INTERNAL REQUEST HELPER
# ----------------------------------

def _post(model_id, payload, retries=4, delay=2):
    """
    Robust API wrapper for HuggingFace Router:
    - automatic retry if model is loading or returns non-JSON (cold start)
    - returns parsed JSON OR a structured error dict
    """

    url = f"{HF_API_URL}/models/{model_id}"

    for attempt in range(1, retries + 1):
        try:
            response = requests.post(url, headers=HEADERS, json=payload, timeout=60)

            # Try to parse JSON
            try:
                data = response.json()
            except:
                # Non-JSON is VERY common on first cold start
                if attempt < retries:
                    time.sleep(delay)
                    continue
                return {"error": "non_json", "raw": response.text[:500]}

            # Check for HF "loading" messages
            if isinstance(data, dict) and "error" in data:
                msg = data["error"].lower()
                if "loading" in msg or "warming" in msg or "downloading" in msg:
                    # Model still loading — retry
                    if attempt < retries:
                        time.sleep(delay)
                        continue
                    return {"error": "loading", "details": data}

                return {"error": data["error"], "details": data}

            # SUCCESS
            return data

        except Exception as e:
            if attempt >= retries:
                return {"error": f"Request failed: {str(e)}"}
            time.sleep(delay)

    return {"error": "unknown_failure"}


# ----------------------------------
#   SUMMARIZATION
# ----------------------------------

def summarize_text(text, max_length=200, min_length=60):
    model = DEFAULT_SUMMARY_MODEL
    payload = {
        "inputs": text,
        "parameters": {
            "max_length": max_length,
            "min_length": min_length,
            "do_sample": False,
            "temperature": 0.3
        }
    }

    data = _post(model, payload)

    # Handle errors
    if isinstance(data, dict) and "error" in data:
        return f"[Summary Error: {data['error']}]"

    if isinstance(data, list) and "summary_text" in data[0]:
        return data[0]["summary_text"]

    return "[Summary unavailable: unexpected HuggingFace response]"


# ----------------------------------
#   KEY POINTS
# ----------------------------------

def extract_key_points(text):
    model = DEFAULT_SUMMARY_MODEL

    prompt = f"""
    Extract the 5 most important bullet points from the text below.
    • If the text is short or partially OCR-damaged, infer the meaning.
    • Each bullet point must be short, factual, and useful.
    • Do NOT echo the prompt.

    TEXT:
    {text}
    """

    data = _post(model, {"inputs": prompt})

    if isinstance(data, list) and "summary_text" in data[0]:
        return data[0]["summary_text"]

    return "Key points unavailable."


# ----------------------------------
#   FLASHCARDS (FLAN-T5)
# ----------------------------------

def generate_flashcards(text):
    model = "google/flan-t5-large"

    prompt = f"""
    You are a teacher. Create 5 high-quality educational flashcards based on the text below.

    Requirements:
    • Infer missing context if the OCR text is incomplete.
    • Questions should be meaningful + answerable.
    • Answers must be correct, concise, and directly related.
    • DO NOT output anything except flashcards.

    Format EXACTLY:

    Q: <question>
    A: <answer>
    ----

    TEXT:
    {text}
    """

    payload = {
        "inputs": prompt,
        "parameters": {"temperature": 0.7}
    }

    data = _post(model, payload)

    if isinstance(data, list) and "generated_text" in data[0]:
        return data[0]["generated_text"]

    return "Flashcards unavailable."


# ----------------------------------
#   MULTIPLE-CHOICE QUIZ (FLAN-T5)
# ----------------------------------

def generate_quiz(text):
    model = "google/flan-t5-large"

    prompt = f"""
    You are a tutor. Create 5 multiple-choice questions (A–D) based on the text.

    Rules:
    • Infer reasonable details if text is short or contains OCR errors.
    • All 4 answer choices must be plausible.
    • Provide the correct answer AFTER the choices.
    • Keep the questions educational.

    Format EXACTLY:

    Q: <question>
    A) <option>
    B) <option>
    C) <option>
    D) <option>
    Answer: <letter>
    ----

    TEXT:
    {text}
    """

    payload = {
        "inputs": prompt,
        "parameters": {"temperature": 0.6}
    }

    data = _post(model, payload)

    if isinstance(data, list) and "generated_text" in data[0]:
        return data[0]["generated_text"]

    return "Quiz generation unavailable."

