import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser

# Initialize the recognizer
recognizer = sr.Recognizer()

# Initialize the text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    
    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio).lower()
        print(f"User said: {query}")
        return query
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that. Could you please repeat?")
        return ""
    except sr.RequestError:
        print("Sorry, there was an error with the speech recognition service.")
        return ""

def process_command(command):
    if "hello" in command:
        speak("Hello! How can I help you today?")
    elif "time" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}")
    elif "date" in command:
        current_date = datetime.datetime.now().strftime("%B %d, %Y")
        speak(f"Today's date is {current_date}")
    elif "search" in command:
        search_query = command.replace("search", "").strip()
        url = f"https://www.google.com/search?q={search_query}"
        webbrowser.open(url)
        speak(f"Here are the search results for {search_query}")
    else:
        speak("Sorry, I don't understand that command. Can you please try again?")

def main():
    speak("Hello! I'm your voice assistant. How can I help you?")
    
    while True:
        command = listen()
        if command:
            if "exit" in command or "quit" in command:
                speak("Goodbye!")
                break
            process_command(command)

if __name__ == "__main__":
    main()