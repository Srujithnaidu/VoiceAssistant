import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser as wb
import os
import random
import pyautogui
import pyjokes
from urllib.parse import quote
import speedtest




def speak(text):
    try:
        print(f"Speaking: {text}")  # Debug line
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)  # Or use voices[0].id
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 1)
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Speech Error: {e}")



def time() -> None:
    """Tells the current time."""
    current_time = datetime.datetime.now().strftime("%I:%M:%S %p")
    speak("The current time is")
    speak(current_time)
    print("The current time is", current_time)


def date() -> None:
    """Tells the current date."""
    now = datetime.datetime.now()
    speak("The current date is")
    speak(f"{now.day} {now.strftime('%B')} {now.year}")
    print(f"The current date is {now.day}/{now.month}/{now.year}")


def wishme() -> None:
    """Greets the user based on the time of day."""
    speak("Welcome back, sir!")
    print("Welcome back, sir!")

    hour = datetime.datetime.now().hour
    if 4 <= hour < 12:
        speak("Good morning!")
        print("Good morning!")
    elif 12 <= hour < 16:
        speak("Good afternoon!")
        print("Good afternoon!")
    elif 16 <= hour < 24:
        speak("Good evening!")
        print("Good evening!")
    else:
        speak("Good night, see you tomorrow.")

    assistant_name = load_name()
    speak(f"{assistant_name} at your service. Please tell me how may I assist you.")
    print(f"{assistant_name} at your service. Please tell me how may I assist you.")


def screenshot() -> None:
    """Takes a screenshot and saves it."""
    img = pyautogui.screenshot()
    img_path = os.path.expanduser("~\\Pictures\\screenshot.png")
    img.save(img_path)
    speak(f"Screenshot saved as {img_path}.")
    print(f"Screenshot saved as {img_path}.")

def takecommand() -> str:
    """Takes microphone input from the user and returns it as text."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1

        try:
            audio = r.listen(source, timeout=5)  # Listen with a timeout
        except sr.WaitTimeoutError:
            speak("Timeout occurred. Please try again.")
            return None

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(query)
        return query.lower()
    except sr.UnknownValueError:
        speak("Sorry, I did not understand that.")
        return None
    except sr.RequestError:
        speak("Speech recognition service is unavailable.")
        return None
    except Exception as e:
        speak(f"An error occurred: {e}")
        print(f"Error: {e}")
        return None

def play_music(song_name=None) -> None:
    """Plays music from the user's Music directory."""
    song_dir = os.path.expanduser("~\\Music")
    songs = os.listdir(song_dir)

    if song_name:
        songs = [song for song in songs if song_name.lower() in song.lower()]

    if songs:
        song = random.choice(songs)
        os.startfile(os.path.join(song_dir, song))
        speak(f"Playing {song}.")
        print(f"Playing {song}.")
    else:
        speak("No song found.")
        print("No song found.")

def set_name() -> None:
    """Sets a new name for the assistant."""
    speak("What would you like to name me?")
    name = takecommand()
    if name:
        with open("assistant_name.txt", "w") as file:
            file.write(name)
        speak(f"Alright, I will be called {name} from now on.")
    else:
        speak("Sorry, I couldn't catch that.")

def load_name() -> str:
    """Loads the assistant's name from a file, or uses a default name."""
    try:
        with open("assistant_name.txt", "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return "Jarvis"  # Default name


def search_wikipedia(query):
    """Searches Wikipedia and returns a summary."""
    try:
        speak("Searching Wikipedia...")
        result = wikipedia.summary(query, sentences=2)
        speak(result)
        print(result)
    except wikipedia.exceptions.DisambiguationError:
        speak("Multiple results found. Please be more specific.")
    except Exception:
        speak("I couldn't find anything on Wikipedia.")

def open_ai_website(name: str) -> None:
    """Opens AI websites in the default browser."""
    ai_sites = {
        "chatgpt": "https://chat.openai.com",
        "gemini": "https://gemini.google.com",
        "perplexity": "https://www.perplexity.ai"
    }
    
    try:
        if name in ai_sites:
            wb.open_new_tab(ai_sites[name])
            speak(f"Opening {name} in your browser")
        else:
            speak(f"Sorry, I don't know how to open {name}")
    except Exception as e:
        speak(f"Error opening {name}: {e}")


def internet_speed_test() -> None:
    """Performs an internet speed test and announces the results."""
    speak("Checking internet speed, please wait.")
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        download = st.download()
        upload = st.upload()
        ping = st.results.ping

        download_speed = download / 1_000_000  # Convert to Mbps
        upload_speed = upload / 1_000_000      # Convert to Mbps

        result = (f"Download speed is {download_speed:.2f} megabits per second, "
                  f"upload speed is {upload_speed:.2f} megabits per second, "
                  f"and ping is {ping:.0f} milliseconds.")
        speak(f"Download speed is {download_speed:.2f} megabits per second.")
        speak(f"Upload speed is {upload_speed:.2f} megabits per second.")
        speak(f"Ping is {ping:.0f} milliseconds.")

        print(result)
    except Exception as e:
        speak("Sorry, I couldn't perform the speed test.")
        print(f"Speed test error: {e}")



if __name__ == "__main__":
    wishme()

    while True:
        query = takecommand()
        if not query:
            continue

        if "time" in query:
            time()
            
        elif "date" in query:
            date()

        elif "wikipedia" in query:
            query = query.replace("wikipedia", "").strip()
            search_wikipedia(query)

        elif "play music" in query:
            song_name = query.replace("play music", "").strip()
            play_music(song_name)

        elif "open youtube" in query:
            wb.open("youtube.com")
            
        elif "open google" in query:
            wb.open("google.com")

        elif "change your name" in query:
            set_name()

        elif "screenshot" in query:
            screenshot()
            speak("I've taken screenshot, please check it")

        elif "tell me a joke" in query:
            joke = pyjokes.get_joke()
            speak(joke)
            print(joke)

        elif "shutdown" in query:
            speak("Shutting down the system, goodbye!")
            os.system("shutdown /s /f /t 1")
            break
            
        elif "restart" in query:
            speak("Restarting the system, please wait!")
            os.system("shutdown /r /f /t 1")
            break
            
        elif "offline" in query or "exit" in query:
            speak("Going offline. Have a good day!")
            break
            
        elif "open chatgpt" in query or "chat gpt" in query:
            open_ai_website("chatgpt")
            
        elif "open gemini" in query:
            open_ai_website("gemini")
            
        elif "open perplexity" in query:
            open_ai_website("perplexity")
        
        elif "internet speed" in query or "speed test" in query:
            internet_speed_test()
        else:
            speak("Sorry, I didn't understand that.")
            print("Sorry, I didn't understand that.")


            
    