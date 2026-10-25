<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0F0C29,50:302B63,100:24243e&height=220&section=header&text=Ali%20Kazmi&fontSize=72&fontColor=ffffff&fontAlignY=38&desc=AI%20%26%20Machine%20Learning%20Portfolio&descAlignY=60&descSize=26&animation=fadeIn&stroke=6EE7F7&strokeWidth=2" width="100%"/>

<br/>

<img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&weight=700&size=24&duration=3000&pause=1000&color=6EE7F7&center=true&vCenter=true&width=700&lines=10+End-to-End+AI+Projects;Computer+Vision+%7C+LLMs+%7C+RAG+%7C+Voice+Agents;Real+code.+Real+models.+Real+results." alt="Typing SVG" />

<br/><br/>

<a href="computer-vision"><img src="https://img.shields.io/badge/Computer%20Vision-6%20Projects-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white"/></a>
<a href="llm"><img src="https://img.shields.io/badge/LLMs%20%26%20Speech-3%20Projects-FF6F00?style=for-the-badge&logo=huggingface&logoColor=white"/></a>
<a href="ai-agents"><img src="https://img.shields.io/badge/AI%20Agents-1%20Project-00C2A8?style=for-the-badge&logo=livekit&logoColor=white"/></a>

<br/><br/>

