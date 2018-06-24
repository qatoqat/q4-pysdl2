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
gFooTexture = None
gBackgroundTexture = None


SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

class LTexture:
    def __init__(self):
        self.mTexture = None
        self.mWidth = 0
        self.mHeight = 0
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.free()
    def loadfromfile(self, path):
        self.free()
        loadedsurface = IMG_Load(bytes(path, "utf-8"))
        if not loadedsurface:
            print("Unable to load image {}! SDL Error: {}\n".format(path, SDL_GetError()))
            return False
        else:
            SDL_SetColorKey(loadedsurface, SDL_TRUE, SDL_MapRGB(loadedsurface.contents.format.contents, 0x00, 0x00, 0x00))
            newtexture = SDL_CreateTextureFromSurface(gRenderer, loadedsurface)
            if not newtexture:
                print("Unable to create texture from {}! SDL Error: {}\n".format(path, SDL_GetError()))
                return False
            self.mWidth = loadedsurface.contents.w
            self.mHeight = loadedsurface.contents.h
            SDL_FreeSurface(loadedsurface)
            self.mTexture = newtexture
            return True if self.mTexture != None else False

    def free(self):
        self.mTexture = None
        self.mWidth = 0
        self.mHeight = 0

    def render(self, x, y):
        renderQuad = SDL_Rect(x, y, self.mWidth, self.mHeight)
        SDL_RenderCopy(gRenderer, self.mTexture, None, renderQuad)
    def getwidth(self):
        return self.mWidth
    def getheight(self):
        return self.mHeight


def init():
    global gWindow, gRenderer
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
    global gFooTexture, gBackgroundTexture
    gFooTexture = LTexture()
    gBackgroundTexture = LTexture()
    if not gFooTexture.loadfromfile(resources_images + "q4.png"):
        print("Failed to load Foo' texture image!\n")
        return False
    if not gBackgroundTexture.loadfromfile(resources_images + "default.png"):
        print("Failed to load background texture image!\n")
        return False
    print(gFooTexture.mTexture, gBackgroundTexture.mTexture)
    return True


def close():
    global gWindow, gRenderer
    gFooTexture.free()
    gBackgroundTexture.free()
    SDL_DestroyRenderer(gRenderer)
    gRenderer = None

    SDL_DestroyWindow(gWindow)
    gWindow = None
    IMG_Quit()
    SDL_Quit()


def main():
    global gWindow, gScreenSurface, gCurrentSurface, gRenderer
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
                SDL_SetRenderDrawColor(gRenderer, 0xFF, 0xFF, 0xFF, 0xFF)
                SDL_RenderClear(gRenderer)
                gBackgroundTexture.render(0, 0)
                gFooTexture.render(0, 0)
                SDL_RenderPresent(gRenderer)
    close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
