import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import requests
import os
import time

# ------------------- 🎤 Step 1: Urdu Voice to Text -------------------
def get_urdu_voice():
    recognizer = sr.Recognizer()
    mic_list = sr.Microphone.list_microphone_names()
    print("🎤 Available Microphones:")
    for i, mic_name in enumerate(mic_list):
        print(f"{i}: {mic_name}")

    for mic_index, mic_name in enumerate(mic_list):
        if "Microphone" not in mic_name:
            continue  # Skip non-microphone devices

        print(f"\n🎙️ Trying microphone index {mic_index}: {mic_name}")
        try:
            with sr.Microphone(device_index=mic_index) as source:
                recognizer.adjust_for_ambient_noise(source, duration=1)
                print("📡 Listening for Urdu speech...")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)

            with open("urdu_input.wav", "wb") as f:
                f.write(audio.get_wav_data())
            print("💾 Saved input audio as 'urdu_input.wav'")

            if os.name == 'nt':
                os.system("start urdu_input.wav")

            print("🔍 Recognizing speech...")
            urdu_text = recognizer.recognize_google(audio, language="ur-PK")
            print("✅ Urdu Text Detected:", urdu_text)
            return urdu_text  # ✅ Return as soon as one mic works

        except sr.UnknownValueError:
            print("⚠️ Could not understand audio.")
        except sr.WaitTimeoutError:
            print("⏰ Timed out, no speech detected.")
        except Exception as e:
            print(f"❌ Error with mic {mic_index}: {e}")

    print("❌ No microphone was able to capture valid Urdu speech.")
    return ""

# ------------------- 🌐 Step 2: Translate Urdu to English -------------------
def translate_to_english(urdu_text):
    translator = Translator()
    try:
        translated = translator.translate(urdu_text, src='ur', dest='en')
        print("🌐 English Translation:", translated.text)
        return translated.text
    except Exception as e:
        print(f"❌ Translation Error: {e}")
        return urdu_text

# ------------------- 🧠 Step 3: Ask GPT via OpenRouter (Free Model) -------------------
def ask_gpt(question):
    print("🤖 Asking GPT via OpenRouter (free model)...")
    try:
        headers = {
            "Authorization": "Bearer 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",
            "Content-Type": "application/json"
        }
        data = {
            "model": "mistralai/mistral-7b-instruct",  # ✅ Free model
            "messages": [{"role": "user", "content": question}],
            "temperature": 0.7
        }

        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        response.raise_for_status()
        answer = response.json()["choices"][0]["message"]["content"].strip()
        print("🧠 GPT Answer:", answer)
        return answer
    except Exception as e:
        print("❌ GPT Error:", e)
        return "I'm sorry, I couldn't get the answer right now."

# ------------------- 🔊 Step 4: Text to Speech (English) -------------------
def speak_text(text):
    print("🔊 Speaking...")
    try:
        tts = gTTS(text=text, lang='en')  # English output
        filename = "response.mp3"
        tts.save(filename)

        if os.name == 'nt':
            os.system(f'start {filename}')
        elif os.name == 'posix':
            os.system(f'afplay {filename}' if os.uname().sysname == 'Darwin' else f'xdg-open {filename}')
        time.sleep(3)
    except Exception as e:
        print(f"❌ TTS Error: {e}")

# ------------------- 🚀 Main Pipeline -------------------
def run_voice_assistant():
    urdu_text = get_urdu_voice()
    if urdu_text:
        english_input = translate_to_english(urdu_text)
        gpt_response = ask_gpt(english_input)
        speak_text(gpt_response)
    else:
        print("⚠️ No valid Urdu input detected.")

# ------------------- 🏁 Start -------------------
if __name__ == "__main__":
    while True:
        run_voice_assistant()
        again = input("\n🔁 Do you want to ask another question? (y/n): ")
        if again.lower() != 'y':
            print("👋 Exiting. Goodbye!")
            break
