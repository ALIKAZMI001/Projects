<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:6EE7F7,100:3B82F6&height=200&section=header&text=Ali%20Kazmi&fontSize=60&fontColor=ffffff&fontAlignY=38&desc=AI%20%26%20Machine%20Learning%20Portfolio&descAlignY=60&descSize=22&animation=fadeIn" width="100%"/>

<br/>

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-Keras-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)](https://tensorflow.org)
[![PyTorch](https://img.shields.io/badge/PyTorch-HuggingFace-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)](https://pytorch.org)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.x-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)](https://opencv.org)
[![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-00CFFF?style=for-the-badge)](https://ultralytics.com)
[![LangChain](https://img.shields.io/badge/LangChain-RAG-1C3C3C?style=for-the-badge)](https://langchain.com)
[![LiveKit](https://img.shields.io/badge/LiveKit-Voice%20Agent-00C2A8?style=for-the-badge)](https://livekit.io)

<br/>

> **10 end-to-end AI projects** spanning Computer Vision · LLMs · RAG · Real-time Voice Agents — all runnable Python, all production-structured.

</div>

---

## 🗂️ Project Map

```
Projects
├── 👁️  computer-vision/         6 real-time CV systems
├── 🧠  llm/                     3 language model projects
└── 🤖  ai-agents/               1 live voice agent
```

---

## 👁️ Computer Vision

<table>
<tr>
<td width="50%">

### 🎂 Age & Gender Estimation
> Real-time two-head CNN — predicts **age + gender** from webcam feed

- Custom CNN with shared backbone, dual output heads
- Trained on IMDB-WIKI face crops
- Live inference on webcam at 30 FPS

**Stack:** `TensorFlow` `Keras` `OpenCV`

[📁 View Project →](computer-vision/age-gender-estimation)

</td>
<td width="50%">

### 🎯 YOLOv8 Face Detection
> Fine-tuned **YOLOv8n** on a self-captured face dataset

- Custom dataset captured with MediaPipe landmark detection
- Fine-tuned YOLOv8 nano — fast & accurate
- Runs predict on images or webcam stream

**Stack:** `Ultralytics YOLOv8` `MediaPipe`

[📁 View Project →](computer-vision/yolo-face-detection)

</td>
</tr>
<tr>
<td width="50%">

### 🪪 Face Recognition
> Two ML approaches behind a **Tkinter desktop app**

- **CNN approach:** Keras classifier trained on face crops
- **KNN approach:** scikit-learn baseline for comparison
- Side-by-side comparison of both methods

**Stack:** `Keras` `scikit-learn` `Tkinter` `OpenCV`

[📁 View Project →](computer-vision/face-recognition)

</td>
<td width="50%">

### 🙌 Gesture Attendance
> Mark attendance with a **thumbs-up or thumbs-down** gesture

- MediaPipe hand landmark detection
- Gesture → Excel (openpyxl) in real time
- Works with 10–20 students per session

**Stack:** `MediaPipe` `OpenCV` `openpyxl`

[📁 View Project →](computer-vision/gesture-attendance)

</td>
</tr>
<tr>
<td width="50%">

### 🖱️ Virtual Mouse
> Control your **cursor and clicks** with your hand — no hardware

- Pinch gesture = click, index finger = cursor
- Smooth tracking with velocity damping
- Works on any webcam

**Stack:** `MediaPipe` `PyAutoGUI` `OpenCV`

[📁 View Project →](computer-vision/virtual-mouse)

</td>
<td width="50%">

### 🎮 Gesture Game Control
> Play a **Unity game** entirely with hand gestures

- Open/close hand → jump / crouch / move
- Real-time gesture classification from webcam
- Bundled Unity WebGL build included

**Stack:** `MediaPipe` `PyAutoGUI` `Unity`

[📁 View Project →](computer-vision/gesture-game-control)

</td>
</tr>
</table>

---

## 🧠 Language Models & Speech

<table>
<tr>
<td width="33%">

### 🏏 LLM Fine-tuning
> Fine-tune **BERT & T5** from scratch

- BERT on GLUE/MRPC sentence-pair task
- T5 → Cricket Q&A chatbot (custom dataset)
- Full training loop in Jupyter notebooks

**Stack:** `HuggingFace Transformers` `PyTorch`

[📁 View Project →](llm/llm-finetuning)

</td>
<td width="33%">

### 🎙️ Urdu Voice Assistant
> Full **speech-to-speech** loop in Urdu

- Urdu speech → STT → LLM → TTS → speaker
- Two modes: reply in English or back in Urdu
- Microphone fallback across audio devices

**Stack:** `SpeechRecognition` `gTTS` `OpenRouter`

[📁 View Project →](llm/urdu-voice-assistant)

</td>
<td width="33%">

### 📄 RAG PDF Chatbot
> Ask questions about **any PDF** document

- Chunks PDF → embeds → Qdrant vector store
- Retrieves top-3 chunks → grounded LLM answer
- Refuses to hallucinate outside the document

**Stack:** `LangChain` `Qdrant` `sentence-transformers`

[📁 View Project →](llm/rag-pdf-chatbot)

</td>
</tr>
</table>

---

## 🤖 AI Agents

<table>
<tr>
<td>

### ✈️ LiveKit Trip Planning Agent
> A **real-time voice AI** that plans your entire trip in a conversation

Talk to it like a person. It pulls live data and plans your trip on the fly:

| Capability | API |
|---|---|
| 🌤️ Live weather at destination | Geoapify |
| 📍 Hotels, attractions, restaurants | Geoapify Places |
| ✈️ Real-time flight search | RapidAPI Flights |
| 🎫 Booking simulation | Built-in |

- Ultra-low latency voice: **LiveKit + Groq (LLaMA 3)** for STT/LLM, **Cartesia** for TTS
- Dockerized — one command to run
- Netlify web console for browser-based voice sessions

**Stack:** `LiveKit Agents` `Groq` `Cartesia` `Geoapify` `Docker`

[📁 View Project →](ai-agents/livekit-trip-agent)

</td>
</tr>
</table>

---

## 🚀 Getting Started

Every project is fully self-contained. General pattern:

```bash
# 1. Enter any project folder
cd computer-vision/age-gender-estimation

# 2. Create & activate virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run
python predict_webcam.py
```

For projects with API keys — copy `.env.example` → `.env` and fill in your keys. **No secrets are committed to this repo.**

---

## 📁 Full Repository Layout

```
.
├── computer-vision/
│   ├── age-gender-estimation/     # trained models + webcam inference
│   ├── yolo-face-detection/       # fine-tuned YOLOv8n + dataset
│   ├── face-recognition/          # cnn/ and knn/ + desktop app
│   ├── gesture-attendance/        # MediaPipe + Excel automation
│   ├── virtual-mouse/             # gesture-driven cursor control
│   └── gesture-game-control/      # hand gesture → Unity game
├── llm/
│   ├── llm-finetuning/            # BERT & T5 training notebooks
│   ├── urdu-voice-assistant/      # Urdu speech ↔ LLM ↔ speech
│   └── rag-pdf-chatbot/           # retrieval-augmented Q&A over PDF
├── ai-agents/
│   └── livekit-trip-agent/        # real-time voice travel agent
└── .github/workflows/             # CI: syntax-checks all Python files
```

---

## 🛠️ Tech Stack Overview

| Domain | Technologies |
|---|---|
| **Computer Vision** | OpenCV, MediaPipe, TensorFlow/Keras, Ultralytics YOLOv8 |
| **ML / Training** | PyTorch, HuggingFace Transformers, scikit-learn |
| **LLMs & RAG** | LangChain, Qdrant, sentence-transformers, OpenRouter |
| **Voice & Agents** | LiveKit Agents, Groq, Cartesia TTS |
| **Tooling** | Docker, GitHub Actions CI, python-dotenv |

---

<div align="center">

## 📬 Connect

[![GitHub](https://img.shields.io/badge/GitHub-ALIKAZMI001-181717?style=for-the-badge&logo=github)](https://github.com/ALIKAZMI001)

<br/>

**If any project helped you, a ⭐ star goes a long way!**

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:3B82F6,100:6EE7F7&height=100&section=footer" width="100%"/>

</div>
