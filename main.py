import pygame
import sys
import random

#каркас
pygame.init()
basic_window_width = 1200
basic_window_height = 800

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

#рандомные цвета
random_color = ['red', 'green', 'blue', 'orange', 'pink', 'magenta', 'brown']

#картинки
backgroung_image = pygame.image.load('image_')
backgroung_image = pygame.transform.scale(backgroung_image, (1000, 600))

basic_window_title = pygame.display.set_caption('PonG')
basic_window_icon = pygame.display.set_icon(pygame.image.load('image_for_pong/icon.png'))
basic_window = pygame.display.set_mode((basic_window_width, basic_window_height), pygame.FULLSCREEN)

game_window_width = 1000
game_window_height = 600
game_window = pygame.Surface((game_window_width, game_window_height))

#игровые переменные и константы
GAME = True
fps = 60
timer_fps = pygame.time.Clock()
score_player1 = 0
score_player2 = 0
speed_ball = 3
end_score = 3

#направления
ball_move_right = True
ball_move_top = False

#звуки
pygame.mixer.music.load('sound/zaglavnaja-tema-mortal-kombat-8-bit.mp3')
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1) # -1 чтобы постоянно играла

paddle = pygame.mixer.Sound('sound/gromkiy-udar-raketkoy.mp3')
paddle.set_volume(1)
laugh = pygame.mixer.Sound('sound/mji3nde5ntg0mji3nde0_c_2b1cpabqhho.mp3')
laugh.set_volume(1)
game_over = pygame.mixer.Sound('sound/95-its-official.mp3')
game_over.set_volume(1)

#текст для счёта
player1_font = pygame.font.SysFont('Arial', 30)
player2_font = pygame.font.SysFont('Arial', 30)
game_over_font = pygame.font.SysFont('Arial', 100, bold=True)

#ИГроки
surf_player1 = pygame.Surface((20, 100))
random_color_player1 = random.choice(random_color)
surf_player1.fill(pygame.Color(random_color_player1))
player1 = surf_player1.get_rect()
player1.x = 0
player1.y = 150

surf_player2 = pygame.Surface((20, 100))
random_color_player2 = random.choice(random_color)
surf_player1.fill(pygame.Color(random_color_player2))
player2 = surf_player1.get_rect()
player2.x = 980
player2.y = 150

#мяч
image_ball = pygame.image.load('image_for_pong/ball.png').convert_alpha()
image_ball = pygame.transform.scale(image_ball, (30, 30))
ball = image_ball.get_rect()
ball.x = game_window_width // 2 - 15
ball.y = game_window_height // 2 - 15

#функции для игры
#закрытие
def close_game_fullscreen():
    key = pygame.key.get_pressed()
    if key[pygame.K_ESCAPE]:
        pygame.quit()
        sys.exit()

def game_close():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

#управление
def player1_control():
    key_player = pygame.key.get_pressed()
    if key_player[pygame.K_w] and player1.y > 0:
        player1.y -= 10
    elif key_player[pygame.K_s] and player1.bottom < game_window_height:
        player1.y += 10

def player2_control():
    key_player = pygame.key.get_pressed()
    if key_player[pygame.K_UP] and player2.y > 0:
        player2.y -= 10
    elif key_player[pygame.K_DOWN] and player2.bottom < game_window_height:
        player2.y += 10

while GAME:
    timer_fps.tick(fps)


    basic_window.fill(BLACK)
    basic_window.blit(game_window, (100, 100))
    game_window.blit(backgroung_image, (0, 0))

    close_game_fullscreen()
    game_close()

    #Стартовые позиции
    game_window.blit(surf_player1, player1)
    game_window.blit(surf_player2, player2)
    game_window.blit(image_ball, ball)

    #управление
    player1_control()
    player2_control()

    #движение мяча
    #вверх
    if ball_move_top == True:
        ball.y -= speed_ball
    else:
        ball.y += speed_ball

    #вправо
    if ball_move_right == True:
        ball.x += speed_ball
    else:
        ball.x -= speed_ball

    if ball.y <= 0:
        ball_move_top = False
    if ball.y >= game_window_height:
        ball_move_top = True

    #Столкновиние
    if ball.colliderect(player1):
        paddle.play()
        ball_move_right = True
        speed_ball += 0.5

    if ball.colliderect(player2):
        paddle.play()
        ball_move_right = False
        speed_ball += 0.5


    if ball.x + 30 >= game_window_width:
        score_player1 +=1
        if score_player1 < end_score:
             laugh.play()
             ball.x = game_window_width // 2 -15
             ball.y = game_window_height // 2 - 15
             speed_ball = 3

    if ball.x <= 0:
        score_player2 +=1
        if score_player2 < end_score:
             laugh.play()
             ball.x = game_window_width // 2 -15
             ball.y = game_window_height // 2 - 15
             speed_ball = 3


    #текст игры
    render_player1_font = player1_font.render(f'Player 1: {score_player1}', True, WHITE)
    render_player2_font = player2_font.render(f'Player 2: {score_player2}', True, WHITE)
    render_game_over = game_over_font.render('GAME OVER', True, RED)

    basic_window.blit(render_player1_font, (0, 50))
    basic_window.blit(render_player2_font, (1090, 50))

    #
    if score_player1 >= end_score or score_player2 >= end_score:
        pygame.mixer.music.stop()
        game_over.play()
    #    while True:


    #end
    pygame.display.update()