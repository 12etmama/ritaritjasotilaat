import pygame
import random

# Pygame init
pygame.init()

# Asetukset
# width, height = 1024, 800
info = pygame.display.Info()
width, height = info.current_w, info.current_h
win = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
# win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Ritari ja Sotilaat")

# Värit
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# Pelaajan asetukset
player_size = 50
player_pos = [width // 2, height // 2]
player_speed = 5

# Hirviön asetukset
monster_size = 50
monster_pos = [random.randint(0, width-monster_size), random.randint(0, height-monster_size)]
monster_speed = 1

clock = pygame.time.Clock()

# Pääsilmukka
game_over = False
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and player_pos[0] > 0:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT] and player_pos[0] < width - player_size:
        player_pos[0] += player_speed
    if keys[pygame.K_UP] and player_pos[1] > 0:
        player_pos[1] -= player_speed
    if keys[pygame.K_DOWN] and player_pos[1] < height - player_size:
        player_pos[1] += player_speed

    # Hirviön liike
    if monster_pos[0] < player_pos[0]:
        monster_pos[0] += monster_speed
    if monster_pos[0] > player_pos[0]:
        monster_pos[0] -= monster_speed
    if monster_pos[1] < player_pos[1]:
        monster_pos[1] += monster_speed
    if monster_pos[1] > player_pos[1]:
        monster_pos[1] -= monster_speed

    # Törmäyksen tarkistus
    if (abs(player_pos[0] - monster_pos[0]) < player_size and
        abs(player_pos[1] - monster_pos[1]) < player_size):
        game_over = True

    win.fill(white)

    pygame.draw.rect(win, black, (player_pos[0], player_pos[1], player_size, player_size))
    pygame.draw.rect(win, red, (monster_pos[0], monster_pos[1], monster_size, monster_size))

    pygame.display.update()

    clock.tick(30)

pygame.quit()
