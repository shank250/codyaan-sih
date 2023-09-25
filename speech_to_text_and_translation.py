import speech_recognition as sr
from googletrans import Translator

# Initialize the recognizer
recognizer = sr.Recognizer()
translator = Translator()

def record_audio():
    with sr.Microphone() as source:
        print("Please speak your grievance...")
        audio = recognizer.listen(source)
        return audio

def convert_audio_to_text(audio):
    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand the audio.")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return ""

def translate_to_english(text):
    translation = translator.translate(text, src='auto', dest='en')
    return translation.text

if __name__ == "__main__":
    audio = record_audio()
    if audio:
        text = convert_audio_to_text(audio)
        if text:
            print("You said:", text)
            translated_text = translate_to_english(text)
            print("Translation to English:", translated_text)
        else:
            print("No speech detected.")
    else:
        print("Failed to record audio.")
