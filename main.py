import pygame
from random import randint

pygame.init()

# Setup the window and the clock for controlling frame rate
screen = pygame.display.set_mode((800, 400))
clock = pygame.time.Clock()

running = True
start_time = 0

# Fonts for different text sizes
game_font = pygame.font.Font(pygame.font.get_default_font(), 30)
small_font = pygame.font.Font(pygame.font.get_default_font(), 18)
title_font = pygame.font.Font(pygame.font.get_default_font(), 36)

# Game state variables
current_time = 0
high_score = 0
last_score = 0
level = 1

is_playing = False
paused = False
show_instructions = False

new_record = False
record_time = 0

# Physics and Movement constants
GROUND_Y = 300
players_gravity_speed = 0
JUMP_GRAVITY_START_SPEED = -14

boulder_angle = 0

# Immunity system variables
immunity = False
immunity_start_time = 0
IMMUNITY_DURATION = 5000
show_immunity_banner = False
banner_start_time = 0
immunity_used_this_round = False

banner_colors = ["red", "yellow", "cyan", "green", "magenta"]

# Health system variables
lives = 0
MAX_LIVES = 3
hearts_locked = False

# Scoring bonuses
PERFECT_WINDOW = 12
perfect_popup_time = 0

# Load images
heart_image = pygame.image.load("graphics/enemies/heart.png")
heart_image = pygame.transform.scale(heart_image, (30, 30))

MIN_OBSTACLE_GAP = 250

# Custom event for spawning obstacles every 1.5 seconds
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

# Create a full-screen surface for instructions
instructions_surface = pygame.Surface((800, 400)) 
instructions_surface.fill("black")
instructions_box = instructions_surface.get_rect(topleft=(0, 0))

exit_text = small_font.render("< exit", True, "white")
exit_rect = exit_text.get_rect(topleft=(20, 20))

# Environment backgrounds
dungeon_background = pygame.image.load("graphics/level/dungeon_background.png")
dungeon_background = pygame.transform.scale(dungeon_background, (800, 400))

lava_background = pygame.image.load("graphics/level/Lava_Jump_Background.png")
lava_background = pygame.transform.scale(lava_background, (800, 400))

castle_background = pygame.image.load("graphics/level/Lava_Jump_background.png")
castle_background = pygame.transform.scale(castle_background, (800, 400))

# Player animation frames
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

# Enemy assets
boulder_image = pygame.image.load("graphics/enemies/boulder.png")
boulder_image = pygame.transform.scale(boulder_image, (40, 40))
boulder_rect_list = []

spear_image = pygame.image.load("graphics/enemies/spear1.png")
spear_image = pygame.transform.scale(spear_image, (90, 30))

fireball_image = pygame.image.load("graphics/enemies/fireball.png")
fireball_image = pygame.transform.scale(fireball_image, (50, 50))

arrows_image = pygame.image.load("graphics/enemies/arrows.png")
arrows_image = pygame.transform.scale(arrows_image, (90, 30))

