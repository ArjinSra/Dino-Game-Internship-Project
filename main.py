import pygame
from random import randint

# Create a window to play on
pygame.init()
screen = pygame.display.set_mode((800, 400))
clock = pygame.time.Clock()
running = True
start_time = 0
game_font = pygame.font.Font(pygame.font.get_default_font(), 30)
current_time = 0
high_score = 0
is_playing = False
GROUND_Y = 300
JUMP_GRAVITY_START_SPEED = -14
players_gravity_speed = 0
boulder_angle = 0
# Immunity variables
immunity = False
immunity_start_time = 0
IMMUNITY_DURATION = 5000
show_immunity_banner = False
banner_start_time = 0

def display_score():
    global current_time
    current_time = int((pygame.time.get_ticks() - start_time) / 750)
    score_surf = game_font.render(f"Score: {current_time}", True, ("white"))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)

def player_animations():
    global player_surf, player_index
    if player_rect.bottom < GROUND_Y:
        player_surf = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_run):
            player_index = 0
        player_surf = player_run[int(player_index)]

boulder_timer = pygame.USEREVENT + 1
pygame.time.set_timer(boulder_timer, 1500)

def obstacles():
    global boulder_timer
    if randint(0,1) == 0:
        new_rect = boulder_surf.get_rect(bottomleft=(randint(900, 1100), 312))
        boulder_rect_list.append(new_rect)
    else:
        new_rect = spear_surf.get_rect(midbottom=(randint(900,1100), SPEAR_Y))
        spear_list.append(new_rect)
    pygame.time.set_timer(boulder_timer, randint(900, 1600))

# Intro Screen
start_player = pygame.image.load("graphics/player/start_player.png")
start_player = pygame.transform.scale(start_player, (180, 200))
start_player_rect = start_player.get_rect(center=(400, 200))
start_text = game_font.render("Dungeon runner", False, "black")
start_text_rect = start_text.get_rect(center=(400, 50))
play_text = game_font.render("Press space to start", False, "Black")
play_text_rect = play_text.get_rect(center=(400, 300))

# Death Screen
death_text = game_font.render("To play again press space", False, "black")
death_text_rect = death_text.get_rect(center=(400, 50))
player_death = pygame.image.load('graphics/player/dead.png')
player_death = pygame.transform.scale(player_death, (230, 230))
player_death_rect = player_death.get_rect(center=(400, 210))
death_effect = pygame.image.load('graphics/player/deathblood.png')
death_effect = pygame.transform.scale(death_effect, (250, 200))
death_effect_rect = death_effect.get_rect(center=(400, 200))

dungeon_background = pygame.image.load("graphics/level/dungeon_background.png").convert()
dungeon_background = pygame.transform.scale(dungeon_background, (800,400))

# Player images
player_run1 = pygame.image.load("graphics/player/player1.png").convert_alpha()
player_run1 = pygame.transform.scale(player_run1, (100,100))
player_run2 = pygame.image.load("graphics/player/player2.png").convert_alpha()
player_run2 = pygame.transform.scale(player_run2, (100,100))
player_run = [player_run1, player_run2]
player_index = 0
player_surf = player_run[player_index]
player_jump = pygame.image.load("graphics/player/jump.png").convert_alpha()
player_jump = pygame.transform.scale(player_jump, (100,100))
player_crouch = pygame.image.load("graphics/player/crouch.png").convert_alpha()
player_crouch = pygame.transform.scale(player_crouch, (100,50))
player_rect = player_run1.get_rect(midbottom=(80, GROUND_Y))
is_crouching = False

# Obstacles
boulder_surf = pygame.image.load("graphics/enemies/boulder.png").convert_alpha()
boulder_surf = pygame.transform.scale(boulder_surf,(40,40))
boulder_rect_list = []

spear_surf = pygame.image.load("graphics/enemies/spear1.png").convert_alpha()
spear_surf = pygame.transform.scale(spear_surf, (90,30))
spear_list = []
SPEAR_Y = 220

game_speed = 6

# More graphics (Immunity timer)
immunity_time = IMMUNITY_DURATION/1000
immunity_timer = game_font.render(f"IMMUNITY:{immunity_time}", False, "White")
immunity_rect = immunity_timer.get_rect(center = (20,20))


