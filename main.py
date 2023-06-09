import pygame
import random
import requests
from io import BytesIO 

pygame.init()
screen = pygame.display.set_mode((400, 400))
current_color = (255, 0, 0)
done = False

pygame.mixer.init()  # Инициализация звукового модуля Pygame
response = requests.get("https://srv5.onlymp3.to/download?file=39fc39122685e647be90cc126ed7cdf1251003003")
pygame.mixer.music.load(BytesIO(response.content))  # Загрузка музыкального файла
pygame.mixer.music.play()  # Воспроизведение музыки

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