from random import *
from math import *
import pygame
import globals
import perlin_noise as perlin
pygame.init()

directional_vectors=[(0,1),(1,0),(0,-1),(-1,0)]
tile_size=1000
class Tile:
    def __init__(self):
        self.vertices=set()
    def draw(self,surface,x,y):
        pygame.draw.circle(surface, (255, 255, 255), (x + tile_size / 2, y + tile_size / 2), int(tile_size / 500 * 65), int(tile_size / 500 * 10))
        for i in self.vertices:
            if i == 0:  # Goes down
                pygame.draw.rect(surface, (255, 255, 255), (x + tile_size / 2 - tile_size / 500 * 65, y + tile_size / 2, tile_size / 500 * 65 * 2, tile_size / 2))
            elif i == 2:  # Goes up
                pygame.draw.rect(surface, (255, 255, 255), (x + tile_size / 2 - tile_size / 500 * 65, y, tile_size / 500 * 65 * 2, tile_size / 2))
            elif i == 1:  # Goes right
                pygame.draw.rect(surface, (255, 255, 255), (x + tile_size / 2, y + tile_size / 2 - tile_size / 500 * 65, tile_size / 2, tile_size / 500 * 65 * 2))
            elif i == 3:  # Goes left
                pygame.draw.rect(surface, (255, 255, 255), (x, y + tile_size / 2 - tile_size / 500 * 65, tile_size / 2, tile_size / 500 * 65 * 2))
        
        pygame.draw.circle(surface, (35, 35, 35), (x + tile_size / 2, y + tile_size / 2), int(tile_size / 500 * 55))
        for i in self.vertices:
            if i == 0:  # Goes down
                pygame.draw.rect(surface, (35, 35, 35), (x + tile_size / 2 - tile_size / 500 * 55, y + tile_size / 2, tile_size / 500 * 110, tile_size / 2))
            elif i == 2:  # Goes up
                pygame.draw.rect(surface, (35, 35, 35), (x + tile_size / 2 - tile_size / 500 * 55, y, tile_size / 500 * 110, tile_size / 2))
            elif i == 1:  # Goes right
                pygame.draw.rect(surface, (35, 35, 35), (x + tile_size / 2, y + tile_size / 2 - tile_size / 500 * 55, tile_size / 2, tile_size / 500 * 110))
            elif i == 3:  # Goes left
                pygame.draw.rect(surface, (35, 35, 35), (x, y + tile_size / 2 - tile_size / 500 * 55, tile_size / 2, tile_size / 500 * 110))
        
        for i in self.vertices:
            if i == 0:
                for ii in range(9):
                    line_y = tile_size / 40 + ii * tile_size / 20 + tile_size / 80
                    pygame.draw.rect(surface, (255, 255, 255), (x + tile_size / 2 - tile_size / 500 * 1, y + tile_size / 2 + line_y, tile_size / 500 * 2, tile_size / 40))
            elif i == 2:
                for ii in range(9):
                    line_y = tile_size / 40 + ii * tile_size / 20 + tile_size / 80
                    pygame.draw.rect(surface, (255, 255, 255), (x + tile_size / 2 - tile_size / 500 * 1, y + line_y, tile_size / 500 * 2, tile_size / 40))
            elif i == 1:
                for ii in range(9):
                    line_x = tile_size / 40 + ii * tile_size / 20 + tile_size / 80
                    pygame.draw.rect(surface, (255, 255, 255), (x + tile_size / 2 + line_x, y + tile_size / 2 - tile_size / 500 * 1, tile_size / 40, tile_size / 500 * 2))
            elif i == 3:
                for ii in range(9):
                    line_x = tile_size / 40 + ii * tile_size / 20 + tile_size / 80
                    pygame.draw.rect(surface, (255, 255, 255), (x + line_x, y + tile_size / 2 - tile_size / 500 * 1, tile_size / 40, tile_size / 500 * 2))
            
class Map:
    def __init__(self):
        self.biome_noise=perlin.PerlinNoise(octaves=100)
        self.graph_noise=perlin.PerlinNoise(octaves=100)
        self.loaded_tiles={} #Shouldn't be too filled, as we think of doing this with WFC if possible
        #otherwise, we can just load the game in chunks, and deload them once the player gets too far
        #I think that for the short term of the game jam, this is optimal
        #Or, even better. We could generate this using a noise generator. 
        #And we generate 1 or 2 random intersections for each tile, and we make this a graph
        #We make the tile size be 2000x2000 pixels
        self.previous_active_x=-100
        self.previous_active_y=-100  #If either of these change, we know that the map needs to be updated
        self.missing_vertices={}
    def update(self,car):
        self.active_x=car.x//tile_size
        self.active_y=car.y//tile_size
        if self.previous_active_x!=self.active_x or self.previous_active_y!=self.active_x:
            new_loaded=[]
            for i in range(7): #first, it should load all the new tiles. 
                i-=3
                for ii in range(7):
                    ii-=3
                    new_pos=(self.active_x+i,self.active_y+ii)
                    if not new_pos in self.loaded_tiles: 
                        self.loaded_tiles[new_pos]=Tile()
                        new_loaded.append(new_pos)
            for new_pos in new_loaded:
                for I,iii in enumerate(directional_vectors): #This may seem too heavy, but it is at worst 28 times, and at best 196 times
                    seed(round(self.graph_noise([new_pos[iv]+iii[iv]/1000 for iv in range(2)])*1000000)) #Takes the seed at the current position
                    for iv in choices([i for i in range(4)],k=randint(1,2)): #adds 1 or two random lines to move out of from the current tile
                        if iv==I: #checks if the inverse vector of the current directional vector is randomly selected
                            self.loaded_tiles[new_pos].vertices.add(iv) #assuming we make it this way. there is practically no need for any WFC
                            other_pos=tuple([new_pos[iv]+iii[iv] for iv in range(2)])
                            if other_pos in self.loaded_tiles:
                                self.loaded_tiles[other_pos].vertices.add((I+2)%4) #Adds the inverse vector to the other tile if it's loaded. 
                            else:
                                if not other_pos in self.missing_vertices:
                                    self.missing_vertices[other_pos]=set() #for optimisation :)
                                self.missing_vertices[other_pos].add((I+2)%4)
                if new_pos in self.missing_vertices:
                    self.loaded_tiles[new_pos].vertices.update(self.missing_vertices[new_pos])
        self.previous_active_x=self.active_x
        self.previous_active_y=self.active_y
    def draw(self,surface,car):
        x_offset=car.x%tile_size
        y_offset=car.y%tile_size
        camera_x_offset=surface.get_width()/2
        camera_y_offset=surface.get_height()/2
        for i in self.loaded_tiles:
            if abs(self.active_x-i[0])<3 and abs(self.active_y-i[1])<3: #draws the nearest 25 tiles
                tile_x=i[0]*tile_size-car.x+camera_x_offset
                tile_y=i[1]*tile_size-car.y+camera_y_offset
                self.loaded_tiles[i].draw(surface,tile_x,tile_y)
                #pygame.draw.circle(surface,(255,255,255),(center_x,center_y),50,10)