from tkinter import *
from random import *
import pyowm
import time

def main():
    UserCoordinatX, UserCoordinatY = 55.553236, 37.552202
    DataOfSlopeInformation = LoadingAndReturnInformation(UserCoordinatX, UserCoordinatY)
    return GetInformationsOfSlopes(DataOfSlopeInformation)  

def LoadingAndReturnInformation(UserCoordinatX, UserCoordinatY):
    global CounterOfSlopes
    LI = PhotoImage(file="LoadingImage.gif")
    LoadingImage = canvas.create_image(_width // 2, _height // 2, image=LI)
    LoadingText = canvas.create_text(_width // 2,_height // 2,text="iSki Russia",font="Verdana 30", fill="red")
    LoadingPanelContur = canvas.create_rectangle(0, _height - 25, _width + 1, _height + 1, fill="white", outline="white")
    LoadingPanelFill = canvas.create_rectangle(0, _height - 25, 0, _height + 1, fill="green", outline="green")
    canvas.pack()
    DataOfSlopeInformation = []
    DataOfSlopesTxt = open("DataOfSlopes.txt")
    CounterOfSlopes = int(DataOfSlopesTxt.readline())
    for i in range(1, _width + 2):
        canvas.delete(LoadingPanelFill)
        if i <= CounterOfSlopes:
            help = list(DataOfSlopesTxt.readline().split())
            SlopeX, SlopeY = float(help[1]), float(help[2])
            DataOfSlopeInformation.append((distance(UserCoordinatX, UserCoordinatY, SlopeX, SlopeY), help[0], SlopeX, SlopeY))
        LoadingPanelFill = canvas.create_rectangle(0, _height - 25, i, _height + 1, fill="green", outline="green")
        canvas.update()
    DataOfSlopesTxt.close()
    DataOfSlopeInformation.sort()
    canvas.delete(LoadingPanelFill, LoadingPanelContur, LoadingText)
    return DataOfSlopeInformation

def GetInformationsOfSlopes(DataOfSlopeInformation):
    DataOfRectangle = [None for i in range(CounterOfSlopes)]
    DataOfText = [None for i in range(CounterOfSlopes)]
    DataOfRectangleCoordinatsAndText = [None for i in range(CounterOfSlopes)]
    DataOfRectangleCoordinatsAndText[0] = [10, 10, _width // 2 - 20, 60, DataOfSlopeInformation[0][1], DataOfSlopeInformation[0][2], DataOfSlopeInformation[0][3]] 
    for i in range(1, CounterOfSlopes):
        DataOfRectangleCoordinatsAndText[i] = [10, DataOfRectangleCoordinatsAndText[i - 1][1] + 60, _width // 2 - 20, DataOfRectangleCoordinatsAndText[i - 1][3] + 60, DataOfSlopeInformation[i][1], DataOfSlopeInformation[i][2], DataOfSlopeInformation[i][3]]
    for i in range(CounterOfSlopes):
        DataOfRectangle[i] = canvas.create_rectangle(DataOfRectangleCoordinatsAndText[i][0], DataOfRectangleCoordinatsAndText[i][1], DataOfRectangleCoordinatsAndText[i][2], DataOfRectangleCoordinatsAndText[i][3], fill="white")
        DataOfText[i] = canvas.create_text((DataOfRectangleCoordinatsAndText[i][0] + DataOfRectangleCoordinatsAndText[i][2]) // 2, DataOfRectangleCoordinatsAndText[i][1] + 10, text=DataOfSlopeInformation[i][1], font="Verdana 11")
    InformationScreen = canvas.create_rectangle(_width // 2, 10, _width - 10, 125, fill="white")
    return DataOfRectangleCoordinatsAndText
    
def distance(x, y, x1, y1):
    return ((x - x1) ** 2 + (y - y1) ** 2) ** 0.5

def GetWeatherInformation(event):
    global FirstGet, DegreeInformationText, WindInformationText, AirMoistureInformationText, PressureInformationText, SkiSlopeInformationText, MouseX, MouseY, DuringIndex, Map
    MouseX, MouseY = event.x, event.y
    if FirstGet:
        canvas.delete(DegreeInformationText, WindInformationText, AirMoistureInformationText, PressureInformationText, SkiSlopeInformationText)
    for i in range(CounterOfSlopes):
        if DataOfRectangleCoordinatsAndText[i][0] <= MouseX <= DataOfRectangleCoordinatsAndText[i][2] and DataOfRectangleCoordinatsAndText[i][1] <= MouseY <= DataOfRectangleCoordinatsAndText[i][3]:
            DuringIndex = i
            break
    observation = owm.weather_at_coords(DataOfRectangleCoordinatsAndText[DuringIndex][5], DataOfRectangleCoordinatsAndText[DuringIndex][6])
    DataOfWeather = observation.get_weather() 
    DegreeInformationText = canvas.create_text(_width // 4 * 3, 20, text="{} Degree by Celsius".format(DataOfWeather.get_temperature('celsius')["temp"]), font="Verdana 12")
    WindInformationText = canvas.create_text(_width // 4 * 3, 40, text="Speed of wind: {} m/s".format(DataOfWeather.get_wind()["speed"]), font="Verdana 12")
    AirMoistureInformationText = canvas.create_text(_width // 4 * 3, 60, text="Air moisture: {}%".format(DataOfWeather.get_humidity()), font="Verdana 12")
    PressureInformationText = canvas.create_text(_width // 4 * 3, 80, text="Pressure: {} mm Hg. article".format(randint(700, 800)), font="Verdana 11")
    AreOpenSkiSlope = randint(0, 1)
    if AreOpenSkiSlope == 1:
        SkiSlopeInformationText = canvas.create_text(_width // 4 * 3, 100, text="Ski slope are open", font="Verdana 12")
    else:
        SkiSlopeInformationText = canvas.create_text(_width // 4 * 3, 100, text="Ski slope are close", font="Verdana 12")
    _image = '{}.gif'.format(DataOfRectangleCoordinatsAndText[DuringIndex][4])
    FirstGet = True


_width, _height = 500, 600
owm = pyowm.OWM('15ea7bd687a6016f005a3668bc437e09')
root = Tk()
root.title("iSkiRussia")
canvas = Canvas(root, width=_width, height=_height, bg="lightblue")
CounterOfSlopes = -1
DuringIndex = 0
DataOfRectangleCoordinatsAndText = main()
DegreeInformationText, WindInformationText, AirMoistureInformationText, PressureInformationText, SkiSlopeInformationText, Map = None, None, None, None, None, None
FirstGet = False
MouseX, MouseY = -1, -1
canvas.bind('<1>', GetWeatherInformation)
root.mainloop()