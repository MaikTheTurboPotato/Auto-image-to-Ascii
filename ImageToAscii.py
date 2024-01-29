import subprocess
import threading
import os
import sys
import time
import imghdr
import customtkinter as cmtk
from CTkColorPicker import *
from tkinter import filedialog
import colorsys

# Logic
# =========================================================================
Loop = False; BraileChar = False; NormalChar = True; ComplexChar = False; FullScale = False;
Whith = 100; Height = 50; OutputInFile = False; ImputPath = ""; OutputPath = ""; OutputName = "AsciiOutput"; 
Color = "255,255,255"; TimeDelay = 0.01; Stop = False; Dynamic = True; ColorOriginal = False; ColorInvert = False; ColorBackground = False; ColorRainbow = False; nextColor = 0; NumColores = 100
CLEARBASHLINE = "\033[1A\x1b[2K"
FRAMES = []

localFolder = os.path.dirname(os.path.abspath(sys.argv[0]))
folder = "ascii-image-converter_Windows_amd64_64bit"
exe = "ascii-image-converter.exe"
exePath = os.path.join(localFolder, folder, exe)
if not os.path.exists(exePath):
    print("   Problem with path: Could not find '" + exe + "'")
    print("   Make sure that the file is in the directory: '" + folder  + "'")
    
    time.sleep(5)
    sys.exit() 


