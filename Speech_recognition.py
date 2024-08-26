import streamlit as st
import speech_recognition as sr
from pydub import AudioSegment
from pydub.playback import play
import io
from gtts import gTTS
import os
import tempfile

def play_audio(file_path):
    audio = AudioSegment.from_mp3(file_path)
    play(audio)

def create_greeting_audio():
    text = "Hello Sir, welcome to the speech recognition system. Please click the button to start recording."
    tts = gTTS(text, lang='en')
    # Save the greeting audio to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
        tts.save(temp_file.name)
        return temp_file.name

def main():
    st.title("Speech Recognition System")

    st.write("## Live Speech Convertor")
    st.write("1. Click the button to record your speech.")
    st.write("2. The system will convert your speech to text and display it.")

    # Generate and play greeting audio
    greeting_audio_path = create_greeting_audio()
    st.write("**Playing greeting message...**")
    st.audio(greeting_audio_path, format="audio/mp3")

    recognizer = sr.Recognizer()

    # Record and display audio
    if st.button("Start Recording"):
        with sr.Microphone() as source:
            st.write("Listening...")
            audio = recognizer.listen(source)
            st.write("Processing...")

        # Save the audio file
        audio_file = io.BytesIO()
        with open("temp.wav", "wb") as f:
            f.write(audio.get_wav_data())
        
        st.audio("temp.wav", format="audio/wav")

        try:
            # Use pocketsphinx for offline recognition
            text = recognizer.recognize_google(audio)
            st.write(f"**Transcription:** {text}")

        except sr.UnknownValueError:
            st.write("Sorry, could not understand the audio.")
        except sr.RequestError:
            st.write("Sorry, there was an issue with the request.")
    
    st.write("## Audio Files")
    # Upload and display a saved audio file if needed
    uploaded_file = st.file_uploader("Upload an audio file", type=["wav", "mp3"])
    
    if uploaded_file is not None:
        st.audio(uploaded_file, format='audio/wav')
        # Optionally, process the uploaded file
        with sr.AudioFile(uploaded_file) as source:
            audio = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio)
                st.write(f"**Transcription:** {text}") 
            except sr.UnknownValueError:
                st.write("Sorry, could not understand the audio.")
            except sr.RequestError:
                st.write("Sorry, there was an issue with the request.")

if __name__ == "__main__":
    main()