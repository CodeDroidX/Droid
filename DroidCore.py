from tkinter import * #Основополагающий модуль
import math #Считать син\кос для езды
import random #Ну типо интеллект
import pyautogui as gui #Делать плохие вещи


def tick(mode,args):
    if mode=="ChangeMode": #Попадаем сюда тогда, когда что то закончилось
        args=[None]
        avalable_modes=2
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
        """
        elif rand==2:
            print("Hiding")
            mode="Hide"
            args=[None]

        elif rand==3:
            print("Listening")
            mode="Listen"
            args=[None]

        elif rand==4:
            print("Playing")
            mode="Play"
            args=[None]

        elif rand==5:
            print("Stealing")
            mode="Steal"
            args=[None]

        elif rand==6:
            print("Typing")
            mode="Type"
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





    root.after(5, lambda mode=mode,args=args: tick(mode,args)) #Запускаем tick с начала

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

#Всё готово к запуску главной рекурсии

root.after(2, lambda mode="ChangeMode",args=[None]: tick(mode,args))#Вот он

root.mainloop()#Запускаем приложение
