import pymem
import scanner as s
from pynput import keyboard
from pynput import mouse
import menu
from sys import exit
import math

def startup():
	global spaceHeld
	global bmenu
	global baimt
	bmenu = 3
	spaceHeld = 0
	baimt = 0
	def on_press(key):
		if key==keyboard.Key.space:
			global spaceHeld
			spaceHeld = 1
	def on_release(key):
		global bmenu 
		if key==keyboard.Key.space:
			global spaceHeld
			spaceHeld = 0
		if key==keyboard.KeyCode.from_char('['):
			bmenu = 1
		if key==keyboard.KeyCode.from_char(']'):
			bmenu = 0
	def on_click(x, y, button, pressed):
		if button == mouse.Button.x2:
			global baimt
			baimt = not baimt
	mlistener = mouse.Listener(on_click=on_click)
	listener = keyboard.Listener(on_press=on_press, on_release=on_release)
	listener.start()
	mlistener.start()

def checkMenu(bmenu):
		if bmenu == 1:
			 menu.app.deiconify()
			 bmenu = 3
		if bmenu == 0:
			 menu.app.withdraw()
			 bmenu = 3

global closestEnt
closestEnt = 0

def main():
	py = pymem.Pymem("csgo.exe")
	startup()
	menu.fovEntry.set(90)
	s.viewAngles += py.read_int(s.dwclientState)
	entCounter = 1
	closestAngle = 3637261.0
	closest = 321321.0
	while 1 == 1:
		checkMenu(bmenu)
		menu.app.update() #refreshing window (always necessary)
		localPlayer = py.read_int(s.localPlayer) #finding local player
		if not localPlayer:
			continue
		py.write_int(localPlayer + 0x332C, menu.fovEntry.get())
		flags = int(py.read_int(localPlayer + 0x104)) ## checking player collisions
		if (flags == 257 or flags == 263) and menu.bHops == True and spaceHeld == 1:
			py.write_int(s.dwForceJump, 6) # jumps
#		m_flFlashDuration = (0xA420)
#		flashvalue = py.read_float(localPlayer + m_flFlashDuration)
#		if flashvalue > 0:
	#		py.write_float(flashvalue, float(0))
		for i in range(20):
			entity = py.read_int(s.entityList + (i * 0x10)) #reading current ent in list
			if not entity or entity == localPlayer or py.read_int(entity+0x100) <= 0 or py.read_int(entity+0xF4) == py.read_int(localPlayer+0xF4): ##check for teams, nulls, dead, or ent = player
			   continue
			if menu.bradar == True: #radar button
				py.write_int(entity + 0x93D, 1) ## writing to spotted bool
			if menu.btriggerbot == True:
				m_iCrosshairId = (0xB3D4)
				entity_id = py.read_int(localPlayer + m_iCrosshairId)
				entity_team = py.read_int(entity+0xF4)
				player_team = py.read_int(localPlayer+0xF4)
				if entity_id > 0 and entity <= 64 and player_team != entity_team:
					mouse.press(Button.left)
					mouse.release(Button.left)
			if menu.baimbot == True: #aimbot button
				playerX = py.read_float(localPlayer + 0x138)
				playerY = py.read_float(localPlayer + 0x13C)
				playerZ = py.read_float(py.read_int(localPlayer + 0x26A8) + 0x1AC)
				entX = py.read_float(py.read_int(entity + 0x26A8) + 0x18C)
				entY = py.read_float(py.read_int(entity + 0x26A8) + 0x19C)
				entZ = py.read_float(py.read_int(entity + 0x26A8) + 0x1AC)
				magnitude = math.sqrt(math.pow(entX-playerX,2) + math.pow(entY-playerY,2)+ math.pow(entZ-playerZ,2))
				desangleX = math.degrees(-math.asin((entZ-playerZ)/magnitude))
				desangleY = math.degrees(math.atan2(entY-playerY, entX-playerX))
				angleDistX = abs(desangleX - py.read_float(s.viewAngles) - (2*py.read_float(localPlayer+0x302C)))
				angleDistY = abs(desangleY - py.read_float(s.viewAngles+0x4) - (2*py.read_float(localPlayer+0x3030)))
				hypotenuseDist = math.sqrt(math.pow(angleDistX, 2) + math.pow(angleDistY, 2))
				if angleDistY > menu.aimScale.get() / 2:
				   continue
				if angleDistX > menu.aimScale.get():
				   continue
				if (hypotenuseDist > closestAngle):
				  continue
				if (hypotenuseDist <= closestAngle):
				   closestAngle = hypotenuseDist
				if baimt == True:
					py.write_float(s.viewAngles, (desangleX-(2*py.read_float(localPlayer+0x302C))))
					py.write_float(s.viewAngles+0x04, (desangleY-(py.read_float(localPlayer+0x3030)*2)))
					mouse.click(Button,left, 1)
		closestAngle+=1
main()