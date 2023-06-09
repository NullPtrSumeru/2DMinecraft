import pygame
import requests
import threading
import random
import sys
from pygame.locals import *
from io import BytesIO 
from threading import Timer
from mcpi.minecraft import *
from mcpi.event import ChatEvent
import time 
from pygame.rect import Rect

class TextObject:
    def __init__(self, x, y, text_func, color, font_name, font_size):
        self.pos = (x, y)
        self.text_func = text_func
        self.color = color
        self.font = pygame.font.SysFont(font_name, font_size)
        self.bounds = self.get_surface(text_func())

    def draw(self, surface, centralized=False):
        text_surface, self.bounds = self.get_surface(self.text_func())
        if centralized:
            pos = (self.pos[0] - self.bounds.width // 2, self.pos[1])
        else:
            pos = self.pos
        surface.blit(text_surface, pos)

    def get_surface(self, text):
        text_surface = self.font.render(text, False, self.color)
        return text_surface, text_surface.get_rect()

    def update(self):
        pass

class GameObject:
    def __init__(self, x, y, w, h, speed=(0,0)):
        self.bounds = Rect(x, y, w, h)
        self.speed = speed

    @property
    def left(self):
        return self.bounds.left

    @property
    def right(self):
        return self.bounds.right

    @property
    def top(self):
        return self.bounds.top

    @property
    def bottom(self):
        return self.bounds.bottom

    @property
    def width(self):
        return self.bounds.width

    @property
    def height(self):
        return self.bounds.height

    @property
    def center(self):
        return self.bounds.center

    @property
    def centerx(self):
        return self.bounds.centerx

    @property
    def centery(self):
        return self.bounds.centery

    def draw(self, surface):
        pass

    def move(self, dx, dy):
        self.bounds = self.bounds.move(dx, dy)

    def update(self):
        """"""
        if self.speed == [0, 0]:
            return

        self.move(*self.speed)

Loading = True
gameRunning = False
musicButtons = True
musicPlays = False
running = True
mcpiInit = False

menu_offset_x = 20 
menu_offset_y = 300 
menu_button_w = 240 
menu_button_h = 150 
button_normal_back_color = (255, 106, 106) 
button_hover_back_color = (238, 106, 167) 
button_pressed_back_color = (205, 85, 85)
button_text_color = (255, 255, 255)
font_name = 'Arial' 
font_size = 60 
objects = []
block_img = 0
width = 0
height = 0

def endLoading():
	   global Loading
	   Loading = False

def on_play():
	   print("Play")
	   global gameRunning
	   gameRunning = True

def on_quit():
	   print("Quit")
	   pygame.quit()
	   global running
	   running = False
	   sys.exit()

class CreateButton(GameObject): 
          def __init__(self, x, y, w, h, text, on_click=lambda x: None, padding=0): 
                 super().__init__(x, y, w, h) 
                 self.state = 'normal'
                 self.on_click = on_click 
                 self.text = TextObject(x + padding, y + padding, lambda: text, button_text_color, font_name, font_size)
          @property 
          def back_color(self): 
                 return dict(normal=button_normal_back_color, hover=button_hover_back_color, pressed=button_pressed_back_color)[self.state] 
          def draw(self, surface): 
                  pygame.draw.rect(surface, self.back_color, self.bounds) 
                  self.text.draw(surface)
          def create_menu(self):
	             for i, (text, handler) in enumerate((('ИГРАТЬ', on_play), ('ВЫЙТИ', on_quit))):
	                   b = CreateButton(menu_offset_x, 
	        	              menu_offset_y + (menu_button_h + 5) * i, 
	         	             menu_button_w, 
	         	             menu_button_h, 
	         	             text,
	                    	  handler, 
	         	             padding=5);
	                   objects.append(b) 
	                   #self.menu_buttons.append(b) 
	                  # self.mouse_handlers.append(b.handle_mouse_event)

class Block(pygame.sprite.Sprite):#Класс Спрайта
 def __init__(self): 
       pygame.sprite.Sprite.__init__(self)#Инициализация Sprite
       self.image = pygame.Surface((50, 50))#Создаем спрайт 50 на 50
       self.image = block_img#Устанавливаем изображение
       self.rect = self.image.get_rect()#Получаем поверхность спрайта
       self.rect.center = (width / 2, height / 2)#Определяем центр спрайта
 def update(self): 
        self.rect.x += 5 #Перемещаем спрайт вправо
        if self.rect.left > width: #Если достигается граница
            self.rect.right = 0#Возвращаем к началу
def MinecraftInit():
    try:
        mc = Minecraft.create(address="de2.netly.gg", port=26704) 
        mc.postToChat("/say test")
        
    except ConnectionRefusedError: 
        print("Не удалось подключиться к серверу Minecraft.") 
    except Exception as e: 
        print("Произошла ошибка при подключении к серверу Minecraft:", str(e))
import pygame

def song(value):
    global musicPlays
    if value == 1 and musicPlays == True:
        pygame.mixer.music.stop()
    if value == 0 and musicPlays == False:
        pygame.mixer.init()  # Инициализация звукового модуля Pygame
        response = requests.get("https://srv5.onlymp3.to/download?file=39fc39122685e647be90cc126ed7cdf1251003003")
        pygame.mixer.music.load(BytesIO(response.content))  # Загрузка музыкального файла
        pygame.mixer.music.play()  # Воспроизведение музыки


def Game():
  pygame.init()#Инициализируем pygame
  #Устанавливаем размеры окна
  pygame.mixer.init()#Для звука
  surface = pygame.display.set_mode((640, 480))
  response = requests.get('https://static-00.iconduck.com/assets.00/minecraft-icon-512x512-8mie91i2.png') 
  ball = pygame.image.load(BytesIO(response.content)) 
  global block_img
  block_img = pygame.image.load(BytesIO(requests.get('https://i.ibb.co/k1wcnxH/head.png').content)).convert()
  background = pygame.image.load(BytesIO(requests.get('https://i.ibb.co/KFwYCYd/background.png').content)).convert()
  ballrect = ball.get_rect()#Получаем повеохность изображения
  clock = pygame.time.Clock()

  GREEN = (0, 255, 0)
  global width, height
  width = surface.get_width()#Подучаем ширинц экрана
  height = surface.get_height()#Получаем высоту экрана
  font = pygame.font.SysFont("Arial", 64)
  toast_font = pygame.font.SysFont("Arial", 32)
  TEXT_COLOR = (0, 0, 0) 
  TOAST_COLOR = (255, 215, 0) 
  TOAST_PADDING = 10
  TOAST_DURATION = 3
  toast_text = "Загружаем... Пожалуйста, подождите.." 
  toast_surface = toast_font.render(toast_text, True, TEXT_COLOR) 
  toast_rect = Rect(TOAST_PADDING, height - (toast_surface.get_height() + TOAST_PADDING), toast_surface.get_width() + 2 * TOAST_PADDING, toast_surface.get_height() + 2 * TOAST_PADDING, ) 
  toast_start_time = None

  label = font.render("Загрузка..", 1, (0, 127, 255))

  speed = [8, 8]#Скорость анимации загрузки
  t = Timer(5, endLoading)#Через 10 секунд выполнится функция
  t.start()#Запускаем тимер

  Blocks = pygame.sprite.Group() 
  block = Block()
  Blocks.add(block)
  
  square = pygame.Surface((40, 300))
  square.fill('gold')
  text_surface = font.render("Minecraft 0.1", False, ('skyblue'))
  grass = pygame.image.load(BytesIO(requests.get('https://opengameart.org/sites/default/files/grass_47.png').content)).convert()
  ghost = pygame.image.load(BytesIO(requests.get('https://i.ibb.co/qsvY22x/imgonline-com-ua-Resize-f-Il-YYp-ACbf.png').content)).convert()
  ghost.set_colorkey('black')
  walk_right = [
                        pygame.image.load(BytesIO(requests.get('https://i.ibb.co/FKDQQYf/1670754087.png').content)).convert(),
                        pygame.image.load(BytesIO(requests.get("https://i.ibb.co/PCgTVGL/1670754094.png").content)).convert(),
                        pygame.image.load(BytesIO(requests.get("https://i.ibb.co/FKDQQYf/1670754087.png").content)).convert(),
                        pygame.image.load(BytesIO(requests.get('https://i.ibb.co/YRMq20J/1670754090.png').content)).convert()
]
  walk_right[0].set_colorkey('white')
  walk_right[1].set_colorkey('white')
  walk_right[2].set_colorkey('white')
  walk_right[3].set_colorkey('white')
  
  bg_x = 0
  
  player_speed = 10
  player_x = 150
  player_y = 250
  is_jump = False
  jump_count = 9
 # ghost_x = 620
  grass_x=35
  grass_blocks=[]
  blocks_cnt = 60
 
  ghost_timer = pygame.USEREVENT + 1
  pygame.time.set_timer(ghost_timer, 3000)
  ghost_list_in_game = []
  
  player_anim_count = 0
  surface_color = (255, 255, 255)
  
  button_font = pygame.font.SysFont("Arial", 24)
  layout = pygame.sprite.Group()

  yes_button = pygame.sprite.Sprite()
  yes_button.image = pygame.Surface((150, 75))
  yes_button.image.fill((255, 0, 0))  # Красный цвет для кнопки "Да"
  yes_button.rect = yes_button.image.get_rect()
  yes_button.rect.center = (200, 300)
  button_text_yes = button_font.render("Да", True, (0, 0, 0))
  text_rect_yes = button_text_yes.get_rect(center=yes_button.rect.center)
  layout.add(yes_button)

  no_button = pygame.sprite.Sprite()
  no_button.image = pygame.Surface((150, 75))
  no_button.image.fill((0, 0, 255))  # Синий цвет для кнопки "Нет"
  no_button.rect = no_button.image.get_rect()
  no_button.rect.center = (600, 300)
  button_text_no = button_font.render("Нет", True, (0, 0, 0))
  text_rect_no = button_text_no.get_rect(center=no_button.rect.center)
  layout.add(no_button)
  
  layout2 = pygame.sprite.Group()

  left_button = pygame.sprite.Sprite()
  left_button.image = pygame.Surface((150, 75))
  left_button.image.fill("green")  # Красный цвет для кнопки "Да"
  left_button.rect = left_button.image.get_rect()
  left_button.rect.center = (400, 600)
  button_text_left = button_font.render("Влево", True, (0, 0, 0))
  text_rect_left = button_text_left.get_rect(center=left_button.rect.center)
  layout2.add(left_button)

  right_button = pygame.sprite.Sprite()
  right_button.image = pygame.Surface((150, 75))
  right_button.image.fill((0, 0, 255))  # Синий цвет для кнопки "Нет"
  right_button.rect = right_button.image.get_rect()
  right_button.rect.center = (600, 600)
  button_text_right = button_font.render("Вправо", True, (0, 0, 0))
  text_rect_right = button_text_right.get_rect(center=right_button.rect.center)
  layout2.add(right_button)
  
  jump_button = pygame.sprite.Sprite()
  jump_button.image = pygame.Surface((150, 75))
  jump_button.image.fill('yellow') 
  jump_button.rect = jump_button.image.get_rect()
  jump_button.rect.center = (500, 700)
  button_text_jump = button_font.render("Прыжок", True, (0, 0, 0))
  text_rect_jump = button_text_jump.get_rect(center=jump_button.rect.center)
  layout2.add(jump_button)
  
  # Создаем поверхность для отрисовки текста
  music_surface = toast_font.render("Хотели бы ли вы музыки?", True, (0, 0, 0))
  music_rect = music_surface.get_rect(center=(width // 2, 200))
  
  btn = CreateButton(400, 400, 200, 200, "play")
  btn.create_menu()
  global mcpiInit
  global musicButtons
  global musicPlays
  global Loading
  global gameRunning
  while running:  # Главный цикл игры
    for event in pygame.event.get():  # Событие
        if event.type == ghost_timer:
                ghost_list_in_game.append(ghost.get_rect(topleft=(620, 250)))
        elif event.type == QUIT:  # Выход
            pygame.quit()  # Закрываем программу
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if Loading == True:
                   surface_color = random.sample(range(0, 256), 3)
            if event.button == 1:  # Левая кнопка мыши
                    if yes_button.rect.collidepoint(event.pos) and gameRunning == True and musicButtons == True:
                        song(0)  # Воспроизведение музыки при нажатии на кнопку "Да"
                        musicPlays = True
                    elif no_button.rect.collidepoint(event.pos) and gameRunning == True and musicButtons == True:
                        musicButtons = False
                        if musicPlays == True:
                            song(1)
                            musicPlays = False
                    if left_button.rect.collidepoint(event.pos) and gameRunning == True and player_x > 50:
                        player_x -= player_speed
                    elif right_button.rect.collidepoint(event.pos) and gameRunning == True and player_x < 600:
                        player_x += player_speed
                    elif jump_button.rect.collidepoint(event.pos) and gameRunning == True and not is_jump:
                        is_jump = True
                    if Loading == False:
                       for obj in objects:
                          if isinstance(obj, CreateButton) and obj.bounds.collidepoint(event.pos):
                             obj.on_click()
            else:
                if Loading == False:
                  for obj in objects:
                    if isinstance(obj, CreateButton) and obj.bounds.collidepoint(event.pos):
                        obj.on_quit()
    clock.tick(15)  # Ограничение в 60 фпс
    ballrect = ballrect.move(speed)  # Перемещаем изображение
    if Loading == True:
        surface.fill(surface_color)  # Заполняем экран белым цветом
        if ballrect.left < 0 or ballrect.right > width:  # Границы экрана вправо влево
            speed[0] = -speed[0]
        if ballrect.top < 0 or ballrect.bottom > height:  # Границы экрана вверх и вниз
            speed[1] = -speed[1]
        surface.blit(ball, ballrect)  # Отрисовываем изображение
        if toast_start_time is None:
            toast_start_time = time.time()
            current_time = time.time()
            if current_time - toast_start_time <= TOAST_DURATION:
                pygame.draw.rect(surface, TOAST_COLOR, toast_rect)
                surface.blit(toast_surface, (toast_rect.x + TOAST_PADDING, toast_rect.y + TOAST_PADDING))
        else:
            toast_start_time = None
        surface.blit(label, (0, 0))  # Рисуем текст
    elif gameRunning == False:
        surface.fill((0, 0, 0))  # Заполняем экран черным цветом
        Blocks.update()
        Blocks.draw(surface)
        for o in objects:
            o.draw(surface)
    elif gameRunning == True:
        surface.blit(background, (bg_x, 0))
        surface.blit(background, (bg_x + width, 0))
        if mcpiInit == False:
            MinecraftInit()
            mcpiInit = True
    elif gameRunning == False:
        surface.fill((0, 0, 0))  # Заполняем экран черным цветом
        Blocks.update()
        Blocks.draw(surface)
        for o in objects:
            o.draw(surface)
    elif gameRunning == True:
        surface.blit(background, (0, 0))
        if mcpiInit == False:
            MinecraftInit()
            mcpiInit = True
    if gameRunning == True and musicButtons == True:
         layout.draw(surface)
         surface.blit(button_text_yes, text_rect_yes.topleft)
         surface.blit(button_text_no, text_rect_no.topleft)
         # Отображаем текстовую поверхность на экране
         surface.blit(music_surface, music_rect.topleft)
    if gameRunning == True:
         surface.blit(square, (10, 0))
         surface.blit(text_surface, (300, 100))
         for i in range(blocks_cnt):
                grass_x+=10
                i+=1
                grass_blocks.append({'surface': grass, 'position': (grass_x, 300)})
         for j in range(blocks_cnt):
              surface.blit(grass_blocks[j-1]['surface'],grass_blocks[j-1]['position'])
              if j==blocks_cnt:
                  j = 0
         surface.blit(walk_right[player_anim_count], (player_x, player_y))
         layout2.draw(surface)
         surface.blit(button_text_left, text_rect_left.topleft)
         surface.blit(button_text_right, text_rect_right.topleft)
         surface.blit(button_text_jump, text_rect_jump.topleft)
         #surface.blit(ghost, (ghost_x, 250))
         player_rect = walk_right[0].get_rect(topleft=(player_x, player_y))
         #ghost_rect = ghost.get_rect(topleft=(ghost_x, 250))
         if ghost_list_in_game:
             for el in ghost_list_in_game:
                 surface.blit(ghost, el)
                 el.x -= 10
                 if player_rect.colliderect(el):
                     print("You lose!")
                     Loading = True
                     gameRunning = False
                     ballrect = ball.get_rect()
                     ghost_list_in_game = []
                     el.x = 0
                     t = Timer(5, endLoading)#Через 10 секунд выполнится функция
                     t.start()#Запускаем тимер

                     
         if is_jump == True:
             if jump_count >= -9:
                 if jump_count > 0:
                     player_y-=(jump_count ** 2) / 2
                 else:
                     player_y+=(jump_count ** 2) / 2
                 jump_count -= 1
             else:
                  is_jump = False
                  jump_count = 9
         if player_anim_count == 1:
             player_anim_count = 0
         else:
             player_anim_count+=1
         bg_x -= 2
         if bg_x == width:
             bg_x=0
        # ghost_x -= 10
    pygame.display.update()
    pygame.display.flip()  # Переворачиваем экран

Game()�еворачиваем экран

Game()