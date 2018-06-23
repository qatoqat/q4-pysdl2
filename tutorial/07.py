import os
path = "C:\\Users\\q4to\\PycharmProject\\q4_c_sdl2\\"
os.environ["PYSDL2_DLL_PATH"] = path + "resources\\dlls\\"
resources_images = path + "resources\\images\\"
import sys
import ctypes
from sdl2 import *
from sdl2.sdlimage import*

gWindow: SDL_Window = None
gRenderer: SDL_Renderer = None
gTexture: SDL_Texture = None
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

def loadsurface(path):
    loadedsurface: SDL_Surface = IMG_Load(bytes(path, "utf-8"))
    if not loadedsurface:
        print("Unable to load image {}! SDL Error: {}\n".format(path, SDL_GetError()))
        return loadedsurface
    optimizedsurface = SDL_ConvertSurface(loadedsurface, gScreenSurface.contents.format.contents, 0)
    if not optimizedsurface:
        print("Unable to optimize image {}! SDL Error: {}\n".format(path, SDL_GetError()))
        return optimizedsurface
    SDL_FreeSurface(loadedsurface)
    print("optimized surface loaded successfully!")
    return optimizedsurface

def loadtexture(path):
    loadedsurface: SDL_Surface = IMG_Load(bytes(path, "utf-8"))
    if not loadedsurface:
        print("Unable to load image {}! SDL Error: {}\n".format(path, SDL_GetError()))
        return loadedsurface
    else:
        newtexture = SDL_CreateTextureFromSurface(gRenderer, loadedsurface)
        if not newtexture:
            print("Unable to create texture from {}! SDL Error: {}\n".format(path, SDL_GetError()))
            return newtexture
        SDL_FreeSurface(loadedsurface)
        return newtexture

def init():
    global gWindow, gTexture, gRenderer
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
            gRenderer = SDL_CreateRenderer(gWindow, -1, SDL_RENDERER_ACCELERATED)
            if not gRenderer:
                print("Renderer could not be created! SDL Error: {}\n".format(SDL_GetError()))
                success = False
            else:
                SDL_SetRenderDrawColor(gRenderer, 0xFF, 0xFF, 0xFF, 0xFF)
                imgflags = IMG_INIT_PNG
                if not IMG_Init(imgflags) & imgflags:
                    print("SDL_image could not initialize! SDL_image Error: {}\n".format(IMG_GetError()))
                    success = False
                else:
                    gScreenSurface = SDL_GetWindowSurface(gWindow)
    return success


def load():
    global gScreenSurface, gTexture
    success: bool = True
    gTexture = loadtexture(resources_images + "q4.png")
    if not gTexture:
        success = False

    return success


def close():
    global gWindow, gRenderer, gTexture
    SDL_DestroyTexture(gTexture)
    gTexture = None

    SDL_DestroyRenderer(gRenderer)
    gRenderer = None

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
            event = SDL_Event()
            running = True
            while running:
                while SDL_PollEvent(ctypes.byref(event)) != 0:
                    if event.type == SDL_QUIT:
                        running = False
                        break
                SDL_RenderClear(gRenderer)

                SDL_RenderCopy(gRenderer, gTexture, None, None)

                SDL_RenderPresent(gRenderer)

    close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
