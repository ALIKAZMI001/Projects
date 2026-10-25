<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0F0C29,40:302B63,100:24243e&height=230&section=header&text=Ali%20Kazmi&fontSize=78&fontColor=ffffff&fontAlignY=38&desc=AI%20%26%20Machine%20Learning%20Portfolio&descAlignY=60&descSize=26&animation=fadeIn&stroke=6EE7F7&strokeWidth=2" width="100%"/>

<br/>

<img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&weight=700&size=22&duration=2800&pause=900&color=6EE7F7&center=true&vCenter=true&width=750&lines=10+End-to-End+AI+Projects;Computer+Vision+%7C+LLMs+%7C+RAG+%7C+Voice+Agents;Real+models.+Real+data.+Real+results.;Everything+is+runnable+Python." alt="Typing SVG"/>

<br/><br/>

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)][repo]
[![TensorFlow](https://img.shields.io/badge/TensorFlow-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)][repo]
[![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)][repo]
[![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)][repo]
[![YOLOv8](https://img.shields.io/badge/YOLOv8-00CFFF?style=for-the-badge)][repo]
[![HuggingFace](https://img.shields.io/badge/🤗%20HuggingFace-FFD21F?style=for-the-badge&logoColor=black)][repo]
[![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge)][repo]
[![LiveKit](https://img.shields.io/badge/LiveKit-00C2A8?style=for-the-badge)][repo]
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)][repo]

[repo]: https://github.com/ALIKAZMI001/Projects

</div>

---

## 📌 All Projects

<table>
<tr>
<td align="center" width="50%">

### ✈️ [LiveKit Trip Agent](livekit-trip-agent)
**Real-time voice AI travel planner**

Talk to it naturally — it queries live flight data, weather, and places, then simulates booking, all in one voice conversation.

`LiveKit` `Groq LLaMA 3.3` `Cartesia TTS` `Geoapify` `RapidAPI` `Docker`

[![View](https://img.shields.io/badge/View%20Project-6EE7F7?style=flat-square&logo=github&logoColor=black)](livekit-trip-agent)

</td>
<td align="center" width="50%">

### 📄 [RAG PDF Chatbot](rag-pdf-chatbot)
**Ask any question about any PDF — grounded answers only**

Embeds your PDF into a local Qdrant vector store, retrieves top chunks, and feeds them to an LLM with a strict grounding prompt. Zero hallucination.

`LangChain` `Qdrant` `sentence-transformers` `OpenRouter` `pypdf`

[![View](https://img.shields.io/badge/View%20Project-6EE7F7?style=flat-square&logo=github&logoColor=black)](rag-pdf-chatbot)

</td>
</tr>
<tr>
<td align="center" width="50%">

### 🎙️ [Urdu Voice Assistant](urdu-voice-assistant)
**Full speech-to-speech loop in Urdu**

Mic → Google STT (ur-PK) → translate → LLM → translate back → gTTS speaker. Runs in Urdu-only or Urdu-to-English mode.

`SpeechRecognition` `googletrans` `gTTS` `OpenRouter` `Mistral 7B`

[![View](https://img.shields.io/badge/View%20Project-6EE7F7?style=flat-square&logo=github&logoColor=black)](urdu-voice-assistant)

</td>
<td align="center" width="50%">

### 🏏 [LLM Fine-tuning](llm-finetuning)
**Fine-tune BERT & T5 from scratch**

BERT fine-tuned on GLUE/MRPC. T5 turned into a cricket Q&A chatbot using a custom dataset. Full training loops in Jupyter.

`HuggingFace Transformers` `PyTorch` `BERT` `T5` `GLUE`

[![View](https://img.shields.io/badge/View%20Project-6EE7F7?style=flat-square&logo=github&logoColor=black)](llm-finetuning)

</td>
</tr>
<tr>
<td align="center" width="50%">

### 🎂 [Age & Gender Estimation](age-gender-estimation)
**Dual-head CNN — live webcam inference**

One CNN backbone, two output heads: binary gender + age regression. Trained on 500k+ IMDB-WIKI face crops. 30 FPS on webcam.

`TensorFlow` `Keras` `OpenCV` `IMDB-WIKI`

[![View](https://img.shields.io/badge/View%20Project-6EE7F7?style=flat-square&logo=github&logoColor=black)](age-gender-estimation)

</td>
<td align="center" width="50%">

### 🎯 [YOLOv8 Face Detection](yolo-face-detection)
**Self-captured dataset → fine-tuned YOLOv8n**

Used MediaPipe to auto-label a custom face dataset, then fine-tuned YOLOv8 nano. Fast, accurate, and fully reproducible.

`Ultralytics YOLOv8` `MediaPipe` `OpenCV` `PyYAML`

[![View](https://img.shields.io/badge/View%20Project-6EE7F7?style=flat-square&logo=github&logoColor=black)](yolo-face-detection)

</td>
</tr>
<tr>
<td align="center" width="50%">

### 🪪 [Face Recognition](face-recognition)
**CNN vs KNN — two approaches, one desktop app**

Keras CNN classifier vs scikit-learn KNN baseline, side-by-side comparison inside a Tkinter GUI. Register, train, and recognize faces.

`Keras` `scikit-learn` `Tkinter` `OpenCV`

[![View](https://img.shields.io/badge/View%20Project-6EE7F7?style=flat-square&logo=github&logoColor=black)](face-recognition)

</td>
<td align="center" width="50%">

### 🙌 [Gesture Attendance](gesture-attendance)
**Thumbs-up/down → marks attendance in Excel**

MediaPipe detects thumbs-up (present) or thumbs-down (absent) and instantly writes the result into an openpyxl spreadsheet with timestamps.

`MediaPipe` `OpenCV` `openpyxl`

[![View](https://img.shields.io/badge/View%20Project-6EE7F7?style=flat-square&logo=github&logoColor=black)](gesture-attendance)

</td>
</tr>
<tr>
<td align="center" width="50%">

### 🖱️ [Virtual Mouse](virtual-mouse)
**Your hand is your mouse — no hardware needed**

Index fingertip → screen cursor. Pinch gesture → left click. Smooth velocity damping. Works on any 720p+ webcam.

`MediaPipe` `PyAutoGUI` `OpenCV`

[![View](https://img.shields.io/badge/View%20Project-6EE7F7?style=flat-square&logo=github&logoColor=black)](virtual-mouse)

</td>
<td align="center" width="50%">

### 🎮 [Gesture Game Control](gesture-game-control)
**Play a Unity game entirely with hand gestures**

Open/close/point hand gestures are classified in real time and injected as keyboard events into a bundled Unity WebGL game. <50ms latency.

`MediaPipe` `PyAutoGUI` `Unity WebGL`

[![View](https://img.shields.io/badge/View%20Project-6EE7F7?style=flat-square&logo=github&logoColor=black)](gesture-game-control)

</td>
</tr>
</table>

---

## 🚀 Quick Start

Every project is fully self-contained:

```bash
# Clone
git clone https://github.com/ALIKAZMI001/Projects.git
cd Projects

# Pick any project — same pattern for all
cd virtual-mouse
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS / Linux
pip install -r requirements.txt
python virtual_mouse.py
```

> **Projects with API keys** — copy `.env.example` → `.env` and add your keys. No secrets are committed.

---

## 📁 Repository Structure

```
Projects/                          ← you are here
│
├── 🎂  age-gender-estimation/     dual-head CNN + IMDB-WIKI dataset
├── 🎯  yolo-face-detection/       self-captured dataset + YOLOv8n weights
├── 🪪  face-recognition/          cnn/ + knn/ + Tkinter desktop app
├── 🙌  gesture-attendance/        MediaPipe hand → Excel automation
├── 🖱️  virtual-mouse/             hand landmark → cursor + click
├── 🎮  gesture-game-control/      hand gesture → Unity WebGL game
├── 🏏  llm-finetuning/            BERT (GLUE) + T5 cricket Q&A notebooks
├── 🎙️  urdu-voice-assistant/      Urdu STT → LLM → Urdu/English TTS
├── 📄  rag-pdf-chatbot/           PDF → Qdrant → grounded LLM answers
├── ✈️  livekit-trip-agent/        real-time voice agent + Docker + web console
│
└── ⚙️  .github/workflows/ci.yml  syntax-checks every Python file on push
```

---

## 🛠️ Tech Stack

<div align="center">

<img src="https://skillicons.dev/icons?i=python,tensorflow,pytorch,opencv,docker,git,github,linux,vscode,jupyter&perline=10" />

</div>

<br/>

<div align="center">

| Domain | Technologies |
|---|---|
| **Computer Vision** | OpenCV · MediaPipe · TensorFlow/Keras · Ultralytics YOLOv8 |
| **Deep Learning** | PyTorch · HuggingFace Transformers · scikit-learn |
| **LLMs & RAG** | LangChain · Qdrant · sentence-transformers · OpenRouter |
| **Voice & Agents** | LiveKit Agents · Groq (LLaMA 3.3) · Cartesia TTS |
| **Data & APIs** | Geoapify · RapidAPI · openpyxl · pypdf |
| **Infra** | Docker · GitHub Actions CI · python-dotenv |

</div>

---

<div align="center">

<img src="https://github-readme-activity-graph.vercel.app/api?username=ALIKAZMI001&theme=tokyo-night&bg_color=0D1117&color=6EE7F7&line=3B82F6&point=ffffff&area=true&hide_border=true" width="100%"/>

<br/>

**If any project helped you — a ⭐ goes a long way.**

[![GitHub](https://img.shields.io/badge/ALIKAZMI001-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/ALIKAZMI001)

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:24243e,50:302B63,100:0F0C29&height=120&section=footer" width="100%"/>

</div>
