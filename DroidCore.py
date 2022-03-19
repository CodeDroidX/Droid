from tkinter import * #Основополагающий модуль
import math #Считать син\кос для езды
import random #Ну типо интеллект
import os
import threading
import ctypes
import pyautogui as gui #Делать плохие вещи
import pywinauto as wgui
import requests

import speech_recognition as recog #Распознавание речи
rec=recog.Recognizer()

#ТТС от гугла - в разы приятнее pyttsx3
#А espeak и Rhvoice это вообще исчадия ада
from gtts import gTTS as gt
#Пайдаб-это костыль для изменения тембра
from googletrans import Translator
translator = Translator() #Вроде это лишнее, но он поможет нам в распознавании языка для TTS
from pydub import AudioSegment
import simpleaudio
from pydub.playback import play #Ну, и за одно звук им проигрывать можно

def tick(mode,args):

    with open("Memory/SleepFlag.mem","r+") as f:
        now=f.read()
    if now=="Yes":
        img=PhotoImage(file=f"Sprites/Afk/1.png")#Грузим костюм
        canvas.image=img#Надо
        canvas.create_image(20,30,image=img)#Рисуем на холсте по середине
        root.after(5, lambda mode=mode,args=args: tick(mode,args))
        return None

    if mode=="ChangeMode": #Попадаем сюда тогда, когда что то закончилось
        args=[None]
        avalable_modes=7
        rand=random.randint(0,avalable_modes-1)

        #Случайный выбор - что делать дальше

        if rand==0:
            print("Running")
            mode="Run"
            args=[None]

        elif rand==1:
            print("Flying")
            mode="Fly"
            args[0]=1

        elif rand==2:
            print("Hiding")
            mode="Hide"
            args[0]=1

        elif rand==3:
            print("Listening")
            mode="Listen"
            args[0]="FirstLoop"

        elif rand==4:
            print("Typing")
            mode="Type"
            args[0]="FirstLoop"

        elif rand==5:
            print("Playing")
            mode="Play"
            args[0]="FirstLoop"

        elif rand==6:
            print("Joke")
            mode="Joke"
            args[0]="FirstLoop"
    """
        elif rand==6:
            print("Stealing")
            mode="Steal"
            args=[None]

    """
    #--------------------------------------------------Modes--------------------------------------------------



    #--------------------------------------------------Следование за мышкой
    if mode=="Run":
        x_move,y_move=20, 30#Что-бы нашими координатами считалась середина окна а не верхний правый край
        my_x,my_y=root.winfo_x()+x_move, root.winfo_y()+y_move #Абсолютные координаты центра окна
        x, y = root.winfo_pointerxy()#Абсолютные координаты мышки

        x_diff,y_diff=x-my_x,y-my_y#Дельты вышесказанных координат
        angle=GetAngle(x_diff,y_diff)#Направление к указателю в градусах

        #Всего есть 74 кадра в обороте дроида на 360
        degrees_per_costume=360/74 #Градусов в одном фрагменте поворота
        costume=math.floor(angle/(360/74))
        costume=str(costume).zfill(2)#Дополнить строку нулями

        img=PhotoImage(file=f"Sprites/Run/frame_{costume}_delay-0.03s.png")#Грузим костюм
        canvas.image=img#Надо
        canvas.create_image(x_move,y_move,image=img)#Рисуем на холсте по середине

        if (x_diff**2+y_diff**2)**0.5 >200:#Сдинемся только если дальше чем 200пкс от мыши

            root.geometry(f"+{math.ceil(my_x-x_move+(x_diff/50))}+{math.ceil(my_y-y_move+(y_diff/50))}")

        if random.randint(0,1000)==0:
            mode="ChangeMode" #Если повезет - то завершаем действие




    #--------------------------------------------------Хаотичный полет
    if mode=="Fly":
        x_move,y_move=20, 30#Что-бы нашими координатами считалась середина окна а не верхний правый край
        my_x,my_y=root.winfo_x()+x_move, root.winfo_y()+y_move #Абсолютные координаты центра окна

        if args[0]>3:
            args[0]-=3

        img=PhotoImage(file=f"Sprites/Fly/{args[0]}.png")#Грузим костюм
        args[0]+=1
        canvas.image=img#Надо
        canvas.create_image(x_move,y_move,image=img)#Рисуем на холсте по середине
        x_m=random.randint(-1,1)
        y_m=random.randint(-1,1)
        if my_x+x_m < 1920 and my_x+x_m > 0 and my_y+y_m <1080 and my_y+y_m >0:
            root.geometry(f"+{my_x-x_move+x_m}+{my_y-y_move+y_m}")

        if random.randint(0,1000)==0:
            mode="ChangeMode" #Если повезет - то завершаем действие

    #--------------------------------------------------Телепортация по экрану
    if mode=="Hide":
        x_move,y_move=20, 30#Что-бы нашими координатами считалась середина окна а не верхний правый край
        my_x,my_y=root.winfo_x()+x_move, root.winfo_y()+y_move #Абсолютные координаты центра окна

        if args[0]>5:
            args[0]-=5

        img=PhotoImage(file=f"Sprites/Hide/{args[0]}.png")#Грузим костюм
        args[0]+=1
        canvas.image=img#Надо
        canvas.create_image(x_move,y_move,image=img)#Рисуем на холсте по середине

        root.geometry(f"+{random.randint(0,1920)}+{random.randint(0,1080)}")

        if random.randint(0,1000)==0:
            mode="ChangeMode" #Если повезет - то завершаем действие

    #--------------------------------------------------Подлое подслушивание твоей речи
    if mode=="Listen":
        x_move,y_move=20, 30#Что-бы нашими координатами считалась середина окна а не верхний правый край

        img=PhotoImage(file=f"Sprites/Listen/1.png")#Грузим костюм
        canvas.image=img#Надо
        canvas.create_image(x_move,y_move,image=img)#Рисуем на холсте по середине


        if args[0]=="FirstLoop":
            args[0]="NotFirstLoop"
        else:
            text=ListenUser()
            if text!="":
                with open("Memory/Memory.mem","a+", encoding='utf-8') as f:
                    f.write("\n"+text.strip())
            mode="ChangeMode" #Завершаем действие

    #--------------------------------------------------Печать на клавиатуре чего-то из памяти
    if mode=="Type":
        x_move,y_move=20, 30#Что-бы нашими координатами считалась середина окна а не верхний правый край

        img=PhotoImage(file=f"Sprites/Type/{random.randint(1,6)}.png")#Грузим костюм
        canvas.image=img#Надо
        canvas.create_image(x_move,y_move,image=img)#Рисуем на холсте по середине

        if args[0]=="FirstLoop":
            with open("Memory/Memory.mem","r", encoding='utf-8') as f:
                data=f.readlines()
            word=random.choice(data).strip()
            while word=="":
                word=random.choice(data).strip()
            args[0]=word
        else:
            if args[0]!="":
                print(args[0][0])
                wgui.keyboard.send_keys(args[0][0], with_spaces=True)
                args[0]=args[0][1:]
            else:
                mode="ChangeMode" #Завершаем действие

    #--------------------------------------------------ОТКРЫВАЕМ БОЧКУ И НАЧИНАЕМ ОРАТЬ ДЕТСКИМ ГОЛОСОМ ЧТО КОТЛЕТКИ ГОТОВЫ
    if mode=="Play":
        x_move,y_move=20, 30#Что-бы нашими координатами считалась середина окна а не верхний правый край

        img=PhotoImage(file=f"Sprites/Play/1.png")#Грузим костюм
        canvas.image=img#Надо
        canvas.create_image(x_move,y_move,image=img)#Рисуем на холсте по середине

        if args[0]=="FirstLoop":
            with open("Memory/Memory.mem","r", encoding='utf-8') as f:
                data=f.readlines()
            word=random.choice(data).strip()
            while word=="":
                word=random.choice(data).strip()
            args[0]=say(word)
        elif not args[0].is_alive():
            mode="ChangeMode" #Завершаем действие

    #--------------------------------------------------ОТКРЫВАЕМ БОЧКУ И НАЧИНАЕМ ОРАТЬ ДЕТСКИМ ГОЛОСОМ ЧТО КОТЛЕТКИ ГОТОВЫ
    if mode=="Joke":
        x_move,y_move=20, 30#Что-бы нашими координатами считалась середина окна а не верхний правый край

        img=PhotoImage(file=f"Sprites/Readme/Info.png")#Грузим костюм
        canvas.image=img#Надо
        canvas.create_image(x_move,y_move,image=img)#Рисуем на холсте по середине

        if args[0]=="FirstLoop":
            args[0]="NotFirstLoop"
        else:
            random_chuck_norries_joke()
            mode="ChangeMode" #Завершаем действие






    root.after(2, lambda mode=mode,args=args: tick(mode,args)) #Запускаем tick с начала


