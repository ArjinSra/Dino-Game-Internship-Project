import pygame
from random import randint

pygame.init()

screen = pygame.display.set_mode((800, 400))
clock = pygame.time.Clock()

running = True
start_time = 0

game_font = pygame.font.Font(pygame.font.get_default_font(), 30)
small_font = pygame.font.Font(pygame.font.get_default_font(), 18)
title_font = pygame.font.Font(pygame.font.get_default_font(), 36)

current_time = 0
high_score = 0
last_score = 0
level = 1

is_playing = False
paused = False
show_instructions = False

new_record = False
record_time = 0

GROUND_Y = 300
players_gravity_speed = 0
JUMP_GRAVITY_START_SPEED = -14

boulder_angle = 0

immunity = False
immunity_start_time = 0
IMMUNITY_DURATION = 5000
show_immunity_banner = False
banner_start_time = 0
immunity_used_this_round = False

banner_colors = ["red", "yellow", "cyan", "green", "magenta"]

lives = 0
MAX_LIVES = 3
hearts_locked = False

PERFECT_WINDOW = 12
perfect_popup_time = 0

heart_image = pygame.image.load("graphics/enemies/heart.png")
heart_image = pygame.transform.scale(heart_image, (30, 30))

MIN_OBSTACLE_GAP = 250

boulder_timer = pygame.USEREVENT + 1
pygame.time.set_timer(boulder_timer, 1500)

menu_background = pygame.image.load("graphics/level/menu_background.png")

start_player = pygame.image.load("graphics/player/start_player.png")
start_player = pygame.transform.scale(start_player, (180, 200))
start_player_rect = start_player.get_rect(center=(400, 200))

title_text = game_font.render("Dungeon Runner", True, "white")
title_rect = title_text.get_rect(center=(400, 50))

start_text = game_font.render("Click to Start", True, "white")
start_rect = start_text.get_rect(center=(400, 300))
start_border = start_rect.inflate(20, 10)

instructions_text = small_font.render("Instructions", True, "white")
instructions_rect = instructions_text.get_rect(center=(70, 200))
instructions_border = instructions_rect.inflate(20, 10)

instructions_surface = pygame.Surface((600, 320)) # Increased height slightly for more text
instructions_surface.fill("black")
instructions_box = instructions_surface.get_rect(center=(400, 200))

exit_text = small_font.render("< exit", True, "white")
exit_rect = exit_text.get_rect(topleft=(instructions_box.left + 10, instructions_box.top + 10))

dungeon_background = pygame.image.load("graphics/level/dungeon_background.png")
dungeon_background = pygame.transform.scale(dungeon_background, (800, 400))

lava_background = pygame.image.load("graphics/level/Lava_Jump_Background.png")
lava_background = pygame.transform.scale(lava_background, (800, 400))

castle_background = pygame.image.load("graphics/level/Lava_Jump_background.png")
castle_background = pygame.transform.scale(castle_background, (800, 400))

player_run1 = pygame.image.load("graphics/player/player1.png")
player_run1 = pygame.transform.scale(player_run1, (100, 100))

player_run2 = pygame.image.load("graphics/player/player2.png")
player_run2 = pygame.transform.scale(player_run2, (100, 100))

player_run = [player_run1, player_run2]
player_index = 0
player_surf = player_run1

player_jump = pygame.image.load("graphics/player/jump.png")
player_jump = pygame.transform.scale(player_jump, (100, 100))

player_crouch = pygame.image.load("graphics/player/crouch.png")
player_crouch = pygame.transform.scale(player_crouch, (100, 50))

player_rect = player_run1.get_rect(midbottom=(80, GROUND_Y))
is_crouching = False

boulder_image = pygame.image.load("graphics/enemies/boulder.png")
boulder_image = pygame.transform.scale(boulder_image, (40, 40))
boulder_rect_list = []

spear_image = pygame.image.load("graphics/enemies/spear1.png")
spear_image = pygame.transform.scale(spear_image, (90, 30))

fireball_image = pygame.image.load("graphics/enemies/fireball.png")
fireball_image = pygame.transform.scale(fireball_image, (50, 50))

arrows_image = pygame.image.load("graphics/enemies/arrows.png")
arrows_image = pygame.transform.scale(arrows_image, (90, 30))

# --- GOLD OBSTACLE LOADING ---
gold_spear_image = pygame.image.load("graphics/enemies/spear1.png")
gold_spear_image = pygame.transform.scale(gold_spear_image, (90, 30))
gold_spear_image.fill((255, 215, 0), special_flags=pygame.BLEND_RGB_MULT)

