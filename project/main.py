import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import time
import subprocess
from ecapture import ecapture as ec
import wolframalpha
import json
import requests
import goslate


gs = goslate.Goslate()

print('Accendendo sium')

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', 'voices[2].id')


def speak(text):
    engine.say(text)
    engine.runAndWait()


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Sto ascoltando...')
        audio = r.listen(source)

        try:
            statement = r.recognize_google(audio, language='en-EN')
            print(f'user ha detto:{statement}\n')

        except Exception as e:
            speak('Scusa, non ho capito bene')
            return 'None'
        return statement


def wishMe():
    hour = datetime.datetime.now().hour
    if hour >= 0 and hour < 12:
        speak('Ciao, buongiorno, come va?')
    elif hour >= 12 and hour < 18:
        speak('Ciao, buon pomeriggio, come va?')
    else:
        speak('Ciao, buona serata, come stai?')

    response = takeCommand()
    if 'good' in response or 'fine' in response or 'tiramu' in response:
        speak('Mi fa piacere')

    elif 'bad' in response or 'not so good' in response:
        speak('Mi dipiace')


speak('Io sono Gea, il tuo assistente personale. Sono programmato per eseguire piccole funzoni come'
      'aprire youtube,google chrome, gmail and stackoverflow, cercare su wikipedia'
      'dire le condizioni atmosferiche in diverse città , dire i titoli delle diverse notizie e puoi anche chiedermi domande di carattere scientifico e geografico!')
wishMe()


if __name__ == '__main__':

    while True:
        speak('Come posso aiutarti adesso?')
        statement = takeCommand().lower()
        if statement == 0:
            continue

        if 'good bye' in statement or 'ok bye' in statement or 'stop' in statement:
            speak('adesso mi spengo, addio.')
            break

        if 'wikipedia' in statement:
            speak('Cercando su wikipedia...')
            statement = statement.replace('wikipedia', '')

            try:
                results = wikipedia.summary(statement, sentences=3)
                speak('Secondo wikipedia')
                speak(results)
            except:
                speak('Devi cercare qualcosa')

        elif 'open youtube' in statement:
            webbrowser.open_new_tab('https://www.youtube.com')
            speak('youtube is open now')
            time.sleep(5)

        elif 'open google' in statement:
            webbrowser.open_new_tab('https://www.google.com')
            speak('Google chrome is open now')
            time.sleep(5)

        elif 'open gmail' in statement:
            webbrowser.open_new_tab('gmail.com')
            speak('Gmail si sta aprendo')
            time.sleep(5)

        elif 'weather' in statement:
            api_key = '8ef61edcf1c576d65d836254e11ea420'
            base_url = 'https://api.openweathermap.org/data/2.5/weather?'
            speak('qual è il nome della città')
            city_name = takeCommand()
            complete_url = base_url+'appid='+api_key+'&q='+city_name
            response = requests.get(complete_url)
            x = response.json()
            if x['cod'] != '404':
                y = x['main']
                current_temperature = y['temp']
                current_humidiy = y['humidity']
                z = x['weather']
                weather_description = z[0]['description']
                speak(' La temperatura in celsius è ' +
                      str(current_temperature - 274) +
                      "\n l'umidità in percentuale " +
                      str(current_humidiy) +
                      "\n descrizione  " +
                      str(weather_description))
            else:
                speak(' Non ho trovato la città ')

        elif 'who are you' in statement or 'what you can do' in statement or 'introduce' in statement:
            speak('Io sono Gea, il tuo assistente personale. Sono programmato per eseguire piccole funzoni come'
                  'aprire youtube,google chrome, gmail and stackoverflow, cercare su wikipedia'
                  'dire le condizioni atmosferiche in diverse città , dire i titoli delle diverse notizie e puoi anche chiedermi domande di carattere scientifico e geografico!')

        elif 'who built you' in statement or 'who created you' in statement or 'chi ti ha scoperta' in statement or 'chi ti ha costruito' in statement or 'chi ti ha creato' in statement or 'chi ti ha scoperto' in statement:
            speak(
                'Sono stata costruita da Mirthula e riprogrammata dalla quinta B osa, sti napoletani')

        elif 'open stackoverflow' in statement:
            webbrowser.open_new_tab('https://stackoverflow.com/login')

        elif 'what happened today' in statement:
            news = webbrowser.open_new_tab(
                'https://www.lametino.it//home/headlines')
            time.sleep(6)

        elif 'search' in statement:
            statement = statement.replace('cerca', '')
            webbrowser.open_new_tab(statement)
            time.sleep(5)

        elif 'chiedi' in statement:
            speak(
                'posso rispondere alle domande di carattere scientifico e geografico che chiedi')
            question = takeCommand()
            translatedText = gs.translate(question, 'en')
            app_id = 'R2K75H-7ELALHR35X'
            client = wolframalpha.Client('R2K75H-7ELALHR35X')
            res = client.query(question)
            answer = next(res.results).text
            speak(answer)

        elif 'close the pc' in statement or 'chiudi il pc' in statement:
            speak(
                'è stato un piacere, il tuo pc si autodistruggerà tra 10 secondi; esci da tutte quante le applicazioni o ti uccido')
            subprocess.call(['shutdown', '/l'])

time.sleep(3)