while running:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            running = False

        elif is_playing:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE  or event.key == pygame.K_UP and player_rect.bottom >= GROUND_Y:
                    players_gravity_speed = JUMP_GRAVITY_START_SPEED
                elif event.key == pygame.K_DOWN and player_rect.bottom >= GROUND_Y:
                    is_crouching = True
                elif event.key == pygame.K_i:  # Press I for immunity
                    immunity = True
                    immunity_start_time = pygame.time.get_ticks()
                    show_immunity_banner = True
                    banner_start_time = pygame.time.get_ticks()


            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    is_crouching = False

            elif event.type == boulder_timer and running:
                obstacles()

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                is_playing = True
                boulder_rect_list.clear()
                spear_list.clear()
                player_rect.midbottom = (80, GROUND_Y)
                players_gravity_speed = 0
                start_time = pygame.time.get_ticks()
                immunity = False  # reset immunity on restart
                is_crouching = False

    if is_playing:
        screen.blit(dungeon_background, (0, 0))
        # IMMUNITY ACTIVATED BANNER
        if show_immunity_banner:
            elapsed = pygame.time.get_ticks() - banner_start_time

            if elapsed < 2000:
                colors = ["red", "yellow", "orange", "white"]
                color = colors[(elapsed // 150) % len(colors)]

                banner = game_font.render("IMMUNITY ACTIVATED!", True, color)
                banner_rect = banner.get_rect(center=(400, 200))
                screen.blit(banner, banner_rect)
        
                pygame.display.flip()
                clock.tick(60)
                continue   
            else:
                show_immunity_banner = False



        display_score()
        # Increase speed but cap at 16
        game_speed = min(16, 6 + current_time // 2)

        # Gravity
        players_gravity_speed += 1
        player_rect.y += players_gravity_speed
        if player_rect.bottom > GROUND_Y:
            player_rect.bottom = GROUND_Y
        if immunity:
            elapsed = pygame.time.get_ticks() - immunity_start_time
            remaining_time =  (IMMUNITY_DURATION - elapsed)
            seconds_left = max(0,remaining_time//1000)
            immunity_text = game_font.render(f"IMMUNITY:{seconds_left}", False, "white")
            screen.blit(immunity_text, (20,20))

        player_animations()

        # Determine hitbox (normal or crouch)
        if is_crouching and player_rect.bottom >= GROUND_Y:
            collision_rect = player_crouch.get_rect(midbottom=(player_rect.centerx, GROUND_Y))
            screen.blit(player_crouch, collision_rect)
        else:
            collision_rect = player_rect
            screen.blit(player_surf, player_rect)

        boulder_angle += 10

        # Immunity timer
        if immunity and pygame.time.get_ticks() - immunity_start_time > IMMUNITY_DURATION:
            immunity = False

        # Boulder movement & collision
        for boulder_rect in boulder_rect_list[:]:
            boulder_rect.x -= game_speed
            if boulder_rect.right < 0:
                boulder_rect_list.remove(boulder_rect)
            else:
                rotated_boulder = pygame.transform.rotate(boulder_surf, boulder_angle)
                new_rect = rotated_boulder.get_rect(center=boulder_rect.center)
                screen.blit(rotated_boulder, new_rect)
                if not immunity and collision_rect.colliderect(boulder_rect):
                    is_playing = False

        # Spear movement & collision
        for spear_rect in spear_list[:]:
            spear_rect.x -= game_speed
            if spear_rect.right < 0:
                spear_list.remove(spear_rect)
            else:
                screen.blit(spear_surf, spear_rect)
                if not immunity and collision_rect.colliderect(spear_rect):
                    is_playing = False

        # Update high score
        if current_time > high_score:
            high_score = current_time

    else:
        if current_time == 0:
            screen.fill("white")
            screen.blit(play_text, play_text_rect)
            screen.blit(start_player, start_player_rect)
            screen.blit(start_text, start_text_rect)
        else:
            screen.fill("dark grey")
            score_message = game_font.render(f'Your score: {current_time}', False, "black")
            score_message_rect = score_message.get_rect(center=(400, 300))
            screen.blit(score_message, score_message_rect)
            screen.blit(death_effect, death_effect_rect)
            screen.blit(player_death, player_death_rect)
            screen.blit(death_text, death_text_rect)

        # Draw high score on menu & death screen
        high_score_text = game_font.render(f"High score: {high_score}", False, "black")
        high_score_rect = high_score_text.get_rect(midbottom=(400, 380))
        screen.blit(high_score_text, high_score_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()