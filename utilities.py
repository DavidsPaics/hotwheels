import pygame, time, logging

fonts={}
texts={}
def drawFPSCounter(screen,clock,font="arial",size=20,color=(255,255,255),bold=False,italic=False): #Draws the fps counter
    fps=round(clock.get_fps())
    screen.blit(renderText("FPS: "+str(fps),size=size,color=color,font=font,bold=bold,italic=italic),(0,0))
def center(sprite,surface,x,y): #Centers a sprite on specific coordinates
   # print(sprite.get_width(),x)
    surface.blit(sprite,(x-sprite.get_width()/2,y-sprite.get_height()/2))
def renderText(text,size=20,color=(255,255,255),font="arial",bold=False,italic=False): #allows you to render text fast
    font_key=str(font)+str(size)
    text_key=str(font_key)+str(text)+str(color)
    if not font_key in fonts:
        try:
            fonts[font_key]=pygame.font.SysFont(font,int(size), bold=bold, italic=italic) #Tries to load the file from the system
        except: #If that doesn't work
            try:
                fonts[font_key]=pygame.font.Font(font,int(size)) #bold/itallic not supported
            except:
                fonts[font_key]=pygame.font.SysFont("comicsansms", int(size), bold=bold, italic=italic)

    if not text_key in texts:
        texts[text_key]=fonts[font_key].render(str(text),1,color)
    return texts[text_key]
