import tkinter as tkr
from tkinter import *

def togglefunc(flip):
	return not flip
global bHops
bHops = 0
global bradar
bradar = 0
global baimbot
baimbot = 0
global iid
iid = 0
global btriggerbot
btriggerbot = 0

def toggleHops():
	global bHops
	bHops = togglefunc(bHops)
	toggleBhop['text'] = ("BHOP: "+ str(int(bHops)))

def toggleRadarb():
	global bradar
	bradar = togglefunc(bradar)
	toggleRadar['text'] = ("RADAR: "+ str(int(bradar)))

def toggleAimbotb():
	global baimbot
	baimbot = togglefunc(baimbot)
	toggleAimbot['text'] = ("AIMBOT: "+ str(int(baimbot)))

def toggleTriggerbotb():
	global btriggerbot
	btriggerbot = togglefunc(btriggerbot)
	toggleTriggerbot["text"] = ("TRIGGERBOT: "+ str(int(btriggerbot)))

app = tkr.Tk()
app.title("invis window")
app.wm_overrideredirect(1)
app.geometry("130x250+0+500")
app.resizable(False, False)
app.attributes("-alpha", 0.9)
app.attributes('-topmost', True)
#bhop button
toggleBhop = tkr.Button(app, text=("BHOP: "+ str(int(bHops))), command=toggleHops, padx=40)
toggleBhop.place(x=0, y=0)
#radar button
toggleRadar = tkr.Button(app, text=("RADAR: "+ str(int(bradar))), command=toggleRadarb, padx=38)
toggleRadar.place(x=0, y=25)
#aimbot button
toggleAimbot = tkr.Button(app, text=("AIMBOT: "+ str(int(baimbot))), command=toggleAimbotb, padx=38)
toggleAimbot.place(x=0, y=50)
#triggerbot button
toggleTriggerbot = tkr.Button(app, text=("TRIGGERBOT: "+ str(int(btriggerbot))), command=toggleTriggerbotb, padx=30)
toggleTriggerbot.place(x=0, y=75)
#fov slider
fovEntry = tkr.Scale(app, orient=HORIZONTAL, from_=30, to_=160)
fovEntry.place(x=0, y=100)
#fov text
labelFov = tkr.Label(app, text="FOV:")
labelFov.place(x=0, y=100)
#aimbot fov range slider
aimScale = tkr.Scale(app, orient=HORIZONTAL, from_=1, to_=180)
aimScale.place(x=0, y=155)
#aimbot fov text
labelFov = tkr.Label(app, text="Aim FOV:")
labelFov.place(x=0, y=135)
app.update_idletasks()
