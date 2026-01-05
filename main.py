import pygame
from random import randint

#create a window to play on 
pygame.init()
screen = pygame.display.set_mode((800, 400))
clock = pygame.time.Clock()
running = True
start_time = 0
game_font = pygame.font.Font(pygame.font.get_default_font(), 30)
current_time = 0

def display_score():
    current_time = int((pygame.time.get_ticks() - start_time) / 750)
    score_surf = game_font.render(f"Score: {current_time}", True, ("white"))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)

def player_animations():
    global player_surf, player_index
    if player_rect.bottom < 300:
        player_surf = player_surf
    else: 
        player_index += 0.1
        if player_index >= len(player_run):
            player_index = 0
        player_surf = player_run[int(player_index)]
    





is_playing = False
GROUND_Y = 300
JUMP_GRAVITY_START_SPEED = -22
players_gravity_speed = 0


boulder_angle = 0 

boulder_timer = pygame.USEREVENT + 1
pygame.time.set_timer(boulder_timer, 1500)

def obstacles():
    global boulder_timer, boulder_surf 
    new_boulder_rect = boulder_surf.get_rect(bottomleft=(randint(900, 1100), 312))
    boulder_rect_list.append(new_boulder_rect)
    # Reset the timer to a random interval for the next egg
    pygame.time.set_timer(boulder_timer, randint(1000, 1800))

# Intro Screen
start_player = pygame.image.load("graphics/player/start_player.png")
start_player = pygame.transform.scale(start_player, (180, 200))
start_player_rect = start_player.get_rect(center=(400, 200))
start_text = game_font.render("Dino runner", False, "black")
start_text_rect = start_text.get_rect(center=(400, 50))
play_text = game_font.render("Press space to start", False, "Black")
play_text_rect = play_text.get_rect(center=(400, 300))

# Death Screen
death_text = game_font.render("To play again press space", False, "black")
death_text_rect = death_text.get_rect(center=(400, 50))
player_death = pygame.image.load('graphics/player/stick_man_end.png')
player_death = pygame.transform.scale(player_death, (250, 200))
player_death_rect = player_death.get_rect(center=(400, 175))
death_effect = pygame.image.load('graphics/player/deathblood.png')
death_effect = pygame.transform.scale(death_effect, (250, 200))
death_effect_rect = death_effect.get_rect(center=(400, 200))


dungeon_background = pygame.image.load("graphics/level/dungeon_background.png").convert()
dungeon_background = pygame.transform.scale(dungeon_background, (800,400))

player_run1 = pygame.image.load("graphics/player/player1.png").convert_alpha()
player_run1 = pygame.transform.scale(player_run1, (100,100))
player_run2 = pygame.image.load("graphics/player/player2.png").convert_alpha()
player_run2 = pygame.transform.scale(player_run2, (100,100))
player_rect = player_run1.get_rect(midbottom=(80, 350))
player_jump = pygame.image.load("graphics/player/jump.png").convert_alpha()
player_jump = pygame.transform.scale(player_jump, (100,100))
player_run = [player_run1, player_run2]
player_index = 0
player_surf = player_run[player_index]

boulder_surf = pygame.image.load("graphics/enemies/boulder.png").convert_alpha()
boulder_surf = pygame.transform.scale(boulder_surf,(70,70) )
boulder_rect_list = [] 

while running:
   # starting event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if is_playing:
            # Jump Logic
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE or 
                event.type == pygame.MOUSEBUTTONDOWN) and player_rect.bottom >= GROUND_Y:
                players_gravity_speed = JUMP_GRAVITY_START_SPEED
            
            # Spawn Egg Logic (triggered by the timer)
            if event.type == boulder_timer and running:
                obstacles()
        
        else:
        
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                is_playing = True
                boulder_rect_list.clear() 
                player_rect.bottom = GROUND_Y
                players_gravity_speed = 0
                start_time = pygame.time.get_ticks()

    #gameplay
    if is_playing:
      
        screen.blit(dungeon_background, (0, 0))
        
        display_score()

        players_gravity_speed += 1
        player_rect.y += players_gravity_speed
        if player_rect.bottom > GROUND_Y:
            player_rect.bottom = GROUND_Y
        player_animations()
        screen.blit(player_surf, player_rect)
        boulder_angle += 10

        # Egg Movement and Collision Loop
        for boulder_rect in boulder_rect_list[:]: 
            boulder_rect.x -= 6
            if boulder_rect.right < 0:
                boulder_rect_list.remove(boulder_rect) # Clean up memory
            else:
                rotated_boulder = pygame.transform.rotate(boulder_surf, boulder_angle)
                new_rect = rotated_boulder.get_rect(center = boulder_rect.center)
                screen.blit(rotated_boulder, new_rect)
                
            #check for collision
            if player_rect.colliderect(boulder_rect):
                is_playing = False

    # menu
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

    pygame.display.flip()
    clock.tick(60)

pygame.quit()