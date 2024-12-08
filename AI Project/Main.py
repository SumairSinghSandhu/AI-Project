import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from openai import OpenAI

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = ""


def speak(text):
    engine.say(text)
    engine.runAndWait()

def aiProcess(command):
    client = OpenAI(
    api_key= "",
)

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a virtual assistant skilled in general tasks like Alexa and Google Cloud."},
        {
            "role": "user",
            "content": command
        }
    ]
)

    return completion.choices[0].message.content

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open github" in c.lower():
        webbrowser.open("https://github.com/")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open chatgpt" in c.lower():
        webbrowser.open("https://chatgpt.com/")
    elif "open netflix" in c.lower():
        webbrowser.open("https://www.netflix.com/")

    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)

    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
        if r.status_code == 200:
            data = r.json()
        # Extract and print headlines
            articles = data.get('articles',[])
            for article in articles:
                speak(article['title'])

    else:
        output = aiProcess(c)
        speak(c)


if __name__=="__main__":
    speak("Hii how may I help you today")
    while True:

    # obtain audio from the microphone
        r = sr.Recognizer()

        print("Recognizing..")
        # recognize speech using Sphinx
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source)#, timeout=2,phrase_time_limit=1)
            word = r.recognize_google(audio)
            if(word.lower()=="matrix"):
                speak("Yes")
                # Listen for command
                with sr.Microphone() as source:
                    print("Matrix Active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    processCommand(command)

        except Exception as e:
            print("Error; {0}".format(e))
