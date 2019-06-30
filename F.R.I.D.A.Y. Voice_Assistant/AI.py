import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import smtplib
#for news feeds
import bs4
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen


#system paths
chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
music_dir = 'D:/MP3 SONGS/Music'
code_dir = "C:\\Users\\Abhiman\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
#print(voices[1].id)
engine.setProperty('voice',voices[1].id) 

#contact dictnary
#Before using email fucntionallity firstly change setting of yourEmail@gmail.com to allow less secure app to accesss

dict = {
    'abhishek' : 'abhie8101@gmail.com',
    'nitika' : 'nitikagupta208@gmail.com'
}

def getmail(str):
    if str in dict:
        return dict[str]



def wishme():
    hour = int(datetime.datetime.now().hour)
    if hour >=1 and hour < 12:
        speak("Hello Good Morning")
    elif hour >= 12 and hour <18:
        speak("Hello Good Afternoon")
    else:
        speak("Hello Good Evening")
    speak("i am friday,your personal voice assitant")
    speak("please tell what to do for you ...")


def news():    
    news_url="https://news.google.com/news/rss"
    Client=urlopen(news_url)
    xml_page=Client.read()
    Client.close()

    soup_page=soup(xml_page,"xml")
    news_list=soup_page.findAll("item")
    # Print news title, url and publish date
    for i in range(6):
        speak(news_list[i].title.text)
        print(news_list[i].title.text)        
        print(news_list[i].link.text)
        print(news_list[i].pubDate.text)
        print("-"*60)



def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening.......")
        r.adjust_for_ambient_noise(source)
        r.pause_threshold = 1.0
        audio = r.listen(source)

    try:
        print("Recognizing....")
        query = r.recognize_google(audio, language= 'en-in')
        print("You said :"+ query)

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        speak("i did not hear anything sir...please set your microphone or say clearly..")
        query = takeCommand()
    except sr.RequestError as e:
        speak("sorry sir , i think your internet is not working properly")
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        query = takeCommand()

    if query is None:
        speak("i did not hear anything sir...please set your microphone or say clearly..")
        query = takeCommand()
    return query

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def sendMail(to,content):
    data = content
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.login('yourEmail@gmail.com','YourPassWord')
    server.sendmail('yourEmail@gmail',to,data)
    server.close()

if __name__ == "__main__":
    wishme()
    while True:
        print("say command list for all commands")            
        query = takeCommand().lower()
        speak("performing.....")
        #logic for wikipedia
        if 'wikipedia' in query:
            speak("Searching wiki...")
            query = query.replace("wikipedia" , "")
            result = wikipedia.summary(query,sentences = 2)
            print(result)
            speak("According to wikipedia")
            speak(result)

        elif 'google' in query:
            speak("googling...sir...")
            query = query.replace('google' ,'')
            url = 'https://www.google.com/search?q=' + query
            webbrowser.get(chrome_path).open(url)            

        #logic for web engine      
        elif 'open youtube' in query:
            webbrowser.get(chrome_path).open("youtube.com")
      
        #elif 'open google' in  query:
            #webbrowser.get(chrome_path).open("google.com")   not workable as google searching function is also used..         

        elif 'open stackoverflow' in  query:
            webbrowser.get(chrome_path).open("stackoverflow.com")            

        elif 'open codechef' in  query:
            webbrowser.get(chrome_path).open("codechef.com")            

        elif 'open github' in  query:
            webbrowser.get(chrome_path).open("github.com")  

        elif 'open wikipedia' in  query:
            webbrowser.get(chrome_path).open("wikipedia.com")            



        #logic for music

        elif 'play music' in query:
            songs = os.listdir(music_dir)
            os.startfile(os.path.join(music_dir,songs[0]))

        # logic for exit 
        elif 'goodbye' in query:
            speak("goodbye sir...")
            speak("it was nice to work with you ... thank you")
            quit()    



        elif 'send email' in query:
            print("who is the reciver of mail.")
            speak("who is the reciver of mail.")
          
            to = takeCommand().lower()
            reciver = getmail(to)

            print("what i supposed to say in mail...")
            speak("what should  say in mail")
            content = takeCommand()               
            print("recivers email address :")
            print(reciver)
            print("content of mesg :")
            print(content)
            sendMail(reciver,content)

        elif 'command list' in query:
            print("use following command for tasks:")
            print("1.wikipedia query : for wikipedia search user anyword instead of query")    
            print("2.google query : for google search page for query")    
            print("3.open youtube : to open youtube in chrome")
            print("4.open stackoverflow : to open stackoverflow in chrome ")
            print("5.open codechef : ")
            print("6.open github :")
            print("7.play music")
            print("8.open code ")
            print("9.goodbye : for exit")
            print("10.send email : for sending email")
            print("11.news feeds or news :for latest news")

        #news feed logic
        elif 'news' or 'news feeds' in query:
            speak("getting latest news feeds.....")
            news()

        else:
            print("sir didn't get it what you say , please use a valid command")
            speak("sir didn't get it what you say , please use a valid command")      

            

 
