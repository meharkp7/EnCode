import speech_recognition as sr
import pyttsx3

#initilize recognizer
r=sr.Recognizer()

def record_text():
    #loop in case of errors
    while(1):
        try:
            #use the microphone as source for input 
            with sr.Microphone() as source2:
                #preparing recongniser to recieve input
                r.adjust_for_ambient_noise(source2,duration=0.3)

                #listens for the user's input
                audio2=r.listen(source2, timeout=5,phrase_time_limit=10)

                #using whisper to recogniise audio 
                MyText=r.recognize_google(audio2)

                return MyText
            
        except sr.RequestError as e:
            print("could not request results; {0}".format(e) )
        
        except sr.UnknownValueError:
            print("unknown error occurred")

def output_text(text):
    f=open("output.txt","a")
    f.write(text)
    f.write("\n")
    f.close()
    return  

while(1):
    text=record_text()
    output_text(text)
    print("wrote text")