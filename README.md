# AI & Machine Learning Portfolio

A collection of end-to-end AI projects I built while learning and shipping: computer
vision systems, fine-tuned language models, retrieval-augmented generation, and a
real-time voice agent.

Everything here is runnable Python. Each project has its own README with setup,
usage and implementation notes.

<p>
  <img alt="Python" src="https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white">
  <img alt="TensorFlow" src="https://img.shields.io/badge/TensorFlow-Keras-FF6F00?logo=tensorflow&logoColor=white">
  <img alt="OpenCV" src="https://img.shields.io/badge/OpenCV-4.x-5C3EE8?logo=opencv&logoColor=white">
  <img alt="MediaPipe" src="https://img.shields.io/badge/MediaPipe-0.10-0097A7">
  <img alt="LangChain" src="https://img.shields.io/badge/LangChain-RAG-1C3C3C">
  <img alt="LiveKit" src="https://img.shields.io/badge/LiveKit-Agents-00C2A8">
</p>

---

## Projects

### Computer Vision

| Project | What it does | Stack |
| --- | --- | --- |
| **[Age & Gender Estimation](computer-vision/age-gender-estimation)** | Two-head CNN that predicts gender and age from a face, live on webcam | TensorFlow / Keras, OpenCV, IMDB-WIKI |
| **[YOLOv8 Face Detection](computer-vision/yolo-face-detection)** | Custom dataset capture with MediaPipe + fine-tuned YOLOv8n detector | Ultralytics YOLOv8, MediaPipe |
| **[Face Recognition](computer-vision/face-recognition)** | Two approaches — a Keras classifier and a KNN baseline — behind a Tkinter app | Keras, scikit-learn, Tkinter |
| **[Gesture Attendance](computer-vision/gesture-attendance)** | Marks students present/absent from a thumbs-up/thumbs-down gesture into Excel | MediaPipe, OpenCV, openpyxl |
| **[Virtual Mouse](computer-vision/virtual-mouse)** | Controls the cursor and clicks with hand landmarks | MediaPipe, PyAutoGUI |
| **[Gesture Game Control](computer-vision/gesture-game-control)** | Drives a bundled Unity game with hand gestures | MediaPipe, PyAutoGUI, Unity |

### Language Models & Speech

| Project | What it does | Stack |
| --- | --- | --- |
| **[LLM Fine-tuning](llm/llm-finetuning)** | Notebooks fine-tuning BERT on GLUE/MRPC and a T5 model into a cricket Q&A chatbot | Hugging Face Transformers, PyTorch |
| **[Urdu Voice Assistant](llm/urdu-voice-assistant)** | Full speech loop: Urdu speech in, LLM answer, spoken reply (English or Urdu) | SpeechRecognition, gTTS, OpenRouter |
| **[RAG PDF Chatbot](llm/rag-pdf-chatbot)** | Chunks and embeds a PDF into Qdrant, then answers questions grounded in it | LangChain, Qdrant, sentence-transformers |

### AI Agents

| Project | What it does | Stack |
| --- | --- | --- |
| **[LiveKit Trip Agent](ai-agents/livekit-trip-agent)** | Real-time voice travel planner: live weather, places and flight data, simulated booking | LiveKit Agents, Groq, Cartesia, Geoapify |

---

## Repository layout

```
.
├── computer-vision/
│   ├── age-gender-estimation/    # trained models + training & inference scripts
│   ├── yolo-face-detection/      # fine-tuned YOLOv8n weights + runs
│   ├── face-recognition/         # cnn/ and knn/ implementations + desktop app
│   ├── gesture-attendance/       # MediaPipe + Excel automation
│   ├── virtual-mouse/            # gesture-driven cursor
│   └── gesture-game-control/     # gesture input + Unity build
├── llm/
│   ├── llm-finetuning/           # BERT and T5 notebooks
│   ├── urdu-voice-assistant/     # speech → LLM → speech
│   └── rag-pdf-chatbot/          # retrieval-augmented Q&A over a PDF
├── ai-agents/
│   └── livekit-trip-agent/       # voice agent, Dockerfile, web console
└── .github/workflows/            # CI: syntax-check every Python file
```

## Getting started

Each project is self-contained. The general pattern:

```bash
cd computer-vision/age-gender-estimation
python -m venv .venv
# Windows:  .venv\Scripts\activate      macOS/Linux:  source .venv/bin/activate
pip install -r requirements.txt
python predict_webcam.py
```

Projects that call hosted APIs read their keys from environment variables — copy
`.env.example` where provided and fill in your own keys. **No secrets are committed.**

## About the models and data

- Trained weights (`.h5`, `.pt`) and the bundled Unity build are committed so the
  demos run without retraining.
- The age/gender project ships the IMDB-WIKI face crops it was trained on, which is
  why that folder is large. Cite the [IMDB-WIKI dataset](https://data.vision.ee.ethz.ch/cvl/rrothe/imdb-wiki/)
  if you reuse it.
- Webcam capture scripts write new images locally into their own project folders;
  generated media and caches are covered by the root `.gitignore`.

## License

[MIT](LICENSE) — use it, learn from it, build on it.

---

**Ali Kazmi** · [GitHub](https://github.com/ALIKAZMI001)