def random_chuck_norries_joke():
    joke=requests.get("https://geek-jokes.sameerkumar.website/api?format=json").json()["joke"]
    joke=translator.translate(joke, dest="ru").text
    ctypes.windll.user32.MessageBoxW(0,joke, "Droid:", 0)


#По катетам пр. треугольника найти угол
#Или же найти угол направления по изменению X и Y
def GetAngle(x_diff,y_diff):
    if x_diff/50 > 0:
        dir=180 + math.degrees(math.atan((y_diff/50)/(x_diff/50)))+90
    elif x_diff/50 < 0:
        dir=math.degrees(math.atan((y_diff/50)/(x_diff/50)))+90
    elif x_diff/50==0 and y_diff/50>0:
        dir=0
    elif x_diff/50==0 and y_diff/50<0:
        dir=180
    else:
        dir=0
    return dir



def ListenUser():
    with recog.Microphone() as source:
        #rec.adjust_for_ambient_noise(source, duration=1) #Если нужно шумоподаление
        try:
            audio = rec.listen(source,timeout=10)
        except:
            return ""
    try:
        text=rec.recognize_google(audio, language="ru-RU") #Можно выбрать язык
    except:
        return ""
    return text

def lang_detect(text): #Собственно, спрашиваем у переводчика язык
    return translator.translate(text).src

