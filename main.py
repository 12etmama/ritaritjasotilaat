import pygame
import random
import sys
import math

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

# Pelaajan asetukset
player_size = 50
player_pos = [width // 2, height // 2]
player_speed = 5

# Ladataan pelaajan kuva
player_image = pygame.image.load("ritari.png")
player_image = pygame.transform.scale(player_image, (player_size, player_size))

# Hirviön asetukset
monster_size = 50
monster_speed = 3
monster_spawn_distance = 200

# Ladataan hirviön kuva
monster_image = pygame.image.load("hirvio.png")
monster_image = pygame.transform.scale(monster_image, (monster_size, monster_size))

def create_monsters(num_monsters):
    monsters = []
    for _ in range(num_monsters):
        monster_pos = [random.randint(0, width-monster_size), random.randint(0, height-monster_size)]
        monster_dir = [random.choice([-1, 1]), random.choice([-1, 1])]
        monsters.append([monster_pos, monster_dir])
    return monsters

def move_monsters(monsters):
    for monster in monsters:
        monster_pos, monster_dir = monster

        distance_to_player = math.sqrt((monster_pos[0] - player_pos[0]) ** 2 + (monster_pos[1] - player_pos[1]) ** 2)
        if distance_to_player < monster_spawn_distance:
            # Liikuta pelaajaa kohti
            if monster_pos[0] < player_pos[0]:
                monster_pos[0] += monster_speed
            if monster_pos[0] > player_pos[0]:
                monster_pos[0] -= monster_speed
            if monster_pos[1] < player_pos[1]:
                monster_pos[1] += monster_speed
            if monster_pos[1] > player_pos[1]:
                monster_pos[1] -= monster_speed
        else:
            # Liikuta satunnaisesti laajemmin
            if random.random() < 0.05:  # Satunnainen suunnan muutos
                monster_dir[0] = random.choice([-1, 1])
                monster_dir[1] = random.choice([-1, 1])
            monster_pos[0] += monster_dir[0] * monster_speed
            monster_pos[1] += monster_dir[1] * monster_speed

        # Tarkistetaan törmäykset muiden hirviöiden kanssa
        for other_monster in monsters:
            if other_monster == monster:
                continue
            other_pos, other_dir = other_monster
            distance = math.sqrt((monster_pos[0] - other_pos[0]) ** 2 + (monster_pos[1] - other_pos[1]) ** 2)
            if distance < monster_size:
                # Hirviöt liikkuvat hetkellisesti eri suuntiin
                if distance == 0:
                    monster_pos[0] += random.choice([-1, 1])
                    monster_pos[1] += random.choice([-1, 1])
                else:
                    overlap = monster_size - distance
                    move_x = overlap * (monster_pos[0] - other_pos[0]) / distance
                    move_y = overlap * (monster_pos[1] - other_pos[1]) / distance
                    monster_pos[0] += move_x / 2
                    monster_pos[1] += move_y / 2
                    other_pos[0] -= move_x / 2
                    other_pos[1] -= move_y / 2

        # Pidä hirviöt pelialueen sisällä
        if monster_pos[0] < 0:
            monster_pos[0] = 0
        if monster_pos[0] > width - monster_size:
            monster_pos[0] = width - monster_size
        if monster_pos[1] < 0:
            monster_pos[1] = 0
        if monster_pos[1] > height - monster_size:
            monster_pos[1] = height - monster_size

def check_collision(player_pos, monsters):
    for monster in monsters:
        monster_pos, _ = monster
        if (abs(player_pos[0] - monster_pos[0]) < player_size and
            abs(player_pos[1] - monster_pos[1]) < player_size):
            return monster
    return None

def draw_entities(player_pos, monsters, player_health):
    win.fill(white)
    win.blit(player_image, (player_pos[0], player_pos[1]))
    for monster_pos, _ in monsters:
        win.blit(monster_image, (monster_pos[0], monster_pos[1]))
    font = pygame.font.Font(None, 36)
    text = font.render(f'Health: {player_health}', True, black)
    win.blit(text, (10, 10))
    pygame.display.update()

def main(num_monsters, player_health):
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
        monster = check_collision(player_pos, monsters)
        if monster:
            player_health -= 1
            if player_health == 0:
                game_over = True
            monsters.remove(monster)
            new_monster_pos = [random.randint(0, width-monster_size), random.randint(0, height-monster_size)]
            new_monster_dir = [random.choice([-1, 1]), random.choice([-1, 1])]
            monsters.append([new_monster_pos, new_monster_dir])

        draw_entities(player_pos, monsters, player_health)
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Käyttö: python peli.py <hirviöiden määrä> <pelaajan terveys>")
        sys.exit(1)

    num_monsters = int(sys.argv[1])
    player_health = int(sys.argv[2])
    main(num_monsters, player_health)
