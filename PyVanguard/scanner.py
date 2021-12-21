import pymem
import re


def pogout(modname, pattern, extra = 0, offset = 0, relative = True):
    pog = pymem.Pymem("csgo.exe")
    out = pymem.process.module_from_name(pog.process_handle, modname)
    bytes = pog.read_bytes(out.lpBaseOfDll, out.SizeOfImage)
    match = re.search(pattern, bytes).start()
    yes_relative = pog.read_int(out.lpBaseOfDll + match + offset) + extra - out.lpBaseOfDll
    non_relative = pog.read_int(out.lpBaseOfDll + match + offset) + extra
    return [yes_relative, out.lpBaseOfDll] if relative else non_relative


POGdwForceJump = pogout("client.dll", rb"\x8B\x0D....\x8B\xD6\x8B\xC1\x83\xCA\x02", 0, 2)
global dwForceJump
dwForceJump = POGdwForceJump[1] + POGdwForceJump[0]
POGlocalPlayer = pogout("client.dll", rb"\x8D\x34\x85....\x89\x15....\x8B\x41\x08\x8B\x48\x04\x83\xF9\xFF", 4, 3)
global localPlayer
localPlayer = POGlocalPlayer[0] + POGlocalPlayer[1]
POGentityList = pogout("client.dll", rb"\xBB....\x83\xFF\x01\x0F\x8C....\x3B\xF8", 0, 1)
entityList = POGentityList[0] + POGlocalPlayer[1]
POGclientstate = pogout("engine.dll", rb"\xA1....\x33\xD2\x6A\x00\x6A\x00\x33\xC9\x89\xB0", 0, 1)
dwclientState = POGclientstate[0] + POGclientstate[1]
POGviewangles = pogout("engine.dll", rb"\xF3\x0F\x11\x80....\xD9\x46\x04\xD9\x05", 0, 4, False) ## returns offset from dwclientstate
viewAngles = POGviewangles