# Gold versions of obstacles (for immunity power-up)
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

        # Handle mouse clicks for menus
        if event.type == pygame.MOUSEBUTTONDOWN:
            if show_instructions == True:
                if exit_rect.collidepoint(event.pos):
                    show_instructions = False

            if is_playing == False:
                if show_instructions == False:
                    if start_border.collidepoint(event.pos):
                        # Reset game state for a new round
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

        # Handle keyboard input during gameplay
        if is_playing == True:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused
                    show_instructions = False

                if paused == False:
                    if show_immunity_banner == False:
                        if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                            if player_rect.bottom >= GROUND_Y:
                                # Check for "Perfect" timing bonus when jumping over boulders
                                for b in boulder_rect_list:
                                    if abs(b.left - player_rect.right) <= PERFECT_WINDOW:
                                        current_time = current_time + 5
                                        perfect_popup_time = pygame.time.get_ticks()
                                players_gravity_speed = JUMP_GRAVITY_START_SPEED

                        if event.key == pygame.K_DOWN:
                            is_crouching = True

                        if event.key == pygame.K_i:
                            if immunity == False:
                                if immunity_used_this_round == False:
                                    show_immunity_banner = True
                                    banner_start_time = pygame.time.get_ticks()
                                    immunity_used_this_round = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    is_crouching = False

            # Randomly spawn either a ground boulder or a flying obstacle
            if event.type == boulder_timer:
                if paused == False:
                    if show_immunity_banner == False:
                        spawn_x = randint(900, 1100)
                        if randint(0, 1) == 0:
                            boulder_rect_list.append(boulder_image.get_rect(bottomleft=(spawn_x, 312)))
                        else:
                            new_spear_rect = flying_obstacle.get_rect(midbottom=(spawn_x, SPEAR_Y))
                            spear_rect_list.append(new_spear_rect)
                            # 10% chance to spawn a golden version
                            if randint(1, 10) == 1: 
                                gold_status_list.append(True)
                            else:
                                gold_status_list.append(False)
                        
                        # Speed up the spawn rate as the game gets faster
                        spawn_delay = 1500 - (game_speed * 60)
                        if spawn_delay < 600:
                            spawn_delay = 600
                        pygame.time.set_timer(boulder_timer, int(spawn_delay))

    if is_playing == True:
        if paused == False:
            # Difficulty/Level system based on time/score
            score_div = 750
            if current_time >= 200:
                level = 2
                score_div = 600
            if current_time >= 400:
                level = 3
                score_div = 500
            current_time = int((pygame.time.get_ticks() - start_time) / score_div)

        # Set obstacle graphics based on current level
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

        # Immunity Activation Animation
        if show_immunity_banner == True:
            elapsed = pygame.time.get_ticks() - banner_start_time
            color_index = (elapsed // 200) % len(banner_colors)
            color = banner_colors[color_index]
            banner = title_font.render("IMMUNITY ACTIVATED!", True, color)
            screen.blit(banner, banner.get_rect(center=(400, 200)))
            if elapsed >= 2000:
                show_immunity_banner = False
                immunity = True
                immunity_start_time = pygame.time.get_ticks()
        
        elif paused == True:
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

        if paused == False:
            # Grant extra lives every 100 points
            if hearts_locked == False:
                lives = current_time // 100
                if lives > MAX_LIVES:
                    lives = MAX_LIVES
                if lives == MAX_LIVES:
                    hearts_locked = True
            
            # High score logic
            if current_time > high_score:
                if current_time > 10:
                    if new_record == False:
                        new_record = True
                        record_time = pygame.time.get_ticks()
            
            # Gradually increase game speed
            game_speed = 6 + (current_time // 2)
            if game_speed > 18:
                game_speed = 18

            # Apply gravity to the player
            players_gravity_speed = players_gravity_speed + 1
            player_rect.y = player_rect.y + players_gravity_speed
            if player_rect.bottom > GROUND_Y:
                player_rect.bottom = GROUND_Y
            
            # Choose player image (jump vs run animation)
            if player_rect.bottom < GROUND_Y:
                player_surf = player_jump
            else:
                player_index = player_index + 0.1
                if player_index >= len(player_run):
                    player_index = 0
                player_surf = player_run[int(player_index)]

        # Draw player and handle crouching height
        if is_crouching == True:
            player_draw_rect = player_crouch.get_rect(midbottom=(player_rect.centerx, GROUND_Y))
            screen.blit(player_crouch, player_draw_rect)
            collision_rect = player_draw_rect
        else:
            screen.blit(player_surf, player_rect)
            collision_rect = player_rect

        if paused == False:
            boulder_angle = boulder_angle + 10

        # Draw immunity timer if active
        if immunity == True:
            remaining = (IMMUNITY_DURATION - (pygame.time.get_ticks() - immunity_start_time)) / 1000
            if remaining < 0:
                immunity = False
            else:
                screen.blit(small_font.render("Immunity: " + str(round(remaining,1)), True, "yellow"), (10, 10))

        # Draw life hearts
        for i in range(lives):
            screen.blit(heart_image, (700 + (i * 35), 10))

        # Update and draw ground boulders
        for b in boulder_rect_list:
            if paused == False:
                b.x = b.x - game_speed
            rot = pygame.transform.rotate(boulder_image, boulder_angle)
            screen.blit(rot, rot.get_rect(center=b.center))
            if immunity == False:
                if collision_rect.colliderect(b):
                    lives = lives - 1
                    boulder_rect_list.remove(b)
                    if lives < 0:
                        is_playing = False
                        last_score = current_time

        # Update and draw flying obstacles (spears/arrows/fireballs)
        for i in range(len(spear_rect_list) - 1, -1, -1):
            s = spear_rect_list[i]
            is_gold = gold_status_list[i]
            if paused == False:
                s.x = s.x - game_speed
            
            if is_gold == True:
                screen.blit(gold_obstacle, s)
            else:
                screen.blit(flying_obstacle, s)
            
            # Collision logic for flying obstacles
            if collision_rect.colliderect(s):
                if is_gold == True:
                    # Gold obstacles give immunity instead of damage
                    immunity = True
                    immunity_start_time = pygame.time.get_ticks()
                    spear_rect_list.pop(i)
                    gold_status_list.pop(i)
                else:
                    if immunity == False:
                        lives = lives - 1
                        spear_rect_list.pop(i)
                        gold_status_list.pop(i)
                        if lives < 0:
                            is_playing = False
                            last_score = current_time

        # Temporary popups for bonuses
        if perfect_popup_time != 0:
            if pygame.time.get_ticks() - perfect_popup_time < 700:
                screen.blit(small_font.render("PERFECT +5", True, "cyan"), (340, 90))
        
        if new_record == True:
            if pygame.time.get_ticks() - record_time < 2000:
                screen.blit(game_font.render("NEW HIGHSCORE!", True, "yellow"), (280, 70))
            else:
                high_score = current_time
        
        screen.blit(game_font.render(str(current_time), True, "white"), (380, 40))

    else:
        # Main Menu Screen
        screen.blit(menu_background, (0, 0))
        screen.blit(start_player, start_player_rect)
        screen.blit(title_text, title_rect)
        pygame.draw.rect(screen, "green", start_border, 3)
        screen.blit(start_text, start_rect)
        pygame.draw.rect(screen, "black", instructions_border)
        screen.blit(instructions_text, instructions_rect)
        screen.blit(game_font.render("High score: " + str(high_score), True, "white"), (300, 360))

    # Overlays instructions on top of everything else if active
    if show_instructions == True:
        screen.blit(instructions_surface, instructions_box)
        screen.blit(exit_text, exit_rect)
        screen.blit(title_font.render("Instructions", True, "white"), (310, 40))
        screen.blit(small_font.render("- Jump with SPACE or UP", True, "white"), (100, 100))
        screen.blit(small_font.render("- Duck with DOWN", True, "white"), (100, 130))
        screen.blit(small_font.render("- Press I once per run for immunity", True, "white"), (100, 160))
        screen.blit(small_font.render("- Perfect jumps give bonus points", True, "white"), (100, 190))
        screen.blit(small_font.render("- Watch out for the golden flying obstacles, Maybe try hitting them", True, "yellow"), (100, 230))
        screen.blit(small_font.render("- New level every 200 points (faster points & new obstacles)", True, "white"), (100, 270))
        screen.blit(small_font.render("- Each 100 points you get a life, maxing out at three", True, "white"), (100, 310))

    pygame.display.flip()
    # Ensure the game runs at 60 FPS
    clock.tick(60)

pygame.quit()