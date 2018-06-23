import os
path = "C:/Users/q4to/PycharmProject/q4_c_sdl2/"
os.environ["PYSDL2_DLL_PATH"] = path + "resources/dlls/"
resources_images = path + "resources/images/"
import sys
import ctypes
from sdl2 import *
from enum import Enum
from pprint import pprint


gWindow: SDL_Window = None
gScreenSurface: SDL_Surface = None
gCurrentSurface: SDL_Surface = None
gHelloWorld: SDL_Surface = None
gKeyPressSurfaces = {}
fmt: SDL_PixelFormat = SDL_PixelFormat(format = 4)
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

def loadsurface(path):
    loadedsurface: SDL_Surface = SDL_LoadBMP(bytes(path, "utf-8"))
    if not loadedsurface:
        print("Unable to load image {}! SDL Error: {}\n".format(path, SDL_GetError()))
        return loadedsurface
    optimizedsurface = SDL_ConvertSurface(loadedsurface, gScreenSurface.contents.format.contents, 0)
    if not optimizedsurface:
        print("Unable to optimize image {}! SDL Error: {}\n".format(path, SDL_GetError()))
        return loadedsurface
    SDL_FreeSurface(loadedsurface)
    print("optimized surface loaded successfully!")
    return optimizedsurface


class KeyPressSurfaces(Enum):
    KEY_PRESS_SURFACE_DEFAULT = 1
    KEY_PRESS_SURFACE_UP = 2
    KEY_PRESS_SURFACE_DOWN = 3
    KEY_PRESS_SURFACE_LEFT = 4
    KEY_PRESS_SURFACE_RIGHT = 5


def init():
    global gWindow, gScreenSurface
    success = True

    if SDL_Init(SDL_INIT_VIDEO) < 0:
        print("SDL could not initialize! SDL_Error: %s\n" % SDL_GetError())
        success = False
    else:
        gWindow = SDL_CreateWindow(b"SDL Tutorial", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED,
                                   SCREEN_WIDTH, SCREEN_HEIGHT, SDL_WINDOW_SHOWN)
        if not gWindow:
            print("Window could not be created! SDL_Error: %s\n" % SDL_GetError())
            success = False

        else:
            gScreenSurface = SDL_GetWindowSurface(gWindow)
            pprint(gScreenSurface.contents.format.contents)
    return success


def load():
    global gScreenSurface, gHelloWorld, gKeyPressSurfaces
    success: bool = True
    gHelloWorld = loadsurface(resources_images + "q4.bmp")
    if not gHelloWorld:
        success = False

    return success


def close():
    global gWindow, gScreenSurface, gHelloWorld
    SDL_FreeSurface(gHelloWorld)
    gHelloWorld = None

    SDL_DestroyWindow(gWindow)
    gWindow = None
    SDL_Quit()


def main():
    global gWindow, gScreenSurface, gHelloWorld, gKeyPressSurfaces, gCurrentSurface
    if not init():
        print("Failed to initialize!\n")
    else:
        if not load():
            print("Failed to load!\n")
        else:
            SDL_BlitSurface(gHelloWorld, None, gScreenSurface, None)
            SDL_UpdateWindowSurface(gWindow)
            event = SDL_Event()

            stretchRect = SDL_Rect()
            stretchRect.x = 0
            stretchRect.y = 0
            stretchRect.w = SCREEN_WIDTH
            stretchRect.h = SCREEN_HEIGHT
            SDL_BlitScaled(gHelloWorld, None, gScreenSurface, stretchRect)

            running = True
            while running:
                while SDL_PollEvent(ctypes.byref(event)) != 0:
                    if event.type == SDL_QUIT:
                        running = False
                        break
    close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
