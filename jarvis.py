import sounddevice as sd
import soundfile as sf
import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import sys
import os
from dotenv import load_dotenv
from groq import Groq

# --- 1. SECURE API CONFIGURATION ---
# This loads the secret key from the .env file so it's never exposed on GitHub
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize the Groq client
if not GROQ_API_KEY:
    print("ERROR: GROQ_API_KEY not found. Did you create the .env file?")
    sys.exit()

client = Groq(api_key=GROQ_API_KEY)

# List of models to try, in order of preference (in case Groq deprecates one)
MODEL_FALLBACK_LIST = [
    "openai/gpt-oss-20b",      
    "openai/gpt-oss-120b",     
    "qwen/qwen3.8-27b",        
]

# --- 2. THE SPEAK FUNCTION ---
def speak(text):
    print(f"JARVIS: {text}")
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 165)
        voices = engine.getProperty('voices')
        for voice in voices:
            if "david" in voice.name.lower() or "george" in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break
        engine.say(text)
        engine.runAndWait()
        engine.stop()
    except Exception as e:
        print(f"[Audio Error: {e}]")

# --- 3. THE LISTEN FUNCTION ---
def record_audio(filename, duration=3):
    fs = 44100
    print("\n[System: Listening...]")
    myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    sf.write(filename, myrecording, fs)

def listen_for_speech(duration=3):
    filename = "temp_audio.wav"
    record_audio(filename, duration)
    
    recognizer = sr.Recognizer()
    text = ""
    
    try:
        with sr.AudioFile(filename) as source:
            audio_data = recognizer.record(source)
        if os.path.exists(filename):
            os.remove(filename)
            
        text = recognizer.recognize_google(audio_data).lower()
        print(f"You said: '{text}'")
        return text
    except sr.UnknownValueError:
        if os.path.exists(filename): os.remove(filename)
        return ""
    except sr.RequestError:
        speak("My speech recognition service is down, Sir.")
        if os.path.exists(filename): os.remove(filename)
        return ""

# --- 4. THE AI BRAIN CONVERSATION MEMORY ---
# This list stores the conversation so JARVIS remembers what you talked about
messages = [
    {"role": "system", "content": "You are JARVIS, Tony Stark's AI assistant from Iron Man. You are helpful, slightly witty, and extremely loyal. Always address the user as 'Sir'. Keep your answers concise (1-3 sentences) because your responses will be spoken out loud. Do not use emojis or markdown formatting."}
]

def chat_with_ai(user_input):
    """Sends the user's input to the Groq AI, trying a list of fallback models."""
    messages.append({"role": "user", "content": user_input})
    
    for model_name in MODEL_FALLBACK_LIST:
        try:
            print(f"[Trying model: {model_name}]")
            chat_completion = client.chat.completions.create(
                messages=messages,
                model=model_name,
                temperature=0.7,
                max_tokens=150
            )
            response = chat_completion.choices[0].message.content
            messages.append({"role": "assistant", "content": response})
            return response
        except Exception as e:
            print(f"[Model {model_name} failed: {e}]")
            continue # Try the next model in the list
    
    # If we get here, all models failed
    return "I am having trouble connecting to my neural network, Sir. All model attempts failed."

# --- 5. THE COMMAND EXECUTOR ---
def execute_command(command):
    if command == "":
        return

    # --- LOCAL COMMANDS (Fast execution) ---
    if "what time is it" in command or "tell me the time" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}, Sir.")
    
    elif "open google" in command:
        speak("Opening Google, Sir.")
        webbrowser.open("https://www.google.com")
        
    elif "open youtube" in command:
        speak("Opening YouTube, Sir.")
        webbrowser.open("https://www.youtube.com")
        
    elif "open code" in command or "open vs code" in command:
        speak("Opening Visual Studio Code, Sir.")
        os.system("code")
        
    elif "exit" in command or "stop" in command or "shut down" in command:
        speak("Powering down. Goodbye, Sir.")
        sys.exit()
        
    # --- AI BRAIN (For everything else) ---
    else:
        print("[Thinking...]")
        ai_response = chat_with_ai(command)
        speak(ai_response)

# --- 6. THE MAIN LOOP ---
def main():
    speak("Systems online. I am at your service, Sir.")
    
    while True:
        text = listen_for_speech(duration=4)
        
        if "jarvis" in text:
            command = text.replace("jarvis", "").strip()
            
            if command:
                execute_command(command)
            else:
                speak("Yes, Sir?")
                command = listen_for_speech(duration=5)
                execute_command(command)

if __name__ == "__main__":
    main()