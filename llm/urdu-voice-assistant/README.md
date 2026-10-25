# Urdu Voice Assistant

A complete speech-to-speech loop for Urdu speakers, in two flavours:

| Script | Pipeline |
| --- | --- |
| `urdu_to_english.py` | Urdu speech → English text → LLM answer → **English** speech |
| `urdu_to_urdu.py` | Urdu speech → English text → LLM answer → **Urdu** speech |

```
mic ──► Google STT (ur-PK) ──► translate ur→en ──► OpenRouter LLM
                                                        │
              speaker ◄── gTTS ◄── translate en→ur ◄─────┘   (urdu_to_urdu.py)
              speaker ◄── gTTS ◄──────────────────────────    (urdu_to_english.py)
```

## Why the English hop

The open-weight model used here is far stronger in English than in Urdu, so the
pipeline translates the question into English, reasons there, and translates the
answer back. `urdu_to_english.py` skips the last hop for users who are happy to hear
the reply in English.

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate          # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

Provide your OpenRouter key — it is read from the environment, never hardcoded:

```powershell
$env:OPENROUTER_API_KEY="sk-or-..."
python urdu_to_urdu.py
```

```bash
export OPENROUTER_API_KEY="sk-or-..."
python urdu_to_urdu.py
```

## Implementation notes

- **Microphone fallback:** it enumerates input devices and tries each one until Urdu
  speech is recognised, instead of assuming device 0 — which is why it works on
  laptops with multiple audio endpoints.
- Recognition uses Google's `ur-PK` locale; the captured WAV is saved so you can
  listen back to what was actually recorded.
- Every network call is wrapped with a graceful spoken fallback, so a failed
  translation or rate-limited model still produces audio instead of crashing.
- Replies are played with the OS-native handler per platform (`start` / `afplay` /
  `xdg-open`).

## Stack

`SpeechRecognition` · `googletrans` · `gTTS` · `requests` · OpenRouter
