import pygame, logging, time, globals

class Player:
    def __init__(self):
        self.pos = [0,0]
        self.vel = [0,0]
        self.surface = globals.carTextures["compact_red"]
    
    def update(self, dt):
        pass

    def draw(self, screen, camerapos):
        screen.blit(self.surface, (self.pos[0]-camerapos[0], self.pos[1]-camerapos[1]))