[![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-FF6F00?style=flat-square&logo=tensorflow&logoColor=white)](https://tensorflow.org)
[![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=flat-square&logo=pytorch&logoColor=white)](https://pytorch.org)
[![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=flat-square&logo=opencv&logoColor=white)](https://opencv.org)
[![HuggingFace](https://img.shields.io/badge/🤗%20HuggingFace-FFD21F?style=flat-square&logoColor=black)](https://huggingface.co)
[![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=flat-square)](https://langchain.com)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)](https://docker.com)
[![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-2088FF?style=flat-square&logo=githubactions&logoColor=white)](https://github.com/features/actions)

</div>

---

<div align="center">

## 🗺️ Portfolio at a Glance

| # | Project | Category | Key Tech | Highlight |
|---|---------|----------|----------|-----------|
| 01 | [Age & Gender Estimation](#-01--age--gender-estimation) | 👁️ Computer Vision | TensorFlow, Keras, OpenCV | Dual-head CNN, live webcam |
| 02 | [YOLOv8 Face Detection](#-02--yolov8-face-detection) | 👁️ Computer Vision | Ultralytics, MediaPipe | Self-captured dataset + fine-tuned model |
| 03 | [Face Recognition](#-03--face-recognition) | 👁️ Computer Vision | Keras, scikit-learn | CNN vs KNN comparison + desktop app |
| 04 | [Gesture Attendance](#-04--gesture-attendance) | 👁️ Computer Vision | MediaPipe, openpyxl | Thumbs-up/down → Excel |
| 05 | [Virtual Mouse](#-05--virtual-mouse) | 👁️ Computer Vision | MediaPipe, PyAutoGUI | Hand = cursor, no hardware |
| 06 | [Gesture Game Control](#-06--gesture-game-control) | 👁️ Computer Vision | MediaPipe, Unity | Play a game with your hands |
| 07 | [LLM Fine-tuning](#-07--llm-fine-tuning) | 🧠 LLMs | HuggingFace, PyTorch | BERT + T5 cricket chatbot |
| 08 | [Urdu Voice Assistant](#-08--urdu-voice-assistant) | 🧠 LLMs & Speech | SpeechRecognition, gTTS | Full Urdu speech ↔ LLM loop |
| 09 | [RAG PDF Chatbot](#-09--rag-pdf-chatbot) | 🧠 LLMs & RAG | LangChain, Qdrant | Grounded Q&A over any PDF |
| 10 | [LiveKit Trip Agent](#-10--livekit-trip-agent) | 🤖 AI Agents | LiveKit, Groq, Cartesia | Real-time voice travel planner |

</div>

---

## 👁️ Computer Vision Projects

### 🔵 01 · Age & Gender Estimation
> **Live dual-head CNN that predicts age and gender from your webcam in real time**

<table><tr><td>

**What it does**
- Shared CNN backbone with two output heads — one for binary gender, one for age regression
- Trained on **IMDB-WIKI** face crop dataset
- Runs inference live on webcam, overlays prediction on the detected face
- Separate training scripts for gender-only, age-only, and joint training

</td><td>

**Tech Stack**
```
TensorFlow / Keras    ← model architecture & training
OpenCV                ← webcam capture & face overlay
IMDB-WIKI dataset     ← 500k+ celebrity face images
NumPy / Matplotlib    ← preprocessing & training curves
```

</td></tr></table>

📁 **[`computer-vision/age-gender-estimation/`](computer-vision/age-gender-estimation)** · Scripts: `train_joint_model.py` · `predict_webcam.py` · `predict_on_images.py`

---

### 🔵 02 · YOLOv8 Face Detection
> **Fine-tuned YOLOv8n on a self-captured dataset — fast, accurate, custom**

<table><tr><td>

**What it does**
- Captures your own face dataset using MediaPipe to auto-crop and label faces
- Fine-tunes **YOLOv8 nano** (fastest variant) on the custom dataset
- Runs real-time face detection on webcam or image files
- Training run artifacts saved in `runs/` for full reproducibility

</td><td>

**Tech Stack**
```
Ultralytics YOLOv8    ← fine-tuning + inference
MediaPipe             ← automated dataset capture
PyYAML (data.yaml)    ← dataset config
OpenCV                ← webcam prediction
```

</td></tr></table>

📁 **[`computer-vision/yolo-face-detection/`](computer-vision/yolo-face-detection)** · Scripts: `train.py` · `predict.py`

---

### 🔵 03 · Face Recognition
> **Two ML approaches side-by-side inside a Tkinter desktop app**

<table><tr><td>

**What it does**
- **CNN approach:** Keras classifier trained on face crops per identity
- **KNN approach:** scikit-learn k-Nearest Neighbors baseline
- Both wrapped in a single Tkinter GUI — register, train, recognize
- Useful for benchmarking deep vs. classical ML on the same data

</td><td>

**Tech Stack**
```
Keras / TensorFlow    ← CNN classifier
scikit-learn          ← KNN baseline
Tkinter               ← desktop GUI
OpenCV                ← face capture & preprocessing
```

</td></tr></table>

📁 **[`computer-vision/face-recognition/`](computer-vision/face-recognition)** · Dirs: `cnn/` · `knn/`

---

### 🔵 04 · Gesture Attendance
> **Raise a thumbs-up or thumbs-down — attendance is marked in Excel instantly**

<table><tr><td>

**What it does**
- Detects thumbs-up (✅ present) or thumbs-down (❌ absent) per student
- Writes results live into an Excel sheet via openpyxl
- Works with a webcam for 10–20 students per session
- Saves the session timestamp alongside each mark

</td><td>

**Tech Stack**
```
MediaPipe Hands       ← 21-landmark hand detection
OpenCV                ← webcam feed
openpyxl              ← Excel read/write
```

</td></tr></table>

📁 **[`computer-vision/gesture-attendance/`](computer-vision/gesture-attendance)** · Script: `attendance.py`

---

### 🔵 05 · Virtual Mouse
> **Your index finger is the cursor. Pinch to click. Zero hardware needed.**

<table><tr><td>

**What it does**
- Tracks index fingertip position → maps to screen coordinates
- Pinch gesture (index + thumb) → left click
- Smooth velocity damping to remove jitter
- Works on any webcam at 720p+

</td><td>

**Tech Stack**
```
MediaPipe Hands       ← 21 hand landmarks
PyAutoGUI             ← cursor & click control
OpenCV                ← webcam capture
```

</td></tr></table>

📁 **[`computer-vision/virtual-mouse/`](computer-vision/virtual-mouse)** · Script: `virtual_mouse.py`

---

### 🔵 06 · Gesture Game Control
> **Open/close your hand to jump, crouch, and move — inside a bundled Unity game**

<table><tr><td>

**What it does**
- Classifies open/closed/pointing hand gestures in real time
- Maps gestures to keyboard inputs for a bundled Unity WebGL game
- Unity build included — no Unity install needed to play
- Runs at low latency: <50ms gesture-to-keypress pipeline

</td><td>

**Tech Stack**
```
MediaPipe Hands       ← gesture classification
PyAutoGUI             ← keyboard event injection
Unity (WebGL build)   ← the game itself
OpenCV                ← webcam pipeline
```

</td></tr></table>

📁 **[`computer-vision/gesture-game-control/`](computer-vision/gesture-game-control)** · Script: `game_control.py` · Dir: `unity-build/`

---

## 🧠 Language Models & Speech

### 🟠 07 · LLM Fine-tuning
> **Fine-tune BERT and T5 from scratch — on real NLP tasks**

<table><tr><td>

**What it does**
- **BERT notebook:** Fine-tuned on GLUE/MRPC sentence-pair similarity task
- **T5 notebook:** Fine-tuned into a Cricket Q&A chatbot using a custom dataset
- Full training loops, evaluation metrics, and inference examples
- Hugging Face Trainer API with custom data collators

</td><td>

**Tech Stack**
```
HuggingFace Transformers   ← BERT, T5, Trainer
PyTorch                    ← training backend
Datasets (HF)              ← GLUE/MRPC loading
Jupyter Notebooks          ← interactive training
```

</td></tr></table>

📁 **[`llm/llm-finetuning/`](llm/llm-finetuning)** · Notebooks: `FineTuningOnBert.ipynb` · `FineTuningCricketModel.ipynb`

---

### 🟠 08 · Urdu Voice Assistant
> **Speak Urdu. Get an intelligent reply — spoken back in Urdu or English.**

<table><tr><td>

**What it does**
- Full speech-to-speech loop: mic → STT → translate → LLM → TTS → speaker
- Two modes: reply in **English** or back in **Urdu** (translate the response)
- Microphone fallback: enumerates all audio devices until Urdu speech is recognised
- Every network call has graceful spoken fallback — never crashes silently

</td><td>

**Tech Stack**
```
SpeechRecognition     ← Google STT (ur-PK locale)
googletrans           ← Urdu ↔ English translation
OpenRouter API        ← Mistral 7B LLM
gTTS                  ← text-to-speech output
```

</td></tr></table>

📁 **[`llm/urdu-voice-assistant/`](llm/urdu-voice-assistant)** · Scripts: `urdu_to_urdu.py` · `urdu_to_english.py`

---

### 🟠 09 · RAG PDF Chatbot
> **Drop in any PDF. Ask it anything. It answers from the document — not from hallucination.**

<table><tr><td>

**What it does**
- Splits PDF → embeds chunks → stores in local Qdrant vector DB (persistent)
- Retrieves top-3 most relevant chunks per question
- Feeds chunk + question to LLM with a grounding prompt ("refuse if not in the doc")
- Retries on rate limits with exponential backoff

</td><td>

**Tech Stack**
```
LangChain                  ← orchestration
Qdrant (local)             ← vector store, on-disk persistence
all-MiniLM-L6-v2           ← local embedding model
OpenRouter API             ← chat LLM
pypdf                      ← PDF parsing
```

</td></tr></table>

📁 **[`llm/rag-pdf-chatbot/`](llm/rag-pdf-chatbot)** · Script: `app.py`

---

## 🤖 AI Agents

### 🟢 10 · LiveKit Trip Planning Agent
> **A real-time voice AI that plans your entire trip in a natural conversation**

<table><tr><td width="60%">

**What it does**
- Talk to it naturally. It understands intent, pulls live data, and responds in < 500ms
- Queries **live APIs** for weather, places, flights — not static data
- Simulates a complete booking flow within the conversation
- Dockerized — one command to run anywhere
- Netlify web console for browser-based voice sessions (no phone needed)

**Live data integrations:**

| Data | API |
|---|---|
| 🌤️ Weather at destination | Geoapify Weather |
| 📍 Hotels, attractions, restaurants | Geoapify Places |
| ✈️ Real-time flight search | RapidAPI Sky Flights |
| 🎫 Booking confirmation | Simulated within agent |

</td><td width="40%">

**Tech Stack**
```
LiveKit Agents        ← real-time voice pipeline
Groq (LLaMA 3.3)      ← ultra-fast LLM inference
Cartesia              ← natural TTS voice
Geoapify              ← weather + places API
RapidAPI Flights      ← live flight search
Docker                ← containerized deploy
Netlify               ← web voice console
```

</td></tr></table>

📁 **[`ai-agents/livekit-trip-agent/`](ai-agents/livekit-trip-agent)** · Main: `agent.py` · `Dockerfile` · `.env.example`

---

## 🚀 Quick Start

```bash
# Clone the repo
git clone https://github.com/ALIKAZMI001/Projects.git
cd Projects

# Pick any project and run it
cd computer-vision/virtual-mouse
python -m venv .venv && .venv\Scripts\activate
pip install -r requirements.txt
python virtual_mouse.py
```

> **For API-based projects** — copy `.env.example` → `.env` and fill in your keys. No secrets are ever committed.

---

## 📁 Repository Structure

```
Projects/
│
├── 👁️  computer-vision/
│   ├── age-gender-estimation/     ← dual-head CNN + IMDB-WIKI dataset
│   ├── yolo-face-detection/       ← self-captured dataset + YOLOv8n weights
│   ├── face-recognition/          ← cnn/ + knn/ + Tkinter desktop app
│   ├── gesture-attendance/        ← MediaPipe → Excel automation
│   ├── virtual-mouse/             ← hand landmark → cursor control
│   └── gesture-game-control/      ← gesture classification → Unity game
│
├── 🧠  llm/
│   ├── llm-finetuning/            ← BERT (GLUE) + T5 (cricket Q&A) notebooks
│   ├── urdu-voice-assistant/      ← Urdu STT → LLM → Urdu/English TTS
│   └── rag-pdf-chatbot/           ← PDF → Qdrant → grounded LLM answers
│
├── 🤖  ai-agents/
│   └── livekit-trip-agent/        ← voice agent + Dockerfile + web console
│
└── ⚙️  .github/workflows/
    └── ci.yml                     ← syntax-checks all Python files on every push
```

---

## 🛠️ Full Tech Stack

<div align="center">

<img src="https://skillicons.dev/icons?i=python,tensorflow,pytorch,opencv,docker,github&perline=6" />
<br/>
<img src="https://skillicons.dev/icons?i=sklearn,jupyter,linux,vscode,git,github&perline=6" />

</div>

<br/>

| Domain | Technologies |
|---|---|
| **Computer Vision** | OpenCV · MediaPipe · TensorFlow/Keras · Ultralytics YOLOv8 |
| **Deep Learning** | PyTorch · HuggingFace Transformers · scikit-learn |
| **LLMs & RAG** | LangChain · Qdrant · sentence-transformers · OpenRouter (Mistral 7B) |
| **Voice & Agents** | LiveKit Agents · Groq (LLaMA 3.3) · Cartesia TTS |
| **Data & APIs** | Geoapify · RapidAPI · openpyxl · pypdf |
| **Infra & Tooling** | Docker · GitHub Actions CI · python-dotenv |

---

<div align="center">

<img src="https://github-readme-activity-graph.vercel.app/api?username=ALIKAZMI001&theme=tokyo-night&bg_color=0D1117&color=6EE7F7&line=3B82F6&point=ffffff&area=true&hide_border=true" width="100%"/>

<br/>

**Found something useful? A ⭐ star means a lot.**

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:24243e,50:302B63,100:0F0C29&height=120&section=footer" width="100%"/>

</div>
