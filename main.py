import pygame
import random
import sys

# Pygame init
pygame.init()

# Asetukset
info = pygame.display.Info()
width, height = info.current_w, info.current_h
win = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
pygame.display.set_caption("Peli")

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
monster_speed = 1

def create_monsters(num_monsters):
    monsters = []
    for _ in range(num_monsters):
        monster_pos = [random.randint(0, width-monster_size), random.randint(0, height-monster_size)]
        monsters.append(monster_pos)
    return monsters

def move_monsters(monsters):
    for monster_pos in monsters:
        if monster_pos[0] < player_pos[0]:
            monster_pos[0] += monster_speed
        if monster_pos[0] > player_pos[0]:
            monster_pos[0] -= monster_speed
        if monster_pos[1] < player_pos[1]:
            monster_pos[1] += monster_speed
        if monster_pos[1] > player_pos[1]:
            monster_pos[1] -= monster_speed

def check_collision(player_pos, monsters):
    for monster_pos in monsters:
        if (abs(player_pos[0] - monster_pos[0]) < player_size and
            abs(player_pos[1] - monster_pos[1]) < player_size):
            return True
    return False

def draw_entities(player_pos, monsters):
    win.fill(white)
    pygame.draw.rect(win, black, (player_pos[0], player_pos[1], player_size, player_size))
    for monster_pos in monsters:
        pygame.draw.rect(win, red, (monster_pos[0], monster_pos[1], monster_size, monster_size))
    pygame.display.update()

def main(num_monsters):
    monsters = create_monsters(num_monsters)
    clock = pygame.time.Clock()
    game_over = False
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            game_over = True
        if keys[pygame.K_LEFT] and player_pos[0] > 0:
            player_pos[0] -= player_speed
        if keys[pygame.K_RIGHT] and player_pos[0] < width - player_size:
            player_pos[0] += player_speed
        if keys[pygame.K_UP] and player_pos[1] > 0:
            player_pos[1] -= player_speed
        if keys[pygame.K_DOWN] and player_pos[1] < height - player_size:
            player_pos[1] += player_speed

        move_monsters(monsters)
        if check_collision(player_pos, monsters):
            game_over = True

        draw_entities(player_pos, monsters)
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Käyttö: python peli.py <hirviöiden määrä>")
        sys.exit(1)

    num_monsters = int(sys.argv[1])
    main(num_monsters)
