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
    return success


def load():

    success: bool = True
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


            topLeftViewport = SDL_Rect()
            topLeftViewport.x = 0
            topLeftViewport.y = 0
            topLeftViewport.w = SCREEN_WIDTH // 2
            topLeftViewport.h = SCREEN_HEIGHT // 2
            SDL_RenderSetViewport(gRenderer, topLeftViewport)

            SDL_RenderCopy(gRenderer, gTexture, None, None)

            topRightViewport = SDL_Rect()
            topRightViewport.x = SCREEN_WIDTH // 2
            topRightViewport.y = 0
            topRightViewport.w = SCREEN_WIDTH // 2
            topRightViewport.h = SCREEN_HEIGHT // 2
            SDL_RenderSetViewport(gRenderer, topRightViewport)

            bottomViewport = SDL_Rect()
            bottomViewport.x = 0;
            bottomViewport.y = SCREEN_HEIGHT // 2
            bottomViewport.w = SCREEN_WIDTH
            bottomViewport.h = SCREEN_HEIGHT // 2
            SDL_RenderSetViewport(gRenderer, bottomViewport)

            event = SDL_Event()
            running = True
            while running:
                while SDL_PollEvent(ctypes.byref(event)) != 0:
                    if event.type == SDL_QUIT:
                        running = False
                        break
                SDL_SetRenderDrawColor(gRenderer, 0xFF, 0xFF, 0xFF, 0xFF)
                SDL_RenderClear(gRenderer)
                fillRect = SDL_Rect(SCREEN_WIDTH//4, SCREEN_HEIGHT//4, SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
                SDL_SetRenderDrawColor(gRenderer, 0xFF, 0x00, 0x00, 0xFF)
                SDL_RenderFillRect(gRenderer, fillRect)

                outlineRect = SDL_Rect(SCREEN_WIDTH//6, SCREEN_HEIGHT//6, SCREEN_WIDTH*2//3, SCREEN_HEIGHT*2//3)
                SDL_SetRenderDrawColor(gRenderer, 0x00, 0xFF, 0x00, 0xFF)
                SDL_RenderDrawRect(gRenderer, outlineRect)
                SDL_SetRenderDrawColor(gRenderer, 0xFF, 0xFF, 0x00, 0xFF)

                for i in range(0,SCREEN_HEIGHT-1,4):
                    SDL_RenderDrawPoint(gRenderer, SCREEN_WIDTH // 2, i)
                SDL_RenderPresent(gRenderer)
    close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