def GetAscii(Filepath):
    global Whith, Height, nextColor, Color
    # bash comand + Image path
    #Filepath.replace("\\", "\\\\")
    Filepath = '"'+Filepath+'"'
    try:
        Whith = int(EntryWhith.get())
    except ValueError:
        Whith = 100
    try:
        Height = int(EntryHeight.get())
    except ValueError:
        Height = 50
        
    if ColorRainbow:
        Color = nextRainowColor(nextColor)
        nextColor = (nextColor+1)%NumColores
    
    # MAKE BASH COMAND
    comando_bash = exePath+" "+Filepath+" "
    if(not OutputInFile): 
        if(ColorOriginal): 
                    comando_bash += "--color "
        else:       comando_bash +=f"--font-color {Color} "
        if(ColorInvert):
                    comando_bash += "-n "
        if(ColorBackground):
                    comando_bash += "--color-bg "
    if(BraileChar): comando_bash += "-b "
    if(ComplexChar):comando_bash += "-c "
    if(FullScale):  comando_bash += "--full "
    else:           comando_bash +=f"-d {Whith},{Height}"
    
    resultado = subprocess.run(comando_bash, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')
    # Imprime la salida de Bash
    if(Dynamic): printFrameBash(resultado.stdout,Height)
    # Save on variable
    FRAMES.append(resultado.stdout)


def nextRainowColor(index):
    hue = index / float(NumColores)
    r, g, b = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
    return f'{int(r * 255)},{int(g * 255)},{int(b * 255)}'

def startButton():
    global Stop
    StartButton.configure(state="disabled")
    StopButton.configure(state="normal")
    Stop = False;
    hilo = threading.Thread(target=printFrames)
    hilo.start()
def stopButton():
    global Stop
    Stop = True;
    
def printFrames():
    global TimeDelay, Dynamic, FRAMES, Stop
    #folder = r"C:\Users\mique\Desktop\pepis\Frames"
    if(ImputPath == ""):
        return
    images = os.listdir(ImputPath)
    
    while not Stop:
        FRAMES = []
        if OutputInFile: saveFrame("",True) # Creal the output file if created, create it if not exits
        for image in images:
            path = os.path.join(ImputPath, image)
            if os.path.isfile(path) and imghdr.what(path): #Is a file and an image
                GetAscii(path)
                
            if Dynamic:
                try:
                    TimeDelay = float(EntryDelay.get())
                except ValueError:
                    TimeDelay = 0.01
                time.sleep(TimeDelay)
                
            if OutputInFile:
                saveFrame(FRAMES[-1])
            
            if(Stop): break
                
        if(not Dynamic or not Loop): break
        
    if Dynamic: 
        StartButton.configure(state="normal")
        StopButton.configure(state="disabled")
        return
    
    while not Stop:
        for frame in FRAMES:
            try:
                TimeDelay = float(EntryDelay.get())
            except ValueError:
                TimeDelay = 0.01
                
            printFrameBash(frame, Height)
            time.sleep(TimeDelay)
            if(Stop): break
            if(Dynamic): break
        if(Dynamic):break
        if(not Loop): break
    if(Dynamic): printFrames()
    
    StartButton.configure(state="normal")
    StopButton.configure(state="disabled")
        
def printFrameBash(Frame, Height):
    print(CLEARBASHLINE*(Height*2))
    print(Frame)

def saveFrame(Frame, override=False):
    global OutputName
    if OutputPath == "": return
    if OutputName.get() == "": EntryOUTPUTNAME.insert(0,"AsciiOutput")
    
    if not os.path.exists(OutputPath):
        os.makedirs(OutputPath)
    fullPath = os.path.join(OutputPath, OutputName.get()+".txt")
    # Save output
    if override:
        with open(fullPath, "w", encoding="utf-8") as archivo:
            archivo.write(Frame)
    else:
        with open(fullPath, "a", encoding="utf-8") as archivo:
            archivo.write(Frame + "\n\n")
#----------------------------------------------------------------
# UI Widgets actions
def searchFolderImput():
    global ImputPath
    ImputPath = filedialog.askdirectory(title='Frames folder').replace("/", "\\")
    PathFOLDER.delete(0, cmtk.END)
    PathFOLDER.insert(0,str(ImputPath))
    StartButton.configure(state="normal")
    printState()
def searchFolderOutput():
    global OutputPath
    OutputPath = filedialog.askdirectory(title='Frames folder').replace("/", "\\")
    PathOUTPUTFOLDER.insert(0,str(OutputPath))
    printState()
def ask_color(color):
    global Color
    Color = hex_to_rgb_string(color)
    #printState()
def hex_to_rgb_string(hex_color):
    hex_color = hex_color.lstrip('#')  # Eliminar el posible caracter '#' al inicio
    rgb_values = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    return f"{rgb_values[0]},{rgb_values[1]},{rgb_values[2]}"

def checkLoop():
    global Loop
    Loop = not Loop
    printState()
def checkStyle():
    global BraileChar, ComplexChar, NormalChar, ComplexChar
    NormalChar = False; BraileChar = False; ComplexChar = False; 
    match StyleRadioVar.get():
        case 1:
            NormalChar = True
        case 2:
            BraileChar = True
        case 3:
            ComplexChar = True 
    printState()
    
def checkInvert():
    global ColorInvert
    ColorInvert = not ColorInvert
    printState()
def checkOriginal():
    global ColorOriginal
    ColorOriginal = not ColorOriginal
    printState()
def checkBackground():
    global ColorBackground
    ColorBackground = not ColorBackground
    printState()
def checkRainbow():
    global ColorRainbow
    ColorRainbow = not ColorRainbow
    printState()
    
def checkFull():
    global FullScale
    FullScale = not FullScale
    if(not FullScale):
        EntryWhith.configure(state="normal")
        EntryHeight.configure(state="normal")
    else:
        EntryWhith.configure(state="disabled")
        EntryHeight.configure(state="disabled")
    printState()
def checkOutput():
    global OutputInFile
    OutputInFile = not OutputInFile
    '''if OutputInFile:
        colorpicker.configure(state="disabled")
    else: 
        colorpicker.configure(state="normal")'''
        
    printState()
def checkDynamic():
    global Dynamic
    Dynamic = not Dynamic
    printState()
def printState():
    print(f"Loop:{Loop}, Normal:{NormalChar}, Braile:{BraileChar}, Complex:{ComplexChar}, FullScale:{FullScale}, Whith:{EntryWhith.get()}, height:{EntryHeight.get()}")
    print(f"RGB:{Color}, ImputPath:{ImputPath}, OutputPath:{OutputPath}, OutputInFile:{OutputInFile}")
    
# GUI
# =========================================================================
cmtk.set_appearance_mode("dark")
cmtk.set_default_color_theme("dark-blue")

root = cmtk.CTk()
root.geometry("675x525")

frame = cmtk.CTkFrame(master=root)
frame.pack(pady=10, padx=10, fill="both", side="left", expand=True)
fontBold16 = cmtk.CTkFont(family="Helvetica", size=16, weight="bold")
fontBold12 = cmtk.CTkFont(family="Helvetica", size=12, weight="bold")

#----------------------------------------------------------------
# Path folder
frameFOLDER = cmtk.CTkFrame(master=frame)
frameFOLDER.pack(pady=2, padx=5, fill="both", expand=False)
LabelFOLDER = cmtk.CTkLabel(master=frameFOLDER, text="Browser folder with frames", font=fontBold16)
LabelFOLDER.pack(pady=2, padx=10)
ButtonBrowse = cmtk.CTkButton(master=frameFOLDER, text="Browse", width=75, font=fontBold12, command=searchFolderImput)
ButtonBrowse.pack(pady=12, padx=10, side="left")
PathFOLDER = cmtk.CTkEntry(master=frameFOLDER, placeholder_text="C:\\FilePath", width=300)
PathFOLDER.pack(pady=12, padx=15, side="left")

#----------------------------------------------------------------
# SETTINGS
frameSETTINGS = cmtk.CTkFrame(master=frame)
frameSETTINGS.pack(pady=2, padx=5, fill="both", expand=False)
LabelSETTINGS = cmtk.CTkLabel(master=frameSETTINGS, text="Settings", font=fontBold16)
LabelSETTINGS.grid(row=0, column=1, padx=10, pady=5)

# Row1
pady = 15
CheckBoxLoop = cmtk.CTkCheckBox(master=frameSETTINGS, text="Loop", command=checkLoop)
CheckBoxLoop.grid(row=1, column=0, padx=10, pady=pady)
LabelDelay = cmtk.CTkLabel(master=frameSETTINGS, text="Delay", font=fontBold12)
LabelDelay.grid(row=1, column=1, padx=10, pady=pady, sticky="W")
EntryDelay = cmtk.CTkEntry(master=frameSETTINGS, placeholder_text="0.01", width=65)
EntryDelay.grid(row=1, column=1, padx=10, pady=pady, sticky="E")
CheckVar = cmtk.IntVar(value=1)
CheckBoxDynamic = cmtk.CTkCheckBox(master=frameSETTINGS, text="Dynamic", variable = CheckVar, command=checkDynamic)
CheckBoxDynamic.grid(row=1, column=2, padx=10, pady=pady)

# Row2
StyleRadioVar = cmtk.IntVar()
CheckBoxNormal = cmtk.CTkRadioButton(frameSETTINGS, text="Normal ascii", command=checkStyle, variable=StyleRadioVar, value=1)
CheckBoxNormal.grid(row=2, column=0, padx=10, pady=pady)
CheckBoxBraile = cmtk.CTkRadioButton(frameSETTINGS, text="Braile ascii", command=checkStyle, variable=StyleRadioVar, value=2)
CheckBoxBraile.grid(row=2, column=1, padx=10, pady=pady)
CheckBoxComplex = cmtk.CTkRadioButton(frameSETTINGS, text="Complex ascii", command=checkStyle, variable=StyleRadioVar, value=3)
CheckBoxComplex.grid(row=2, column=2, padx=10, pady=pady)

# Row3
#CheckBoxFull = cmtk.CTkCheckBox(master=frameSETTINGS, text="Full scale", command=checkFull)
#CheckBoxFull.grid(row=3, column=0, padx=10, pady=pady)

LabelWhith = cmtk.CTkLabel(master=frameSETTINGS, text="Whith", font=fontBold12)
LabelWhith.grid(row=3, column=0, padx=10, pady=pady, sticky="W")
EntryWhith = cmtk.CTkEntry(master=frameSETTINGS, placeholder_text="100", width=65)
EntryWhith.grid(row=3, column=0, padx=10, pady=pady, sticky="E")

LabelHeight = cmtk.CTkLabel(master=frameSETTINGS, text="Height", font=fontBold12)
LabelHeight.grid(row=3, column=1, padx=10, pady=pady, sticky="W")
EntryHeight = cmtk.CTkEntry(master=frameSETTINGS, placeholder_text="50", width=65)
EntryHeight.grid(row=3, column=1, padx=10, pady=pady, sticky="E")

#----------------------------------------------------------------
# Output Path folder
frameOUTPUTFOLDER = cmtk.CTkFrame(master=frame)
frameOUTPUTFOLDER.pack(pady=2, padx=5, fill="both", expand=False)
LabelOUTPUTFOLDER = cmtk.CTkLabel(master=frameOUTPUTFOLDER, text="Output ascii text into file", font=fontBold16)
LabelOUTPUTFOLDER.grid(row=0, column=0, columnspan=2, padx=10, pady=5)

CheckBoxFull = cmtk.CTkCheckBox(master=frameOUTPUTFOLDER, text="Output text?", command=checkOutput)
CheckBoxFull.grid(row=1, column=0, padx=10, pady=5)

PathOUTPUTNAME = cmtk.CTkLabel(master=frameOUTPUTFOLDER, text="Output mame", font=fontBold12)
PathOUTPUTNAME.grid(row=2, column=0, padx=10, pady=5, sticky="W")
OutputName = cmtk.StringVar()
EntryOUTPUTNAME = cmtk.CTkEntry(master=frameOUTPUTFOLDER, placeholder_text="AsciiOutput", textvariable=OutputName,width=200)
EntryOUTPUTNAME.grid(row=2, column=1, padx=10, pady=5, sticky="W")
EntryOUTPUTNAME.insert(0,"AsciiOutput")

ButtonOUTPUTBrowse = cmtk.CTkButton(master=frameOUTPUTFOLDER, text="Browse", width=75, font=fontBold12, command=searchFolderOutput)
ButtonOUTPUTBrowse.grid(row=3, column=0, padx=10, pady=5, sticky="W")
PathOUTPUTFOLDER = cmtk.CTkEntry(master=frameOUTPUTFOLDER, placeholder_text="C:\\FilePath", width=250)
PathOUTPUTFOLDER.grid(row=3, column=1, padx=10, pady=5, sticky="W")

#----------------------------------------------------------------
# Terminal ASCII COLOR
frameCOLOR = cmtk.CTkFrame(master=root)
frameCOLOR.pack(pady=2, padx=5, fill="both", side="right", expand=False)
LabelColor = cmtk.CTkLabel(master=frameCOLOR, text="Terminal ascii color", font=fontBold16)
LabelColor.grid(row=0, column=0, padx=10, pady=5, sticky="W")
colorpicker = CTkColorPicker(frameCOLOR, width=250, orientation="horizontal", command=ask_color)
colorpicker.grid(row=1, column=0, padx=10, pady=5, sticky="W")

CheckBoxoriginal = cmtk.CTkCheckBox(frameCOLOR, text="Original Colors", command=checkOriginal)
CheckBoxoriginal.grid(row=2, column=0, padx=10, pady=5, sticky="W")
CheckBoxInvert = cmtk.CTkCheckBox(frameCOLOR, text="Invert Color", command=checkInvert)
CheckBoxInvert.grid(row=3, column=0, padx=10, pady=5, sticky="W")
CheckBoxBackground = cmtk.CTkCheckBox(frameCOLOR, text="Color in Background", command=checkBackground)
CheckBoxBackground.grid(row=4, column=0, padx=10, pady=5, sticky="W")
CheckBoxRainbow = cmtk.CTkCheckBox(master=frameCOLOR, text="Rainbow", command=checkRainbow)
CheckBoxRainbow.grid(row=5, column=0, padx=10, pady=5, sticky="W")

#----------------------------------------------------------------
# START BUTTON
frameBUTTONS = cmtk.CTkFrame(master=frame)
frameBUTTONS.pack(pady=2, padx=5, fill="both", side="right", expand=True)
StartButton = cmtk.CTkButton(master=frameBUTTONS, text="Start", command=startButton) #(SpamEntry.text, DelayEntry.text)
StartButton.pack(pady=12, padx=10, side="left")
StartButton.configure(state="disabled")
StopButton = cmtk.CTkButton(master=frameBUTTONS, text="Stop", command=stopButton) #(SpamEntry.text, DelayEntry.text)
StopButton.pack(pady=12, padx=10, side="right")
ButtonColor = "#d8241b"
StopButton.configure(fg_color=ButtonColor)
StopButton.configure(state="disabled")


root.mainloop()
