import sys
import time
from time import sleep
import pygame
import random
from pygame.math import Vector2
from pygame.locals import *
import json
import re
import datetime as dt
import copy
pygame.mixer.pre_init(44100,-16,2,512)
current_date = dt.datetime.now().strftime("%H:%M, %A, %d %B %Y")


pygame.init()
counter = 0
cell_size = 40
cell_number_x = 20
cell_number_y = 20
cell_number = 20
screen = pygame.display.set_mode((cell_number_x * cell_size, cell_number_y * cell_size), RESIZABLE)
screen_width = screen.get_width( )
screen_hight = screen.get_height( )
game_active = True
go = True
grass_color = (110,170,50)
portal_color = (255,0,0)
snake_length = 4
snake_next_boost  = 12

class Fruit():
    def __init__(self):
        self.randomize()

    def draw_fruit(self):
        self.fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(apple,self.fruit_rect)
    def randomize(self):
        self.x = random.randint(0, (screen_width // 40) - 1)
        self.y = random.randint(0, (screen_hight // 40) -1)
        self.pos = Vector2(self.x, self.y)

class Snake():
    def __init__(self):
        self.body_copy = None
        self.body = [Vector2(7,8),Vector2(6,8),Vector2(5,8)]
        self.direction = Vector2(1,0)
        self.new_block = False

        self.head_up = pygame.image.load('head_up.png').convert_alpha( )
        self.head_down = pygame.image.load('head_down.png').convert_alpha( )
        self.head_right = pygame.image.load('head_right.png').convert_alpha( )
        self.head_left = pygame.image.load('head_left.png').convert_alpha( )

        self.tail_up = pygame.image.load('tail_up.png').convert_alpha( )
        self.tail_down = pygame.image.load('tail_down.png').convert_alpha( )
        self.tail_right = pygame.image.load('tail_right.png').convert_alpha( )
        self.tail_left = pygame.image.load('tail_left.png').convert_alpha( )

        self.body_vertical = pygame.image.load('body_vertical.png').convert_alpha( )
        self.body_horizontal = pygame.image.load('body_horizontal.png').convert_alpha( )

        self.body_tr = pygame.image.load('body_tr.png').convert_alpha( )
        self.body_tl = pygame.image.load('body_tl.png').convert_alpha( )
        self.body_br = pygame.image.load('body_br.png').convert_alpha( )
        self.body_bl = pygame.image.load('body_bl.png').convert_alpha( )
        self.crunch_sound = pygame.mixer.Sound("Sound_crunch.wav")


    def draw_snake(self):
        global snake_rect
        self.update_head()
        self.update_tail()

        for index,block in enumerate(self.body):
            self.snake_rect = pygame.Rect(int(block.x * cell_size), int(block.y * cell_size), cell_size, cell_size)

            if index == 0:
                screen.blit(self.head,self.snake_rect)
            elif index == len(self.body) -1:
                screen.blit(self.tail,self.snake_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical,self.snake_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal,self.snake_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                       screen.blit(self.body_tl,self.snake_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                       screen.blit(self.body_tr,self.snake_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                       screen.blit(self.body_bl,self.snake_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                       screen.blit(self.body_br,self.snake_rect)
    def draw_grass(self):
        for row in range(screen_width//20):
            if row % 2 == 0:
                for col in range(screen_hight//20):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * cell_size,row * cell_size,cell_size,cell_size)
                        pygame.draw.rect(screen,grass_color,grass_rect)
            else:
                for col in range(screen_hight//20):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)


    def update_head(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1,0): self.head = self.head_left
        elif head_relation == Vector2(-1,0): self.head = self.head_right
        elif head_relation == Vector2(0,1): self.head = self.head_up
        elif head_relation == Vector2(0,-1): self.head = self.head_down

    def update_tail(self):
        tail_relaition = self.body[-2] - self.body[-1]
        if tail_relaition == Vector2(1,0): self.tail = self.tail_left
        if tail_relaition == Vector2(-1,0): self.tail = self.tail_right
        if tail_relaition == Vector2(0,1): self.tail = self.tail_up
        if tail_relaition == Vector2(0,-1): self.tail = self.tail_down

    def move_snake(self):

        if self.new_block == True:
            self.body_copy = self.body[:]
            self.body_copy.insert(0,self.body_copy[0] + self.direction)
            self.body = self.body_copy[:]
            if grass_color != (0,0,0):
                self.new_block = False
            if grass_color == (0,0,0):
                self.body_copy = self.body[:]
                self.body_copy.insert(0, self.body_copy[0] + self.direction)
                self.body = self.body_copy[:]
                self.body_copy = self.body[:]
                self.body_copy.insert(0, self.body_copy[0] + self.direction)
                self.body = self.body_copy[:]
                self.body_copy = self.body[:]
                self.body_copy.insert(0, self.body_copy[0] + self.direction)
                self.body = self.body_copy[:]

                self.new_block = False
        else:
            self.body_copy = self.body[:-1]
            self.body_copy.insert(0,self.body_copy[0] + self.direction)
            self.body = self.body_copy[:]

    def add_block(self):
        self.new_block = True
    def play_crunch_sound(self):
        self.crunch_sound.play()

class Portal():

    def __init__(self):
        self.snake = Snake()
        self.width = cell_size
        self.hight = cell_size



    def draw(self):
        global portal_color
        self.portal_x = screen_width - self.width
        self.portal_y = (screen_hight - self.hight) - screen_hight // 2
        self.portal_rect = pygame.Rect(self.portal_x, self.portal_y, self.width, self.hight)
        self.portal_x = screen_width - self.width
        self.portal_y = (screen_hight - self.hight) - screen_hight // 2

        pygame.draw.rect(screen,portal_color,self.portal_rect)

class Main():
    def __init__(self):
        self.Counter = 0
        self.current_mode = []
        self.snake = Snake()
        self.fruit = Fruit()
        self.highscore = [0,0,0]
        self.current_highscore = [0]
        self.portal = Portal()

    def update(self):
        self.Colission_fruit()
        self.Colision_self()
        self.snake.move_snake()
        self.Hit_Wall()



    def draw_elements(self):
        self.snake.draw_snake( )
        self.fruit.draw_fruit( )
        if len(self.snake.body[0:]) >= snake_length:
            self.portal.draw( )



    def movement(self, event):
        global game_speed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and self.snake.direction != Vector2(0,1):
                self.snake.direction = Vector2(0,-1)
            if event.key == pygame.K_s and self.snake.direction != Vector2(0,-1):
                self.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_a and self.snake.direction != Vector2(1,0):
                self.snake.direction = Vector2(-1, 0)
            if event.key == pygame.K_d and self.snake.direction != Vector2(-1,0):
                self.snake.direction = Vector2(1, 0)

    def Quit(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    def Colission_fruit(self):
        global grass_color
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.Counter += 1
            if grass_color == (0,0,0):
                self.Counter += 3
            self.snake.play_crunch_sound()

        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()

    def Colision_self(self):
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()


    def Hit_Wall(self):
        if not 0 <= self.snake.body[0].x < screen_width / cell_size:

            self.game_over()
        if not 0 <= self.snake.body[0].y < screen_hight / cell_size:
            self.game_over()
    def game_over(self):
        global game_over,run
        game_over = True
        run = True
        self.new_counter = main_game.highscore.append(main_game.Counter)


    def counter(self):
        font = pygame.font.SysFont("Calibri",25,True,False)
        text = font.render("Counter: " + str(self.Counter),True,"White")
        score_x = int(cell_size * (screen_width // cell_size) - 70)
        score_y = int(cell_size * (screen_hight // cell_size) - 60)
        score_rect = text.get_rect(center=(score_x,score_y))
        apple_rect = apple.get_rect(midright=(score_rect.left,score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left,apple_rect.top,apple_rect.width + score_rect.width +12,apple_rect.height)

        pygame.draw.rect(screen, (176, 209, 61), bg_rect)
        screen.blit(text, score_rect)
        screen.blit(apple,apple_rect)
        pygame.draw.rect(screen, (0, 0, 0), bg_rect,2)
    def Highscore(self):
        global current_highscore, saved_highscores, casual_highscore
        for x in main_game.highscore[0:-2]:
            if main_game.highscore[-1] > x and main_game.highscore[-1] >= current_highscore["highscore"]:

                screen.fill((0,0,100))
                font_go = pygame.font.SysFont("Calibri", 80, True, False)
                You_reached = font_go.render("You reached: " + str(main_game.Counter), True, "White")
                screen.blit(You_reached, [screen_width // 2 - screen_width // 2.5, 100])
                new_highscore = main_game.highscore[-1]
                font_go = pygame.font.SysFont("Calibri", 100, True, False)
                settings_text = font_go.render("New Highscore:" + str(new_highscore), True, "Green")
                screen.blit(settings_text, [screen_width // 2 - screen_width // 2.5, 550])
                self.current_highscore.append(new_highscore)
                casual_highscore = self.current_highscore[-1]
                current_highscore = {"highscore": self.current_highscore[-1]}



                return current_highscore, saved_highscores



            else:
                screen.fill((0, 0, 100))
                font_go = pygame.font.SysFont("Calibri", 100, True, False)
                You_reached = font_go.render("You reached: " + str(main_game.Counter), True, "White")
                screen.blit(You_reached, [screen_width // 2 - screen_width // 2.5, 100])
                font_go = pygame.font.SysFont("Calibri", 100, True, False)
                settings_text = font_go.render(f'Highscore: {current_highscore["highscore"]}', True, "Red")

                screen.blit(settings_text, [screen_width // 2 - screen_width // 2.5, 550])
    def collision_portal(self):
        global R, G,B, grass_color, game_speed, portal_color, snake_length, snake_next_boost
        if len(self.snake.body[0:]) >= snake_length:
            if self.snake.snake_rect.colliderect(self.portal.portal_rect):

                print("lol")


                grass_color = (0,0,0)
                R = 255
                G = 0
                B = 0
                portal_color = "black"
                self.snake.body[0] = Vector2(7,8)
                self.snake.body[1] = Vector2(6,8)
                self.snake.body[2] = Vector2(5, 8)
                self.snake.direction = Vector2(1,0)
                return grass_color, R, G, B, game_speed
            if len(self.snake.body[0:]) >= snake_next_boost:
                grass_color = (110,170,50)
                snake_length += 4
                snake_next_boost += 10
                R = 0
                G = 90
                B = 10
                portal_color = "Red"
                return grass_color, R, G, B, game_speed





class Button:

    def __init__(self,text,width,height,pos, elevaition, Button):
        self.text_font = pygame.font.SysFont("Calibri", 20, True, False)
        self.user_input = "0"
        self.input_rect = pygame.Rect(60,300,180,30)
        self.text_is_shown = False
        self.button_down = [1]
        self.list = [0]
        self.click_counter = [1]
        self.game_speed = 100
        self.check_input_difference = ["h"]

        self.elevaition = elevaition
        self.dynamic_elevaition = elevaition
        self.original_y_pos = pos[1]

        gui_font = pygame.font.Font(None,30)
        self.pressed = False
        self.top_rect = pygame.Rect((pos),(width,height))
        self.top_color = "Blue"

        self.bottom_rect = pygame.Rect(pos,(width, elevaition))
        self.bottom_color = "Black"

        self.text_surf = gui_font.render(text,True,"White")
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)
    def Update_restart(self):
        self.draw()
        self.check_click_restart()
    def Update_settings(self):
        self.draw()
        self.check_click_settings()
    def check_click_settings(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = "Blue"
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elevaition = 0
                self.pressed = True
                self.settings()
                return
            else:
                if self.pressed == True:
                    self.dynamic_elevaition = self.elevaition
                    self.pressed = False
        else:
            self.dynamic_elevaition = self.elevaition
            self.top_color = "Blue"

    def settings(self):
        global settings
        settings = True

    def draw(self):
        self.top_rect.y = self.original_y_pos - self.dynamic_elevaition
        self.text_rect.center = self.top_rect.center

        pygame.draw.rect(screen,self.bottom_color,self.bottom_rect,border_radius = 12)
        pygame.draw.rect(screen,self.top_color,self.top_rect, border_radius = 12)
        screen.blit(self.text_surf,self.text_rect)

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elevaition
    def restart(self):
        global snake, game_over,main_game, grass_color, R, G, B, portal_color, snake_length, snake_next_boost

        game_over = False
        main_game.snake.body[0:] = [Vector2(7, 8), Vector2(6, 8), Vector2(5, 8)]
        snake.direction = Vector2(1,0)
        snake = main_game.snake
        grass_color = (110, 170, 50)
        main_game.Counter = 0
        R = 0
        G = 90
        B = 10
        portal_color = "Red"
        snake_length = 4
        snake_next_boost = 12


    def check_click_restart(self):
        global game_over, run
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = "Blue"
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elevaition = 0
                self.pressed = True
                self.restart()
                run = False
                return

            else:
                if self.pressed == True:
                    self.dynamic_elevaition = self.elevaition
                    self.pressed = False
                    #funktion
        else:
            self.dynamic_elevaition = self.elevaition
            self.top_color = "Blue"

    def difficulty(self):
        global difficult
        difficult = True
    def Update_difficulty(self):
        self.draw( )
        self.check_click_difficulty( )


    def check_click_difficulty(self):
        global game_speed, difficult
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = "Blue"
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elevaition = 0
                self.pressed = True
                self.difficulty( )
                return

            else:
                if self.pressed == True:
                    self.dynamic_elevaition = self.elevaition
                    self.pressed = False
                    if self.button_down[-1] == 2:
                        self.button_down.append(1)
                        difficult = False



                        self.list.append(self.user_input)
                        self.user_input = int(self.user_input)
                        if isinstance(self.user_input,str):
                            self.list = [0]
                            self.user_input = "0"
                        game_speed -= int(self.list[-1])
                        pygame.time.set_timer(SCRREEN_UPDATE,game_speed)
                        self.list = [0]
                        self.user_input = "0"

                        return game_speed


                    if self.button_down[-1] == 1:
                        self.button_down.append(2)
                        difficult = True
                        return

        else:
            self.dynamic_elevaition = self.elevaition
            self.top_color = "Blue"
    def Update_back_home(self):
        self.draw()
        self.check_click_back_home()
    def check_click_back_home(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = "Blue"
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elevaition = 0
                self.pressed = True
                self.back_home()
                return
            else:
                if self.pressed == True:
                    self.dynamic_elevaition = self.elevaition
                    self.pressed = False
        else:
            self.dynamic_elevaition = self.elevaition
            self.top_color = "Blue"

    def back_home(self):
        global settings, show_history
        settings = False
        show_history = False


    def volume(self):
        global volume_got_clicked
        volume_got_clicked = True

    def update_volume(self):
        self.draw()
        self.check_click_volume()
    def check_click_volume(self):
        global draw_volume, volume_got_clicked
        mouse_pos = pygame.mouse.get_pos()

        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = "Blue"
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elevaition = 0
                self.pressed = True
                self.volume()

                return
            else:
                if self.pressed == True:
                    self.dynamic_elevaition = self.elevaition
                    self.pressed = False
                    if self.click_counter[-1] == 2:
                        volume_got_clicked = False
                        self.click_counter.append(1)
                        return
                    if self.click_counter[-1] == 1:
                        self.click_counter.append(2)
                        return


        else:
            self.dynamic_elevaition = self.elevaition
            self.top_color = "Blue"

    def text_input(self):


        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.user_input = self.user_input[0:-1]

                else:
                    self.user_input += event.unicode

        pygame.draw.rect(screen,"Black", self.input_rect,4)
        font_text = self.text_font.render(str("Speed: " + self.user_input), True, "White")
        screen.blit(font_text, (self.input_rect.x + 10, self.input_rect.y + 10))

    def safe_highscore(self):
        global save_highscore
        save_highscore = True
    def update_save_highscore(self):
        self.draw()
        self.check_click_save_highscore()

    def check_click_save_highscore(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = "Blue"
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elevaition = 0
                self.pressed = True
                #self.safe_highscore()
                return
            else:
                if self.pressed == True:
                    self.dynamic_elevaition = self.elevaition
                    self.pressed = False
                    self.safe_highscore( )
        else:
            self.dynamic_elevaition = self.elevaition
            self.top_color = "Blue"
    def show_highscore_history(self):
        global show_history
        show_history = True
    def update_show_history(self):
        self.draw()
        self.check_click_history()

    def check_click_history(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = "Blue"
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elevaition = 0
                self.pressed = True
                self.show_highscore_history()
                return
            else:
                if self.pressed == True:
                    self.dynamic_elevaition = self.elevaition
                    self.pressed = False
        else:
            self.dynamic_elevaition = self.elevaition
            self.top_color = "Blue"








class Volume():
    def __init__(self):
        self.top_circle_rect = 20
        self.main_line_x = 70
        self.main_line_y = 450
        self.circle_y = self.main_line_y + 30

        self.line_bonded_y = self.main_line_y + 20
        self.circle_radius = 10
        self.circle_x = self.main_line_x
        self.line_bonded_x = self.main_line_x -10
        self.top_circle = pygame.Rect((self.circle_x, self.circle_y), (35, 35))
        self.current_volume = []
        self.top_triangle = pygame.Rect((self.line_bonded_x, self.line_bonded_y), (40 ,40))

    def draw(self):
            mouse_pos = pygame.mouse.get_pos()
            if self.top_circle.collidepoint(mouse_pos):
                if self.circle_radius <= 10:
                    self.circle_radius += 3
                    self.top_circle_rect += 3

                if pygame.mouse.get_pressed()[0]:
                    self.circle_x = pygame.mouse.get_pos( )[0]
                    self.line_bonded_x = pygame.mouse.get_pos( )[0]
                    if self.circle_x >= self.main_line_x + 150:
                        self.circle_x = self.main_line_x + 150
                        self.line_bonded_x = self.main_line_x + 150
                    elif self.circle_x <= self.main_line_x:
                        self.circle_x = self.main_line_x
                        self.line_bonded_x = self.main_line_x

            else:
                self.circle_radius = 10
                self.top_circle_rect = 20
            self.current_volume.append(self.circle_x - 70)

            pygame.mixer.music.set_volume(self.current_volume[-1] * 0.01)
            if len(self.current_volume) >= 3:
                del self.current_volume[0]


            self.top_circle = pygame.Rect((self.circle_x - 10 , self.circle_y - 10), (self.top_circle_rect, self.top_circle_rect))


            pygame.draw.rect(screen,(0,0,0),(self.main_line_x,self.main_line_y,150,15))
            pygame.draw.circle(screen, (130, 50, 0), (self.circle_x, self.circle_y), self.circle_radius)
            pygame.draw.polygon(screen, (0,0,0),((self.line_bonded_x - 30, self.line_bonded_y - 50), (self.line_bonded_x + 30, self.line_bonded_y - 50),(self.line_bonded_x, self.line_bonded_y -20)))
            percent = pygame.font.SysFont("Calibri", 10, True, False)
            percent_text = percent.render(f"{int(self.current_volume[-1] / 1.5)} %", True, "White")
            screen.blit(percent_text,(self.line_bonded_x - 8, self.line_bonded_y - 45))


FPS = pygame.time.Clock()
apple = pygame.image.load("apple.png").convert_alpha()

difficult = None
game_over = True
settings = False
volume_got_clicked = False
draw_volume = False
hit_portal = False
save_highscore = False

show_history = False




button1 = Button("Restart",screen_width // 3,40,(screen_width // 2 - screen_width // 6,250), 7,None)

button_show_history = Button("Show Highscore History",screen_width // 3,40,(screen_width // 2 - screen_width // 6,400), 7, None)
save_highscore_Button = Button("Save Highscore",screen_width // 3,40,(screen_width // 2 - screen_width // 6,325), 7,None)


button2 = Button("Settings",screen_width // 3,40,(screen_width // 2 - screen_width // 6,475), 7, None)

button_volume = Button("Volume",200,40,(50,375),7,None)
button_difficulty = Button("Difficulty LVL",200,40,(50,240), 7, None)
button_back_home = Button("Back to Menu",200,40,(50,600),7,None)



game_speed = 100
volume = Volume()
SCRREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCRREEN_UPDATE, game_speed)
main_game = Main()
snake = Snake()
pygame.mixer.music.load("tropicana-soundroll-main-version-1725-02-15.mp3")
pygame.mixer.music.play(-1,0.0)
portal = Portal()
R = 0
G = 90
B = 10
round = 0
last_element_of_the_history = 0
saved_highscores = {"highscore": 0}
current_highscore = {"highscore": 0}
Highscore_dictionary = current_highscore
highscore_history = saved_highscores

saved_times = []
saved_forenumber = []

try:
    with open("save_highscore.txt") as highscore_saved:
        Highscore_dictionary = json.load(highscore_saved)
        current_highscore = Highscore_dictionary


except:
    print("No file yet")

#try:
with open("highscore_history.txt") as Highscore_history_txt:
    highscore_history = json.load(Highscore_history_txt)
    saved_highscores = highscore_history
    forenumber = highscore_history
    for x in forenumber["fore_numbers"]:
        print(type(x))
        Vornummer = x






#except:
    #print("you suck")
values_list = []
def get_all_values(highscore_history):
    global values_list
    for key, value in highscore_history.items():
        if type(value) is dict:
            get_all_values(value)
        else:
            values_list.append(value)





while go:



    Highscore_dictionary = current_highscore





    events = pygame.event.get()
    for event in events:
        if event.type == VIDEORESIZE:
            screen_width = screen.get_width( )
            screen_hight = screen.get_height( )
    if not game_over:
        screen.fill((R,G,B))

        if round >= 1:
            main_game.collision_portal( )
            screen.fill((R, G, B))

        portal.draw( )
        snake.draw_grass()
        round +=1


        for event in events:
            main_game.Quit(event)

            if event.type == SCRREEN_UPDATE:
                 main_game.update()
            main_game.movement(event)
        main_game.counter()
        main_game.draw_elements( )
    if game_over and not settings:
        screen.fill((0, 0, 100))

        main_game.Highscore()
        button1.Update_restart()
        button2.Update_settings()
        button_show_history.update_show_history()
        save_highscore_Button.update_save_highscore( )

        for event in events:
          main_game.Quit(event)
        if save_highscore:
            with open("highscore_history.txt","r") as Highscore_history_txt:
                highscore_history = json.load(Highscore_history_txt)
                saved_highscores = highscore_history
            last_element_of_the_history = Vornummer


            last_element_of_the_history += 1
            with open("highscore_history.txt", "w") as Highscore_history_txt:
                highscore_history["fore_numbers"].append(last_element_of_the_history)
                highscore_history["fore_numbers"].pop(0)

                json.dump(highscore_history, Highscore_history_txt)

            with open("save_highscore.txt","w") as highscore_saved:
                json.dump(Highscore_dictionary, highscore_saved, indent =4)

            get_all_values(highscore_history["Highscores_history"])
            print(values_list)

            if values_list[-1] < Highscore_dictionary.get("highscore"):
                        print("gotit")
                        with open("highscore_history.txt", "w") as Highscore_history_txt:
                            highscore_history['Highscores_history'][f"{last_element_of_the_history}highscore"] = main_game.current_highscore[-1]
                            print(highscore_history)
                            json.dump(highscore_history, Highscore_history_txt, indent=4)
                            saved_times.append(current_date)
                        with open("highscore_history.txt", "w") as Highscore_history_txt:
                            highscore_history['Time_set'][f"{last_element_of_the_history}Score made in:"] = current_date
                            json.dump(highscore_history, Highscore_history_txt, indent=4)
                        saved_highscores = {f"{last_element_of_the_history} highscore": main_game.current_highscore[-1]}
                        save_highscore = False

            values_list = []

            save_highscore = False


        if show_history:
            screen.fill((0, 0, 100))
            y_coord = 120

            font_history = pygame.font.SysFont("Calibri", 75, True, False)
            time_text = font_history.render(f"You're Highscores: ", True, "White")

            screen.blit(time_text, [screen_width // 2 - screen_width // 2.3, 50])
            Forenumber = 0

            for k,f in highscore_history['Highscores_history'].items():


                    Forenumber += 1
                    y_coord += 40

                    try:

                        if highscore_history['Highscores_history'].get(f"{forenumber}highscore") - highscore_history['Highscores_history'].get(f"{forenumber - 1}highscore") >= 1:
                                highscore_history_replace = f"Highscore: {f}"
                                highscore_history_replaced1 = re.sub("[{}']", "",highscore_history_replace)
                                highscore_history_replaced2 = highscore_history_replaced1.replace("[","")
                                highscore_history_replaced3 = highscore_history_replaced2.replace("]","")
                                test = highscore_history_replaced3.replace(",", "")


                                button_back_home.Update_back_home( )
                                font_history = pygame.font.SysFont("Calibri", 20, True, False)
                                history_text = font_history.render(f"{test}", True, "White")

                                screen.blit(history_text, [screen_width // 2 - screen_width // 2.5, y_coord])

                        else:
                            y_coord -= 40
                    except:

                          highscore_history_replace = f"Highscore : {f}"
                          highscore_history_replaced1 = re.sub("[{}']", "",highscore_history_replace)
                          highscore_history_replaced2 = highscore_history_replaced1.replace("[","")
                          highscore_history_replaced3 = highscore_history_replaced2.replace("]","")
                          test = highscore_history_replaced3.replace(",", "")
                          font_history = pygame.font.SysFont("Calibri", 20, True, False)
                          history_text = font_history.render(f"{test}", True, "White")

                          screen.blit(history_text, [screen_width // 2 - screen_width // 2.5, y_coord])
                          button_back_home.Update_back_home( )

            y_coord1 = 120
            for h,g in highscore_history["Time_set"].items():
                y_coord1 += 40
                font_history = pygame.font.SysFont("Calibri", 20, True, False)
                time_text = font_history.render(f"Date: {g}", True, "White")

                screen.blit(time_text, [(screen_width // 2 - screen_width // 2.5) + 300, y_coord1])
                button_back_home.Update_back_home( )















    if game_over and settings:


        screen.fill((0, 0, 100))

        font_go = pygame.font.SysFont("Calibri", 100, True, False)
        settings_text = font_go.render("Settings", True, "White")
        screen.blit(settings_text,[screen_width // 2 - screen_width // 2.5,100])
        button_back_home.Update_back_home()
        for event in events:
          main_game.Quit(event)
        button_difficulty.Update_difficulty()
        button_volume.update_volume()
        if difficult:
            button_difficulty.text_input()


        if volume_got_clicked:
            volume.draw( )


    FPS.tick(60)
    pygame.display.flip()






