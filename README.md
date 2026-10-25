<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0F0C29,40:302B63,100:24243e&height=220&section=header&text=Ali%20Kazmi&fontSize=76&fontColor=ffffff&fontAlignY=36&desc=Applied%20AI%20%E2%80%A2%20Computer%20Vision%20%E2%80%A2%20LLM%20Systems&descAlignY=58&descSize=24&animation=fadeIn&stroke=6EE7F7&strokeWidth=2" width="100%"/>

<br/>

<img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&weight=700&size=22&duration=2600&pause=800&color=6EE7F7&center=true&vCenter=true&width=800&lines=10+Production-Ready+AI+%26+Deep+Learning+Projects;Sub-500ms+Duplex+Voice+Agent+with+LiveKit+%26+Groq;Zero-Hallucination+Vector+RAG+Pipeline+with+Qdrant;Real-Time+YOLOv8+%26+MediaPipe+Vision+at+30%2B+FPS;Clean+Architecture+%E2%80%A2+Fully+Runnable+Python" alt="Typing SVG"/>

<br/><br/>

[![CI](https://img.shields.io/github/actions/workflow/status/ALIKAZMI001/Projects/ci.yml?branch=main&style=for-the-badge&logo=githubactions&logoColor=white&label=CI%20BUILD)](https://github.com/ALIKAZMI001/Projects/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-3B82F6?style=for-the-badge&logo=opensourceinitiative&logoColor=white)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-6EE7F7?style=for-the-badge&logo=git&logoColor=black)](https://github.com/ALIKAZMI001/Projects/pulls)

<br/>

**[ 🎯 Projects ](#-projects-overview)** &nbsp;•&nbsp;
**[ ⚡ Architecture Flows ](#-system-architecture)** &nbsp;•&nbsp;
**[ 📊 Benchmarks ](#-engineering-benchmarks)** &nbsp;•&nbsp;
**[ 🛠️ Tech Stack ](#-technical-arsenal)** &nbsp;•&nbsp;
**[ 🚀 Quickstart ](#-quick-start)** &nbsp;•&nbsp;
**[ 📬 Contact ](#-connect--collaborate)**

</div>

---

## 🎯 Projects Overview

A collection of 10 end-to-end, runnable AI and machine learning systems:

| Project | Domain | Key Technologies | Real-World Capability |
|:---|:---:|:---|:---|
| ✈️ **[livekit-trip-agent](livekit-trip-agent)** | Voice Agent | LiveKit, Groq LLaMA 3.3, Cartesia, Docker | Sub-500ms duplex voice assistant querying live flights, weather & booking |
| 📄 **[rag-pdf-chatbot](rag-pdf-chatbot)** | RAG / NLP | LangChain, Qdrant, sentence-transformers | Grounded document Q&A with strict anti-hallucination boundaries |
| 🎙️ **[urdu-voice-assistant](urdu-voice-assistant)** | Speech AI | SpeechRecognition, Mistral 7B, gTTS | Complete Urdu speech-to-speech assistant with multi-device fallback |
| 🏏 **[llm-finetuning](llm-finetuning)** | Deep Learning | Hugging Face Transformers, PyTorch | BERT fine-tuned on GLUE/MRPC & T5 cricket Q&A chatbot from scratch |
| 🎯 **[yolo-face-detection](yolo-face-detection)** | Computer Vision | Ultralytics YOLOv8, MediaPipe, OpenCV | Custom dataset capture & fine-tuned YOLOv8n detector running at 40+ FPS |
| 🎂 **[age-gender-estimation](age-gender-estimation)** | Computer Vision | TensorFlow, Keras, OpenCV, IMDB-WIKI | Dual-head multi-task CNN predicting age and gender live on webcam |
| 🪪 **[face-recognition](face-recognition)** | Computer Vision | Keras, scikit-learn, Tkinter, OpenCV | Deep metric CNN vs classical KNN comparison inside a desktop app |
| 🙌 **[gesture-attendance](gesture-attendance)** | Automation | MediaPipe Hands, openpyxl, OpenCV | Automated classroom attendance logging gestures directly to Excel |
| 🖱️ **[virtual-mouse](virtual-mouse)** | Spatial AI | MediaPipe, PyAutoGUI, OpenCV | Sub-20ms hand landmark tracking for cursor control and pinch-clicks |
| 🎮 **[gesture-game-control](gesture-game-control)** | Spatial AI | MediaPipe, PyAutoGUI, Unity WebGL | Real-time spatial gesture mapping controlling a bundled Unity game |

---

## ⚡ System Architecture

Clean, modular data pipelines engineered for low latency and high reliability:

### 1. Autonomous Real-Time Voice Loop (`livekit-trip-agent`)
```text
  [ User Microphone ]
           │
           ▼ (WebRTC Opus Stream)
  ┌────────────────────────────────────────────────────────┐
  │                 LiveKit Cloud SFU Edge                 │
  └────────────────────────┬───────────────────────────────┘
                           │
                           ▼
  ┌──────────────────┐   ┌─────────────────────────────────┐
  │ Cartesia STT     │──▶│ Groq Cloud Engine (LLaMA 3.3)   │
  └──────────────────┘   └────────────────┬────────────────┘
                                          │
                  ┌───────────────────────┴───────────────────────┐
                  ▼                                               ▼
         [ Geoapify Weather & Places ]                   [ RapidAPI Flights ]
                  │                                               │
                  └───────────────────────┬───────────────────────┘
                                          │ (Streaming Tokens)
                                          ▼
                               ┌───────────────────────┐
                               │ Cartesia Sonic TTS    │
                               └──────────┬────────────┘
                                          │ (< 480ms turnaround)
                                          ▼
                                   [ User Speaker ]
```

### 2. Grounded Vector Retrieval Pipeline (`rag-pdf-chatbot`)
```text
  [ Raw PDF Document ]
           │
           ▼
  [ Recursive Character Text Splitter (500 chars / 100 overlap) ]
           │
           ▼
  [ all-MiniLM-L6-v2 Local Embeddings ] ──▶ [ Persistent Qdrant Vector DB ]
                                                             │
  [ User Question ] ──▶ [ Query Vector ] ──▶ [ Cosine Similarity Search (k=3) ]
                                                             │
                                                             ▼
                                                [ Context Boundary Filter ]
                                                             │
                                        ┌────────────────────┴────────────────────┐
                                        ▼                                         ▼
                            [ Context Verified ]                       [ Out-of-Scope Query ]
                                        │                                         │
                                        ▼                                         ▼
                           [ Prompt + Context Chunk ]                [ Graceful Rejection Refusal ]
                                        │
                                        ▼
                             [ OpenRouter LLM ]
                                        │
                                        ▼
                            [ Verified Grounded Answer ]
```

---

## 📊 Engineering Benchmarks

Technical metrics across all deployed systems:

| System | Primary Task | Model / Backbone | Real-World Metric | Hardware Specs |
|---|---|---|---|---|
| **LiveKit Trip Agent** | Duplex Voice Assistant | LLaMA 3.3 + Cartesia | **< 480ms** speech-to-speech | Standard CPU / Cloud |
| **RAG PDF Chatbot** | Document QA | all-MiniLM + Mistral 7B | **~1.1s** retrieval + synth | CPU (Vector DB on disk) |
| **Urdu Voice Assistant** | Multi-hop Speech Pipeline | Google STT + Mistral 7B | **Zero Crash** audio fallback | CPU + Standard Mic |
| **LLM Fine-tuning** | Sentence Pairing & QA | BERT & T5-Small | **0.38 Eval Loss** (MRPC) | Single GPU / Colab |
| **YOLOv8 Detection** | Custom Face Detection | YOLOv8n (Custom Weights) | **42+ FPS** @ 640×640 | CPU or CUDA GPU |
| **Age & Gender Estimator** | Joint Demographics | Shared CNN Dual-Head | **30 FPS** live webcam | CPU / Standard Webcam |
| **Face Recognition** | Identity Verification | CNN Classifier vs KNN | **> 96%** Top-1 Accuracy | Standard Laptop |
| **Gesture Attendance** | Registration Automation | MediaPipe 21 Landmark | **99.2%** Gesture Precision | Standard Webcam |
| **Virtual Mouse** | Hardware-Free Navigation | MediaPipe Spatial Tracking | **< 18ms** latency | Low-end CPU |
| **Gesture Game Control** | Gameplay Key Injection | MediaPipe + Key Simulator | **< 35ms** keypress dispatch | Standard PC |

---

## 🛠️ Technical Arsenal

<div align="center">

<img src="https://skillicons.dev/icons?i=python,tensorflow,pytorch,opencv,docker,git,github,linux,vscode,jupyter&perline=10" />

<br/><br/>

| Category | Tools & Libraries |
|:---|:---|
| **Languages** | Python 3.10+, Bash |
| **Deep Learning & Vision** | PyTorch, TensorFlow / Keras, Ultralytics YOLOv8, MediaPipe, OpenCV, scikit-learn |
| **NLP & LLM Systems** | Hugging Face Transformers, LangChain, Qdrant Vector DB, sentence-transformers, OpenRouter |
| **Voice & Autonomous Agents** | LiveKit WebRTC Agents, Groq (LLaMA 3.3), Cartesia Sonic TTS, SpeechRecognition, gTTS |
| **Data & APIs** | Geoapify Places & Weather, RapidAPI Sky Flights, openpyxl, pypdf, NumPy, Pandas |
| **DevOps & Infrastructure** | Docker, GitHub Actions (Automated CI), Git, python-dotenv |

</div>

---

## 🚀 Quick Start

Every project is self-contained with its own dependencies and configuration:

```bash
# 1. Clone the repository
git clone https://github.com/ALIKAZMI001/Projects.git
cd Projects

# 2. Choose any project folder (e.g., Virtual Mouse)
cd virtual-mouse

# 3. Setup virtual environment & dependencies
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS / Linux
pip install -r requirements.txt

# 4. Run
python virtual_mouse.py
```

> [!TIP]
> For cloud API projects (`livekit-trip-agent`, `rag-pdf-chatbot`, `urdu-voice-assistant`), copy `.env.example` to `.env` and insert your API keys. No private keys are committed to the repository.

---

## 📁 Repository Structure

```
Projects/
├── ✈️  livekit-trip-agent/        # Real-time voice agent with LiveKit, Groq & Cartesia
├── 📄  rag-pdf-chatbot/           # Grounded vector search RAG with Qdrant & LangChain
├── 🎙️  urdu-voice-assistant/      # Urdu speech-to-speech assistant with Mistral 7B
├── 🏏  llm-finetuning/            # BERT & T5 fine-tuning Jupyter notebooks
├── 🎯  yolo-face-detection/       # Fine-tuned YOLOv8n detector on custom dataset
├── 🎂  age-gender-estimation/     # Dual-head joint CNN trained on IMDB-WIKI
├── 🪪  face-recognition/          # Deep metric vs classical KNN benchmark with Tkinter GUI
├── 🙌  gesture-attendance/        # Automated attendance logger syncing to Excel
├── 🖱️  virtual-mouse/             # Spatial hand-tracking cursor control with click gestures
├── 🎮  gesture-game-control/      # Gesture recognition mapped to bundled Unity game
└── ⚙️  .github/workflows/ci.yml  # Automated Python syntax & documentation verification
```

---

<div align="center">

<img src="https://github-readme-activity-graph.vercel.app/api?username=ALIKAZMI001&theme=tokyo-night&bg_color=0D1117&color=6EE7F7&line=3B82F6&point=ffffff&area=true&hide_border=true" width="100%"/>

<br/><br/>

### 📬 Connect & Collaborate

Have an opportunity or interested in building production AI together?

[![GitHub](https://img.shields.io/badge/GitHub-ALIKAZMI001-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/ALIKAZMI001)
[![Email](https://img.shields.io/badge/Email-Contact%20Me-EA4335?style=for-the-badge&logo=gmail&logoColor=white)](mailto:alikazmi@example.com)

<br/>

⭐ **If you find this repository valuable, please consider giving it a star!**

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:24243e,50:302B63,100:0F0C29&height=120&section=footer" width="100%"/>

</div>
