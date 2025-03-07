import pygame, logging, time
from utilities import *

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((0, 0))
pygame.display.set_caption("Hot Wheels Game")

# Set up the clock for managing the frame rate
clock = pygame.time.Clock()

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw everything
    screen.fill((0, 0, 0))  # Fill the screen with black

    # Flip the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()