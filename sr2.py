import speech_recognition as sr
import webbrowser

def listen_for_wake_word():
    # Initialize the recognizer
    r = sr.Recognizer()

    # Listen continuously for the wake word
    with sr.Microphone() as source:
        print("Listening for wake word...")
        while True:
            audio = r.listen(source)
            try:
                # Convert speech to text
                speech_text = r.recognize_google(audio).lower()
                print("Heard: " + speech_text)
                if "python" in speech_text:
                    print("Wake word detected!")
                    return True
            except sr.UnknownValueError:
                pass  # Ignore if the speech isn't understood
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")

def listen_for_command():
    # Initialize the recognizer
    r = sr.Recognizer()

    # Listen for a command after wake word is detected
    with sr.Microphone() as source:
        print("Listening for command...")
        audio = r.listen(source)

    try:
        # Use Google Web Speech API to decode the audio
        command = r.recognize_google(audio).lower()
        print("You said: " + command)
        return command
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")

    return ""

# Function to open a YouTube search for the specified query
def search_youtube(query):
    url = f"https://www.youtube.com/results?search_query={query}"
    webbrowser.open(url)

# Main function to get voice input and search on YouTube
def main():
    while True:
        if listen_for_wake_word():
            command = listen_for_command()
            if command:
                if 'exit' in command or 'stop' in command:
                    print("Exiting program...")
                    break
                search_youtube(command.replace(" ", "+"))
            else:
                print("No command detected, please try again.")

if __name__ == "__main__":
    main()