gold_fireball_image = pygame.image.load("graphics/enemies/fireball.png")
gold_fireball_image = pygame.transform.scale(gold_fireball_image, (50, 50))
gold_fireball_image.fill((255, 215, 0), special_flags=pygame.BLEND_RGB_MULT)

gold_arrows_image = pygame.image.load("graphics/enemies/arrows.png")
gold_arrows_image = pygame.transform.scale(gold_arrows_image, (90, 30))
gold_arrows_image.fill((255, 215, 0), special_flags=pygame.BLEND_RGB_MULT)

spear_rect_list = []
gold_status_list = [] 

SPEAR_Y = 220
game_speed = 6

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if not is_playing:

            if event.type == pygame.MOUSEBUTTONDOWN:

                if start_border.collidepoint(event.pos) and not show_instructions:
                    is_playing = True
                    paused = False
                    start_time = pygame.time.get_ticks()
                    boulder_rect_list.clear()
                    spear_rect_list.clear()
                    gold_status_list.clear()
                    player_rect.midbottom = (80, GROUND_Y)
                    immunity = False
                    immunity_used_this_round = False
                    hearts_locked = False
                    new_record = False
                    current_time = 0
                    lives = 0
                    level = 1

                if instructions_border.collidepoint(event.pos):
                    show_instructions = True

                if exit_rect.collidepoint(event.pos):
                    show_instructions = False

        else:

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_p:
                    paused = not paused
                    show_instructions = False

                if not paused and not show_immunity_banner:

                    if (event.key == pygame.K_SPACE or event.key == pygame.K_UP) and player_rect.bottom >= GROUND_Y:
                        for b in boulder_rect_list:
                            if abs(b.left - player_rect.right) <= PERFECT_WINDOW:
                                current_time += 5
                                perfect_popup_time = pygame.time.get_ticks()
                        players_gravity_speed = JUMP_GRAVITY_START_SPEED

                    if event.key == pygame.K_DOWN:
                        is_crouching = True

                    if event.key == pygame.K_i and not immunity and not immunity_used_this_round:
                        show_immunity_banner = True
                        banner_start_time = pygame.time.get_ticks()
                        immunity_used_this_round = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    is_crouching = False

            if event.type == boulder_timer and not paused and not show_immunity_banner:
                spawn_x = randint(900, 1100)
                if randint(0, 1) == 0:
                    boulder_rect_list.append(boulder_image.get_rect(bottomleft=(spawn_x, 312)))
                else:
                    new_spear_rect = flying_obstacle.get_rect(midbottom=(spawn_x, SPEAR_Y))
                    spear_rect_list.append(new_spear_rect)
                    
                    if randint(1, 10) == 1: 
                        gold_status_list.append(True)
                    else:
                        gold_status_list.append(False)
                        
                spawn_delay = max(600, 1500 - game_speed * 60)
                pygame.time.set_timer(boulder_timer, spawn_delay)

    if is_playing:

        # level system
        score_div = 750
        if current_time >= 200:
            level = 2
            score_div = 600
        if current_time >= 400:
            level = 3
            score_div = 500

        current_time = int((pygame.time.get_ticks() - start_time) / score_div)

        if level == 1:
            screen.blit(dungeon_background, (0, 0))
            flying_obstacle = spear_image
            gold_obstacle = gold_spear_image
        elif level == 2:
            screen.blit(lava_background, (0, 0))
            flying_obstacle = fireball_image
            gold_obstacle = gold_fireball_image
        else:
            screen.blit(castle_background, (0, 0))
            flying_obstacle = arrows_image
            gold_obstacle = gold_arrows_image

        if show_immunity_banner:
            elapsed = pygame.time.get_ticks() - banner_start_time
            color = banner_colors[(elapsed // 200) % len(banner_colors)]
            banner = title_font.render("IMMUNITY ACTIVATED!", True, color)
            screen.blit(banner, banner.get_rect(center=(400, 200)))
            if elapsed >= 2000:
                show_immunity_banner = False
                immunity = True
                immunity_start_time = pygame.time.get_ticks()

        elif paused:
            screen.blit(title_font.render("PAUSED", True, "white"), (330, 120))
            screen.blit(small_font.render("P - Resume", True, "white"), (320, 170))
            screen.blit(small_font.render("I - Instructions", True, "white"), (320, 200))
            screen.blit(small_font.render("M - Main Menu", True, "white"), (320, 230))
            keys = pygame.key.get_pressed()
            if keys[pygame.K_i]:
                show_instructions = True
            if keys[pygame.K_m]:
                is_playing = False
                paused = False

        if not hearts_locked:
            lives = min(current_time // 100, MAX_LIVES)
            if lives >= MAX_LIVES:
                hearts_locked = True

        if current_time > high_score and current_time > 10 and not new_record:
            new_record = True
            record_time = pygame.time.get_ticks()

        game_speed = min(18, 6 + current_time // 2)

        players_gravity_speed += 1
        player_rect.y += players_gravity_speed
        if player_rect.bottom > GROUND_Y:
            player_rect.bottom = GROUND_Y

        if player_rect.bottom < GROUND_Y:
            player_surf = player_jump
        else:
            player_index += 0.1
            if player_index >= len(player_run):
                player_index = 0
            player_surf = player_run[int(player_index)]

        if is_crouching:
            player_draw_rect = player_crouch.get_rect(midbottom=(player_rect.centerx, GROUND_Y))
            screen.blit(player_crouch, player_draw_rect)
            collision_rect = player_draw_rect
        else:
            screen.blit(player_surf, player_rect)
            collision_rect = player_rect

        boulder_angle += 10

        if immunity:
            remaining = (IMMUNITY_DURATION - (pygame.time.get_ticks() - immunity_start_time)) / 1000
            if remaining < 0:
                immunity = False
            else:
                screen.blit(small_font.render("Immunity: " + str(round(remaining,1)), True, "yellow"), (10, 10))

        for i in range(lives):
            screen.blit(heart_image, (700 + i * 35, 10))

        for b in boulder_rect_list[:]:
            b.x -= game_speed
            rot = pygame.transform.rotate(boulder_image, boulder_angle)
            screen.blit(rot, rot.get_rect(center=b.center))
            if not immunity and collision_rect.colliderect(b):
                lives -= 1
                boulder_rect_list.remove(b)
                if lives <= 0:
                    is_playing = False
                    last_score = current_time

        for i in range(len(spear_rect_list) - 1, -1, -1):
            s = spear_rect_list[i]
            is_gold = gold_status_list[i]
            
            s.x -= game_speed
            
            if is_gold:
                screen.blit(gold_obstacle, s)
            else:
                screen.blit(flying_obstacle, s)
                
            if collision_rect.colliderect(s):
                if is_gold:
                    immunity = True
                    immunity_start_time = pygame.time.get_ticks()
                    spear_rect_list.pop(i)
                    gold_status_list.pop(i)
                elif not immunity:
                    lives -= 1
                    spear_rect_list.pop(i)
                    gold_status_list.pop(i)
                    if lives <= 0:
                        is_playing = False
                        last_score = current_time

        if perfect_popup_time and pygame.time.get_ticks() - perfect_popup_time < 700:
            screen.blit(small_font.render("PERFECT +5", True, "cyan"), (340, 90))

        if new_record and pygame.time.get_ticks() - record_time < 2000:
            screen.blit(game_font.render("NEW HIGHSCORE!", True, "yellow"), (280, 70))
        elif new_record:
            high_score = current_time

        screen.blit(game_font.render(str(current_time), True, "white"), (380, 40))

    else:
        screen.blit(menu_background, (0, 0))
        screen.blit(start_player, start_player_rect)
        screen.blit(title_text, title_rect)

        pygame.draw.rect(screen, "green", start_border, 3)
        screen.blit(start_text, start_rect)

        pygame.draw.rect(screen, "black", instructions_border)
        screen.blit(instructions_text, instructions_rect)

        screen.blit(game_font.render("High score: " + str(high_score), True, "white"), (300, 360))

        if show_instructions:
            screen.blit(instructions_surface, instructions_box)
            screen.blit(exit_text, exit_rect)
            screen.blit(title_font.render("Instructions", True, "white"), (instructions_box.centerx - 90, instructions_box.top + 20))
            
            # --- UPDATED INSTRUCTIONS TEXT ---
            screen.blit(small_font.render("- Jump with SPACE or UP", True, "white"), (instructions_box.left + 40, instructions_box.top + 70))
            screen.blit(small_font.render("- Duck with DOWN", True, "white"), (instructions_box.left + 40, instructions_box.top + 95))
            screen.blit(small_font.render("- Press I once per run for immunity", True, "white"), (instructions_box.left + 40, instructions_box.top + 120))
            screen.blit(small_font.render("- Perfect jumps give bonus points", True, "white"), (instructions_box.left + 40, instructions_box.top + 145))
            screen.blit(small_font.render("- Watch out for the golden flying obstacles, Maybe try hitting them", True, "yellow"), (instructions_box.left + 40, instructions_box.top + 175))
            screen.blit(small_font.render("- New level every 200 points (faster points & new obstacles)", True, "white"), (instructions_box.left + 40, instructions_box.top + 205))
            screen.blit(small_font.render("- Each 100 points you get a life, maxing out at three", True, "white"), (instructions_box.left + 40, instructions_box.top + 235))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()