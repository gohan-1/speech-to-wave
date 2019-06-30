import speech_recognition as sr
r=sr.Recognizer()

with sr.Microphone() as source:
    print("speek anything")
    audio=r.listen(source)

    try:
        text=r.recognize_google(audio)
        print("your word is {}",format(text))
        List_of_words=list(text)
        count=len(List_of_words)
        print(count)
    except:
        print("sorry can't recognize the audio ")