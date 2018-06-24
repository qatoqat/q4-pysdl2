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
gSpriteClips = []
gSpriteSheetTexture = None


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

    def render(self, x, y, clip: SDL_Rect):
        renderQuad = SDL_Rect(x, y, self.mWidth, self.mHeight)
        if clip:
            renderQuad.w = clip.w
            renderQuad.h = clip.h
        SDL_RenderCopy(gRenderer, self.mTexture, clip, renderQuad)
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
    global gSpriteSheetTexture, gBackgroundTexture, gSpriteClips
    gSpriteSheetTexture = LTexture()
    gFooTexture = LTexture()
    gBackgroundTexture = LTexture()
    if not gSpriteSheetTexture.loadfromfile(resources_images + "sprites.png"):
        print("Failed to load Foo' texture image!\n")
        return False
    gSpriteClips.append(SDL_Rect())
    gSpriteClips[0].x = 0
    gSpriteClips[0].y = 0
    gSpriteClips[0].w = 100
    gSpriteClips[0].h = 100
    gSpriteClips.append(SDL_Rect())
    gSpriteClips[1].x = 100
    gSpriteClips[1].y = 0
    gSpriteClips[1].w = 100
    gSpriteClips[1].h = 100
    gSpriteClips.append(SDL_Rect())
    gSpriteClips[2].x = 0
    gSpriteClips[2].y = 100
    gSpriteClips[2].w = 100
    gSpriteClips[2].h = 100
    gSpriteClips.append(SDL_Rect())
    gSpriteClips[3].x = 100
    gSpriteClips[3].y = 100
    gSpriteClips[3].w = 100
    gSpriteClips[3].h = 100

    return True

def close():
    global gWindow, gRenderer, gSpriteClips
    gSpriteSheetTexture.free()
    gBackgroundTexture.free()
    SDL_DestroyRenderer(gRenderer)
    gRenderer = None

    SDL_DestroyWindow(gWindow)
    gWindow = None
    IMG_Quit()
    SDL_Quit()


def main():
    global gWindow, gScreenSurface, gCurrentSurface, gRenderer, gSpriteClips
    if not init():
        print("Failed to initialize!\n")
    else:
        if not load():
            print("Failed to load!\n")
        else:


            event = SDL_Event()
            running = True
            print(gSpriteClips)
            SDL_SetRenderDrawColor(gRenderer, 0xFF, 0xFF, 0xFF, 0xFF)
            SDL_RenderClear(gRenderer)
            gSpriteSheetTexture.render(0, 0, gSpriteClips[0])
            gSpriteSheetTexture.render(SCREEN_WIDTH - gSpriteClips[1].w, 0, gSpriteClips[1])
            gSpriteSheetTexture.render(0, SCREEN_HEIGHT - gSpriteClips[2].h, gSpriteClips[2])
            gSpriteSheetTexture.render(SCREEN_WIDTH - gSpriteClips[3].w, SCREEN_HEIGHT - gSpriteClips[3].h,
                                       gSpriteClips[3])
            SDL_RenderPresent(gRenderer)
            while running:
                while SDL_PollEvent(ctypes.byref(event)) != 0:
                    if event.type == SDL_QUIT:
                        running = False
                        break

    close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
