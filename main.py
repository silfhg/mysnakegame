import os
import sys

import pygame
import random
import pygame_menu
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
pygame.init()
pygame.mixer.music.load('music.mp3')
pygame.mixer.music.play(-1)

screen_width = 600
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

menu = pygame_menu.Menu('go to play', 500, 500,
                        theme=pygame_menu.themes.THEME_GREEN)


def start_the_game():
    green = pygame.Color('#99ff99')
    red = (139, 0, 0, 255)
    font = pygame.font.SysFont("Bahnschrift SemiLight", 20)
    clock = pygame.time.Clock()

    # основные параметры игры
    cell_size = 20
    snake_speed = 10
    snake_length = 3
    snake_body = []

    for i in range(snake_length):
        snake_body.append(pygame.Rect((screen_width / 2) - (cell_size * i), screen_height / 2, cell_size, cell_size))
    snake_direction = "right"
    new_direction = "right"
    apple_position = pygame.Rect(random.randint(0, screen_width - cell_size),
                                 random.randint(0, screen_height - cell_size), cell_size, cell_size)

    game_over = False
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake_direction != "down":
                    new_direction = "up"
                elif event.key == pygame.K_DOWN and snake_direction != "up":
                    new_direction = "down"
                elif event.key == pygame.K_LEFT and snake_direction != "right":
                    new_direction = "left"
                elif event.key == pygame.K_RIGHT and snake_direction != "left":
                    new_direction = "right"

        # новое направление движения
        snake_direction = new_direction
        # управление змейкой
        if snake_direction == "up":
            snake_body.insert(0, pygame.Rect(snake_body[0].left,
                                             snake_body[0].top - cell_size, cell_size, cell_size))
        elif snake_direction == "down":
            snake_body.insert(0, pygame.Rect(snake_body[0].left,
                                             snake_body[0].top + cell_size, cell_size, cell_size))
        elif snake_direction == "left":
            snake_body.insert(0, pygame.Rect(snake_body[0].left - cell_size,
                                             snake_body[0].top, cell_size, cell_size))
        elif snake_direction == "right":
            snake_body.insert(0, pygame.Rect(snake_body[0].left + cell_size,
                                             snake_body[0].top, cell_size, cell_size))

        # проверяем, съела ли змея яблоко
        if snake_body[0].colliderect(apple_position):
            apple_position = pygame.Rect(random.randint(0, screen_width - cell_size),
                                         random.randint(0, screen_height - cell_size), cell_size, cell_size)
            snake_length += 1

        if len(snake_body) > snake_length:
            snake_body.pop()

        # проверка столкновения со стенами
        if (snake_body[0].left < 0 or snake_body[0].right > screen_width or snake_body[0].top < 0 or
                snake_body[0].bottom > screen_height):
            game_over = True

        # проверка столкновения с собственным телом
        for i in range(1, len(snake_body)):
            if snake_body[0].colliderect(snake_body[i]):
                game_over = True

        screen.fill((0, 0, 0))
        # рисуем змейку
        for i in range(len(snake_body)):
            if i == 0:
                pygame.draw.circle(screen, green, snake_body[i].center, cell_size / 2)
            else:
                pygame.draw.circle(screen, green, snake_body[i].center, cell_size / 2)
                pygame.draw.circle(screen, (0, 255, 0), snake_body[i].center, cell_size / 4)

        # рисуем яблоко
        pygame.draw.circle(screen, red, apple_position.center, cell_size / 2)

        # выводим количество яблок
        score_text = font.render(f"apples eaten: {snake_length - 3}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        if game_over:
            screen.fill((0, 0, 0))
            font = pygame.font.SysFont('Bahnschrift SemiLight', 40)
            title = font.render('Game Over', True, (255, 255, 255))
            value = font.render("Your Score: " + f"{snake_length - 3}", True, (255, 255, 255))
            screen.blit(title, (screen_width / 2 - title.get_width() / 2,
                                screen_height / 2 - title.get_height() / 3))
            screen.blit(value, [5, 5])

            pygame.display.update()
            pygame.time.wait(1000)

        pygame.display.flip()
        clock.tick(snake_speed)

    pygame.quit()
    sys.exit()


menu.add.text_input('name:', default='')
menu.add.button('play', start_the_game)
menu.add.button('exit', pygame_menu.events.EXIT)
menu.mainloop(screen)
