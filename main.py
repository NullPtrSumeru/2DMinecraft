import pygame
import random

pygame.init()
screen = pygame.display.set_mode((400, 400))
current_color = (255, 0, 0)
done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            current_color = random.sample(range(0, 256), 3)
            screen.fill(current_color)
            
    #screen.blit(pygame_head, (0,0))
    pygame.display.flip()

pygame.quit()