import pygame, logging, time
from utilities import *
import os, globals
from player import Player
pygame.init()

# Set up the display
screen = pygame.display.set_mode((0 , 0))
globals.screen_width = screen.get_width()
globals.screen_height = screen.get_height()
pygame.display.set_caption("Hot wheels")

logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler('log.txt'),
                        logging.StreamHandler()
                    ])

logging.info('Starting game...')

globals.cars = {}
car_images_path = 'assets/cars'

for car_image in os.listdir(car_images_path):
    if car_image.endswith('.png'):
        car_name = os.path.splitext(car_image)[0]
        globals.carTextures[car_name] = pygame.image.load(os.path.join(car_images_path, car_image))

logging.info(f'Loaded {len(globals.carTextures)} car images.')


player = Player()

# Main game loop
running = True
clock = pygame.time.Clock()
while running:
    dt = clock.tick() # ms
    player.update(dt)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            pass

    screen.fill((0, 0, 0))

    player.draw(screen, (0,0))

    pygame.display.update()

pygame.quit()