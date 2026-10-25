"""Urdu speech → English reasoning → Urdu speech.

Pipeline: microphone → Google STT (ur-PK) → translate to English → OpenRouter
LLM → translate the answer back to Urdu → gTTS (ur).

Setup:
    pip install -r requirements.txt
    set OPENROUTER_API_KEY=sk-or-...        (PowerShell: $env:OPENROUTER_API_KEY="...")

Run:  python urdu_to_urdu.py
"""

import os
import time

import requests
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "mistralai/mistral-7b-instruct"
INPUT_AUDIO = "urdu_input.wav"
OUTPUT_AUDIO = "response.mp3"


def get_urdu_voice() -> str:
    """Listen on every available microphone until Urdu speech is recognised."""
    recognizer = sr.Recognizer()
    mic_list = sr.Microphone.list_microphone_names()

    print("Available microphones:")
    for i, mic_name in enumerate(mic_list):
        print(f"  {i}: {mic_name}")

    for mic_index, mic_name in enumerate(mic_list):
        if "Microphone" not in mic_name:
            continue

        print(f"\nTrying microphone {mic_index}: {mic_name}")
        try:
            with sr.Microphone(device_index=mic_index) as source:
                recognizer.adjust_for_ambient_noise(source, duration=1)
                print("Listening for Urdu speech...")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)

            with open(INPUT_AUDIO, "wb") as f:
                f.write(audio.get_wav_data())

            if os.name == "nt":
                os.system(f"start {INPUT_AUDIO}")

            urdu_text = recognizer.recognize_google(audio, language="ur-PK")
            print("Urdu text:", urdu_text)
            return urdu_text

        except sr.UnknownValueError:
            print("Could not understand the audio.")
        except sr.WaitTimeoutError:
            print("Timed out — no speech detected.")
        except Exception as exc:  # noqa: BLE001 - try the next device
            print(f"Microphone {mic_index} failed: {exc}")

    print("No microphone captured valid Urdu speech.")
    return ""


def translate(text: str, source: str, target: str) -> str:
    try:
        translated = Translator().translate(text, src=source, dest=target)
        return translated.text
    except Exception as exc:  # noqa: BLE001 - fall back to the original text
        print(f"Translation error: {exc}")
        return text


def ask_llm(question: str) -> str:
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise SystemExit("Set OPENROUTER_API_KEY before running this script.")

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": question}],
        "temperature": 0.7,
    }

    try:
        response = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()
    except Exception as exc:  # noqa: BLE001 - spoken fallback message
        print(f"LLM error: {exc}")
        return "I'm sorry, I couldn't get the answer right now."


def speak(text: str, lang: str = "ur") -> None:
    try:
        tts = gTTS(text=text, lang=lang)
        tts.save(OUTPUT_AUDIO)

        if os.name == "nt":
            os.system(f"start {OUTPUT_AUDIO}")
        elif os.name == "posix":
            os.system(f"afplay {OUTPUT_AUDIO}" if os.uname().sysname == "Darwin"
                      else f"xdg-open {OUTPUT_AUDIO}")
        time.sleep(3)
    except Exception as exc:  # noqa: BLE001 - TTS is best-effort
        print(f"TTS error: {exc}")


def run_voice_assistant() -> None:
    urdu_text = get_urdu_voice()
    if not urdu_text:
        print("No valid Urdu input detected.")
        return

    english_input = translate(urdu_text, "ur", "en")
    print("English translation:", english_input)

    answer_en = ask_llm(english_input)
    print("Answer (English):", answer_en)

    answer_ur = translate(answer_en, "en", "ur")
    print("Answer (Urdu):", answer_ur)
    speak(answer_ur, lang="ur")


if __name__ == "__main__":
    while True:
        run_voice_assistant()
        if input("\nAsk another question? (y/n): ").strip().lower() != "y":
            print("Goodbye!")
            break