def gen_wav_TTS(text):

    tts = gt(text=text,lang=lang_detect(text))
    with open("cache.mp3","wb") as fp:
        tts.write_to_fp(fp)

def say_TTS():
    octaves=0.3
    try:
        sound = AudioSegment.from_file('cache.mp3', format="mp3")
    except FileNotFoundError:
        raise FileNotFoundError("Download ffmpeg.exe,ffplay.exe into your program path, or install it in system")
    os.remove('cache.mp3')

    new_rate = int(sound.frame_rate * (2.0 ** octaves))

    new_sound = sound._spawn(sound.raw_data, overrides={'frame_rate': new_rate})

    pitched_sound = new_sound.set_frame_rate(44100)

    play(pitched_sound)

def say(text):#Обертка для say_TTS
    gen_wav_TTS(text)
    th=threading.Thread(target=say_TTS)
    th.start()
    return th
def goto_sleep(event):
    with open("Memory/SleepFlag.mem","r+") as f:
        now=f.read()
    if now!="Yes":
        with open("Memory/SleepFlag.mem","w+") as f:
            f.write("Yes")
            print("Fell asleep")
    if now=="Yes":
        with open("Memory/SleepFlag.mem","w+") as f:
            f.write("No")
            print("Wake up")





#--------------------------------------------------Main--------------------------------------------------

gui.PAUSE = 0 #По умолчанию зачем-то есть задержка перед действиями
gui.FAILSAFE = False #Не ломаться

root = Tk() #Наше окошко
root.geometry("40x60")
root.attributes('-alpha', 0.7) #Немного прозрачности
root.attributes("-topmost",True) #Поверх всех окон
root.resizable(0, 0) #Не растягиваемое
root.overrideredirect(1) #Без всякого интерфейса по типу крестика или рамки
root.wm_attributes("-transparentcolor", "blue") #Крутая фича - любой СИНИЙ пиксель будет создавать прозрачную дыру в окне

frame = Frame(root,bd=0, highlightthickness=0) #Рамки на 0, свечение рамок на 0
frame.pack()


canvas = Canvas(frame, bg="blue", width=40, height=60, borderwidth = 0, highlightthickness=0) #Тоже рамки на 0
#Задний фон будет СИНИЙ, 5 строчек назад сказано зачем.
canvas.pack()


root.bind("<Button-1>", goto_sleep)

#Всё готово к запуску главной рекурсии

root.after(2, lambda mode="Run",args=[None]: tick(mode,args))#Вот он

root.mainloop()#Запускаем приложение
