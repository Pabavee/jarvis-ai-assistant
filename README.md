# JARVIS - AI Voice Assistant (Iron Man Inspired)

A Python-based virtual assistant that listens for a wake word, answers questions using an LLM, and controls local PC apps via voice commands.

## 🚀 Features
- **Conversational AI:** Integrated with the Groq API (Llama 3.1) to answer general knowledge questions conversationally.
- **Speech-to-Text:** Uses Google Speech Recognition to transcribe voice commands.
- **Text-to-Speech:** Uses `pyttsx3` for robotic, real-time audio responses.
- **System Control:** Can open websites (Google, YouTube) and launch local apps (VS Code).
- **Secure:** Uses `python-dotenv` to keep API keys safe.

## 🛠️ Tech Stack
- Python 3
- Groq API (Llama 3.1)
- SpeechRecognition, pyttsx3, sounddevice

## ⚙️ Setup
1. Clone the repo: `git clone ...`
2. Install dependencies: `pip install -r requirements.txt`
3. Create a `.env` file and add your Groq API Key: `GROQ_API_KEY=your_key_here`
4. Run: `python jarvis.py`