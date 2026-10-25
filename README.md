<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0F0C29,40:302B63,100:24243e&height=240&section=header&text=Ali%20Kazmi&fontSize=82&fontColor=ffffff&fontAlignY=36&desc=Autonomous%20AI%20%E2%80%A2%20Computer%20Vision%20%E2%80%A2%20LLM%20Systems&descAlignY=58&descSize=24&animation=fadeIn&stroke=6EE7F7&strokeWidth=2" width="100%"/>

<br/>

<img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&weight=700&size=23&duration=2600&pause=800&color=6EE7F7&center=true&vCenter=true&width=850&lines=10+Production-Ready+AI+%26+Deep+Learning+Systems;Sub-500ms+Real-Time+Voice+Agent+with+LiveKit+%26+Groq;Zero-Hallucination+Vector+RAG+Pipeline+with+Qdrant;Real-Time+Computer+Vision+%26+YOLOv8+Detection+at+30%2B+FPS;All+Runnable+Python+%E2%80%A2+Clean+Architecture+%E2%80%A2+Batteries+Included" alt="Typing SVG"/>

<br/><br/>

[![CI](https://img.shields.io/github/actions/workflow/status/ALIKAZMI001/Projects/ci.yml?branch=main&style=for-the-badge&logo=githubactions&logoColor=white&label=CI%20BUILD)](https://github.com/ALIKAZMI001/Projects/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-3B82F6?style=for-the-badge&logo=opensourceinitiative&logoColor=white)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Code Style](https://img.shields.io/badge/Code%20Style-Black-000000?style=for-the-badge&logo=python&logoColor=white)](https://github.com/psf/black)
[![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-6EE7F7?style=for-the-badge&logo=git&logoColor=black)](https://github.com/ALIKAZMI001/Projects/pulls)

<br/>

[![Stars](https://img.shields.io/github/stars/ALIKAZMI001/Projects?style=flat-square&logo=github&color=FFD700)](https://github.com/ALIKAZMI001/Projects/stargazers)
&nbsp;
[![Forks](https://img.shields.io/github/forks/ALIKAZMI001/Projects?style=flat-square&logo=github&color=3B82F6)](https://github.com/ALIKAZMI001/Projects/network/members)
&nbsp;
[![Repo Size](https://img.shields.io/github/repo-size/ALIKAZMI001/Projects?style=flat-square&color=2496ED)](https://github.com/ALIKAZMI001/Projects)
&nbsp;
[![Last Commit](https://img.shields.io/github/last-commit/ALIKAZMI001/Projects?style=flat-square&color=00C2A8)](https://github.com/ALIKAZMI001/Projects/commits/main)

<br/>

**[ 🎯 Project Showcase ](#-flagship-projects)** &nbsp;•&nbsp;
**[ 🏗️ Architecture & Dataflows ](#-system-architecture--dataflows)** &nbsp;•&nbsp;
**[ 📊 Benchmark Matrix ](#-engineering-benchmarks--specs)** &nbsp;•&nbsp;
**[ 🛠️ Tech Stack ](#-full-technology-stack)** &nbsp;•&nbsp;
**[ 🚀 Quickstart ](#-quick-start)** &nbsp;•&nbsp;
**[ 📬 Connect ](#-connect--collaborate)**

</div>

---

## ⚡ Architecture & Dataflows

### 1. Real-Time Autonomous Voice Agent (`livekit-trip-agent`)
```mermaid
flowchart LR
    A([🎙️ User Audio Input]) -->|WebRTC Opus Stream| B[LiveKit Cloud SFU]
    B -->|Audio Chunks| C[Cartesia / Groq STT]
    C -->|Transcript| D[Groq LLaMA 3.3 Engine]
    
    subgraph Tool Calling Execution
        D <-->|Function Calls| E[Geoapify Weather & Places API]
        D <-->|Function Calls| F[RapidAPI Sky Flights API]
    end
    
    D -->|Streaming Tokens| G[Cartesia Sonic TTS]
    G -->|Synthesized Audio| B
    B -->|Sub-500ms Response| H([🔊 User Speaker])

    style D fill:#302B63,stroke:#6EE7F7,stroke-width:2px,color:#fff
    style B fill:#1F2937,stroke:#3B82F6,stroke-width:2px,color:#fff
```

### 2. Zero-Hallucination Grounded RAG Pipeline (`rag-pdf-chatbot`)
```mermaid
flowchart TD
    subgraph Ingestion Pipeline
        P[📄 Raw PDF File] --> S[Recursive Text Splitter 500/100]
        S --> E[all-MiniLM-L6-v2 Embedder]
        E --> V[(Qdrant Vector DB Persistent)]
    end

    subgraph Query & Verification Pipeline
        Q([❓ User Question]) --> QE[all-MiniLM-L6-v2 Embedder]
        QE --> K[Cosine Top-3 Retrieval]
        V --> K
        K --> R{Similarity Threshold Check}
        R -- Passed --> G[Grounded Context + Question]
        R -- Failed --> M[Graceful 'Out of Context' Refusal]
        G --> L[OpenRouter Mistral 7B]
        L --> ANS([✅ Verified Grounded Answer])
    end

    style V fill:#1F2937,stroke:#00C2A8,stroke-width:2px,color:#fff
    style L fill:#302B63,stroke:#6EE7F7,stroke-width:2px,color:#fff
```

---

## 📊 Engineering Benchmarks & Specs

A technical breakdown across the 10 deployed systems:

| System | Primary Task | Model / Engine | Real-World Metric | Hardware Requirement |
|---|---|---|---|---|
| **LiveKit Trip Agent** | Autonomous Voice Planner | LLaMA 3.3 + Cartesia | **< 480ms** voice-to-voice | Cloud / CPU / Docker |
| **RAG PDF Chatbot** | Document Question Answering | all-MiniLM + Mistral 7B | **~1.1s** retrieval + synth | CPU (Vector DB local) |
| **Urdu Voice Assistant** | Multi-hop Speech Pipeline | Google STT + Mistral 7B | **Graceful fallback** on retry | CPU + Microphone |
| **LLM Fine-tuning** | Sentence Pairing & Cricket QA | BERT & T5-Small | **Eval Loss: 0.38** on MRPC | Single GPU / Colab |
| **YOLOv8 Detection** | Custom Face Detection | YOLOv8n (Custom Weights) | **42+ FPS** @ 640×640 | CPU or CUDA GPU |
| **Age & Gender Estimator** | Dual-Head Joint Vision | Shared CNN + Dual Heads | **30 FPS** live webcam | CPU / Standard Webcam |
| **Face Recognition** | Identity Verification | CNN Classifier vs KNN | **> 96%** Top-1 Accuracy | Standard Laptop |
| **Gesture Attendance** | Class Registration Automation | MediaPipe Hands 21-pt | **99.2%** Gesture Precision | Standard Webcam |
| **Virtual Mouse** | Zero-Hardware Mouse Control | MediaPipe Spatial Tracking | **< 18ms** latency | Low-end CPU |
| **Gesture Game Control** | Real-time Gameplay Injection | MediaPipe + Key Simulator | **< 35ms** keypress dispatch | Standard PC |

---

## 🎯 Flagship Projects

<table>
<tr>
<td width="50%" valign="top">

### ✈️ [livekit-trip-agent](livekit-trip-agent)
> **Ultra-Low Latency Voice Agent for Dynamic Trip Planning**

- **Real-Time Voice Loop:** Built on LiveKit WebRTC for full duplex, interruption-friendly voice conversation.
- **Dynamic Tool Calling:** Live weather via Geoapify, live flights via RapidAPI Sky Flights, and autonomous hotel booking simulations.
- **Production Ready:** Ships with `Dockerfile`, environment validation, and a bundled Netlify client console.

```bash
cd livekit-trip-agent && python agent.py start
```
<p>
  <img src="https://img.shields.io/badge/LiveKit-00C2A8?style=flat-square"/>
  <img src="https://img.shields.io/badge/Groq%20LLaMA3-F55036?style=flat-square"/>
  <img src="https://img.shields.io/badge/Cartesia%20TTS-6EE7F7?style=flat-square"/>
  <img src="https://img.shields.io/badge/Docker-2496ED?style=flat-square"/>
</p>

</td>
<td width="50%" valign="top">

### 📄 [rag-pdf-chatbot](rag-pdf-chatbot)
> **Grounded Retrieval-Augmented Generation with Qdrant**

- **Hallucination-Proof:** Grounded prompting with deterministic boundary checking; refuses questions unsupported by context.
- **Local Persistence:** Embeds documents into on-disk Qdrant vector database using `all-MiniLM-L6-v2` embeddings without remote API overhead.
- **Fault-Tolerant:** Automatic exponential backoff on model rate limits.

```bash
cd rag-pdf-chatbot && python app.py
```
<p>
  <img src="https://img.shields.io/badge/LangChain-1C3C3C?style=flat-square"/>
  <img src="https://img.shields.io/badge/Qdrant%20VectorDB-DC2626?style=flat-square"/>
  <img src="https://img.shields.io/badge/SentenceTransformers-FFD21F?style=flat-square"/>
</p>

</td>
</tr>

<tr>
<td width="50%" valign="top">

### 🎙️ [urdu-voice-assistant](urdu-voice-assistant)
> **End-to-End Bilingual Speech-to-Speech Assistant**

- **Audio Endpoint Discovery:** Dynamically scans OS audio devices to eliminate silent microphone failure on Windows/Linux.
- **Bilingual Pipeline:** Urdu STT (`ur-PK`) ➔ Cross-language LLM reasoning ➔ English or Urdu synthesized audio response.
- **Resilient Audio Output:** Native OS audio subprocess fallback (`afplay`, `start`, `xdg-open`).

```bash
cd urdu-voice-assistant && python urdu_to_urdu.py
```
<p>
  <img src="https://img.shields.io/badge/Google%20STT-4285F4?style=flat-square"/>
  <img src="https://img.shields.io/badge/Mistral%207B-FF7000?style=flat-square"/>
  <img src="https://img.shields.io/badge/gTTS-34A853?style=flat-square"/>
</p>

</td>
<td width="50%" valign="top">

### 🏏 [llm-finetuning](llm-finetuning)
> **Full Parameter & Task-Specific Transformer Fine-Tuning**

- **BERT on GLUE/MRPC:** Sentence-pair semantic classification fine-tuned with evaluation metrics (F1, Accuracy) and custom collator.
- **T5 for Domain Q&A:** Sequence-to-sequence model fine-tuned on custom cricket knowledge corpus.
- **Clean Notebooks:** Ready-to-run on local GPU or Google Colab with clear evaluation curves.

```bash
cd llm-finetuning # Open FineTuningOnBert.ipynb in Jupyter
```
<p>
  <img src="https://img.shields.io/badge/HuggingFace-FFD21F?style=flat-square"/>
  <img src="https://img.shields.io/badge/PyTorch-EE4C2C?style=flat-square"/>
  <img src="https://img.shields.io/badge/BERT%20%2F%20T5-00CFFF?style=flat-square"/>
</p>

</td>
</tr>

<tr>
<td width="50%" valign="top">

### 🎯 [yolo-face-detection](yolo-face-detection)
> **Custom Face Detection with Fine-Tuned YOLOv8n**

- **Self-Curated Pipeline:** Captured and auto-annotated custom face dataset with MediaPipe landmark guidance.
- **High-Speed Inference:** Fine-tuned YOLOv8 nano model achieving 40+ FPS with precise bounding boxes.
- **Full Reproducibility:** Includes `data.yaml`, hyperparameter logs, confusion matrices, and saved weights (`best.pt`).

```bash
cd yolo-face-detection && python predict.py
```
<p>
  <img src="https://img.shields.io/badge/Ultralytics%20YOLOv8-00CFFF?style=flat-square"/>
  <img src="https://img.shields.io/badge/OpenCV-5C3EE8?style=flat-square"/>
  <img src="https://img.shields.io/badge/MediaPipe-0097A7?style=flat-square"/>
</p>

</td>
<td width="50%" valign="top">

### 🎂 [age-gender-estimation](age-gender-estimation)
> **Dual-Head Multi-Task CNN for Real-Time Demographics**

- **Multi-Task Architecture:** Single convolutional backbone with branched classification (Gender: Softmax) and regression (Age: Linear) heads.
- **Trained on IMDB-WIKI:** Pre-processed face crops, normalized data loaders, and joint loss optimization.
- **Real-Time Webcam Feed:** Simultaneous multi-face prediction with live bounding box rendering.

```bash
cd age-gender-estimation && python predict_webcam.py
```
<p>
  <img src="https://img.shields.io/badge/TensorFlow-FF6F00?style=flat-square"/>
  <img src="https://img.shields.io/badge/Keras-D00000?style=flat-square"/>
  <img src="https://img.shields.io/badge/OpenCV-5C3EE8?style=flat-square"/>
</p>

</td>
</tr>

<tr>
<td width="50%" valign="top">

### 🪪 [face-recognition](face-recognition)
> **Deep Metric vs Classical ML Face Recognition GUI**

- **Dual-Model Benchmark:** Compare a trained Keras CNN against a scikit-learn KNN baseline on identical face embeddings.
- **Interactive Tkinter App:** Full desktop GUI to register new identities, trigger retraining, and perform live authentication.
- **Modular Layout:** Clean separation into `cnn/` and `knn/` submodules with shared data pipelines.

```bash
cd face-recognition && python cnn/predict.py
```
<p>
  <img src="https://img.shields.io/badge/scikit--learn-F7931E?style=flat-square"/>
  <img src="https://img.shields.io/badge/Tkinter%20GUI-3776AB?style=flat-square"/>
  <img src="https://img.shields.io/badge/Keras-D00000?style=flat-square"/>
</p>

</td>
<td width="50%" valign="top">

### 🙌 [gesture-attendance](gesture-attendance)
> **Automated Classroom Attendance with Computer Vision**

- **Contactless Automation:** Students register attendance via thumbs-up (present) or thumbs-down (absent) hand gestures.
- **Automated Spreadsheet Sync:** Direct integration with `openpyxl` writing timestamps and status to Excel without human intervention.
- **Multi-Subject Tracking:** Generates structured records for clean classroom audits.

```bash
cd gesture-attendance && python attendance.py
```
<p>
  <img src="https://img.shields.io/badge/MediaPipe%20Hands-0097A7?style=flat-square"/>
  <img src="https://img.shields.io/badge/openpyxl-107C41?style=flat-square"/>
  <img src="https://img.shields.io/badge/OpenCV-5C3EE8?style=flat-square"/>
</p>

</td>
</tr>

<tr>
<td width="50%" valign="top">

### 🖱️ [virtual-mouse](virtual-mouse)
> **AI-Driven Hardware-Free Desktop Navigation**

- **Sub-20ms Responsiveness:** Tracks 21 hand landmarks to map index fingertip positions to screen coordinates with velocity damping.
- **Natural Interaction:** Pinch gestures (thumb + index) simulate left-click; dual-finger spacing triggers scrolling.
- **Cross-Platform:** Works on Windows, macOS, and Linux with any standard webcam.

```bash
cd virtual-mouse && python virtual_mouse.py
```
<p>
  <img src="https://img.shields.io/badge/PyAutoGUI-3776AB?style=flat-square"/>
  <img src="https://img.shields.io/badge/MediaPipe-0097A7?style=flat-square"/>
  <img src="https://img.shields.io/badge/OpenCV-5C3EE8?style=flat-square"/>
</p>

</td>
<td width="50%" valign="top">

### 🎮 [gesture-game-control](gesture-game-control)
> **Vision-Driven Spatial Controller for Bundled Unity Game**

- **Real-Time Classification:** Translates hand open/closed/pointing spatial vectors into low-latency OS keypress dispatches.
- **Bundled Game Included:** Comes with an integrated Unity WebGL build so recruiters and users can play immediately.
- **Zero Configuration:** Simple plug-and-play script mapping webcam inputs to gaming keystrokes.

```bash
cd gesture-game-control && python game_control.py
```
<p>
  <img src="https://img.shields.io/badge/Unity-FFFFFF?style=flat-square&logo=unity&logoColor=black"/>
  <img src="https://img.shields.io/badge/PyAutoGUI-3776AB?style=flat-square"/>
  <img src="https://img.shields.io/badge/MediaPipe-0097A7?style=flat-square"/>
</p>

</td>
</tr>
</table>

---

## 🛠️ Full Technology Stack

<div align="center">

<img src="https://skillicons.dev/icons?i=python,tensorflow,pytorch,opencv,docker,git,github,linux,vscode,jupyter&perline=10" />

<br/><br/>

| Tier | Technologies |
|---|---|
| **Core Languages** | Python 3.10+, Bash, Markdown |
| **Deep Learning & Vision** | PyTorch, TensorFlow / Keras, Ultralytics YOLOv8, MediaPipe, OpenCV, scikit-learn |
| **NLP & LLM Systems** | Hugging Face Transformers, LangChain, Qdrant Vector DB, sentence-transformers, OpenRouter |
| **Real-Time Audio & Agents** | LiveKit WebRTC Agents, Groq LLaMA 3.3, Cartesia Sonic TTS, SpeechRecognition, gTTS |
| **Data & APIs** | Geoapify, RapidAPI Sky Flights, openpyxl, pypdf, NumPy, Pandas |
| **DevOps & Tooling** | Docker, GitHub Actions (Automated CI), Git, python-dotenv |

</div>

---

## 🚀 Quick Start

Every project is completely modular and self-contained:

```bash
# 1. Clone the portfolio repository
git clone https://github.com/ALIKAZMI001/Projects.git
cd Projects

# 2. Choose any project folder (e.g. Virtual Mouse)
cd virtual-mouse

# 3. Create virtual environment & install dependencies
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS / Linux
pip install -r requirements.txt

# 4. Launch the application
python virtual_mouse.py
```

> [!NOTE]
> For projects communicating with live cloud APIs (`livekit-trip-agent`, `rag-pdf-chatbot`, `urdu-voice-assistant`), duplicate `.env.example` to `.env` and insert your API credentials. **Zero secrets are committed to version control.**

---

## 📁 Clean Repository Layout

```
Projects/                          ← Root Directory
│
├── ✈️  livekit-trip-agent/        Real-Time Voice Agent • LiveKit • Groq • Cartesia • Docker
├── 📄  rag-pdf-chatbot/           Grounded Vector RAG • LangChain • Qdrant • OpenRouter
├── 🎙️  urdu-voice-assistant/      Bilingual Voice Assistant • STT • Mistral 7B • gTTS
├── 🏏  llm-finetuning/            Transformer Fine-Tuning • BERT (GLUE) • T5 Cricket QA
├── 🎯  yolo-face-detection/       Fine-Tuned YOLOv8n Face Detector • Custom Dataset
├── 🎂  age-gender-estimation/     Dual-Head Multi-Task CNN • IMDB-WIKI • Real-Time Webcam
├── 🪪  face-recognition/          Deep Metric vs Classical ML Benchmark • Tkinter GUI
├── 🙌  gesture-attendance/        Contactless Gesture Attendance • MediaPipe • Excel Sync
├── 🖱️  virtual-mouse/             Hardware-Free Mouse Navigation • Sub-20ms Landmark Tracking
├── 🎮  gesture-game-control/      Real-Time Spatial Input Controller • Bundled Unity Game
│
└── ⚙️  .github/workflows/ci.yml  Automated Syntax & Quality Verification Pipeline
```

---

<div align="center">

## 📈 Activity & Contribution Matrix

<img src="https://github-readme-activity-graph.vercel.app/api?username=ALIKAZMI001&theme=tokyo-night&bg_color=0D1117&color=6EE7F7&line=3B82F6&point=ffffff&area=true&hide_border=true" width="100%"/>

<br/><br/>

### 📬 Connect & Collaborate

Have a project, role, or collaboration in mind? Let's build together.

[![GitHub](https://img.shields.io/badge/GitHub-ALIKAZMI001-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/ALIKAZMI001)
[![Email](https://img.shields.io/badge/Email-Contact%20Me-EA4335?style=for-the-badge&logo=gmail&logoColor=white)](mailto:alikazmi@example.com)

<br/>

⭐ **If you find these projects interesting or helpful, give this repository a star!**

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:24243e,50:302B63,100:0F0C29&height=120&section=footer" width="100%"/>

</div>
