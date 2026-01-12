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
is_playing = False
show_instructions = False
paused = False

new_record = False
record_time = 0

GROUND_Y = 300
JUMP_GRAVITY_START_SPEED = -14
players_gravity_speed = 0

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

heart_surf = pygame.transform.scale(
    pygame.image.load("graphics/enemies/heart.png").convert_alpha(), (30, 30)
)

MIN_OBSTACLE_GAP = 250

def draw_wrapped_text(surface, text, font, color, rect, spacing=4):
    words = text.split(" ")
    line = ""
    y = rect.top
    for word in words:
        test = line + word + " "
        if font.size(test)[0] <= rect.width:
            line = test
        else:
            surface.blit(font.render(line, True, color), (rect.left, y))
            y += font.get_height() + spacing
            line = word + " "
    surface.blit(font.render(line, True, color), (rect.left, y))

def display_score():
    global current_time, lives, hearts_locked, new_record, record_time
    current_time = int((pygame.time.get_ticks() - start_time) / 750)
    if not hearts_locked:
        lives = min(current_time // 100, MAX_LIVES)
        if lives >= MAX_LIVES:
            hearts_locked = True
    if current_time > high_score and current_time > 10:
        new_record = True
        record_time = pygame.time.get_ticks()
    screen.blit(game_font.render(str(current_time), True, "white"), (380, 40))

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
    last_x = 0
    if boulder_rect_list:
        last_x = boulder_rect_list[-1].x
    elif spear_list:
        last_x = spear_list[-1].x
    spawn_x = randint(900, 1100)
    if spawn_x - last_x < MIN_OBSTACLE_GAP:
        return
    if randint(0,1) == 0:
        boulder_rect_list.append(boulder_surf.get_rect(bottomleft=(spawn_x, 312)))
    else:
        spear_list.append(spear_surf.get_rect(midbottom=(spawn_x, SPEAR_Y)))

menu_background = pygame.image.load("graphics/level/menu_background.png")
start_player = pygame.transform.scale(
    pygame.image.load("graphics/player/start_player.png"), (180, 200)
)
start_player_rect = start_player.get_rect(center=(400, 200))
title_text = game_font.render("Dungeon Runner", True, "white")
title_rect = title_text.get_rect(center=(400, 50))
start_text = game_font.render("Click to Start", True, "white")
start_rect = start_text.get_rect(center=(400, 300))
start_border = start_rect.inflate(20, 10)

instructions_text = small_font.render("Instructions", True, "white")
instructions_rect = instructions_text.get_rect(center=(70, 200))
instructions_border = instructions_rect.inflate(20, 10)

instructions_surface = pygame.Surface((600, 280))
instructions_surface.fill("black")
instructions_box = instructions_surface.get_rect(center=(400, 200))
exit_text = small_font.render("< exit", True, "white")
exit_rect = exit_text.get_rect(topleft=(instructions_box.left + 10, instructions_box.top + 10))

dungeon_background = pygame.transform.scale(
    pygame.image.load("graphics/level/dungeon_background.png").convert(), (800,400)
)

player_run1 = pygame.transform.scale(
    pygame.image.load("graphics/player/player1.png").convert_alpha(), (100,100)
)
player_run2 = pygame.transform.scale(
    pygame.image.load("graphics/player/player2.png").convert_alpha(), (100,100)
)
player_run = [player_run1, player_run2]
player_index = 0
player_surf = player_run1
player_jump = pygame.transform.scale(
    pygame.image.load("graphics/player/jump.png").convert_alpha(), (100,100)
)
player_crouch = pygame.transform.scale(
    pygame.image.load("graphics/player/crouch.png").convert_alpha(), (100,50)
)
player_rect = player_run1.get_rect(midbottom=(80, GROUND_Y))
is_crouching = False

boulder_surf = pygame.transform.scale(
    pygame.image.load("graphics/enemies/boulder.png").convert_alpha(), (40,40)
)
boulder_rect_list = []

spear_surf = pygame.transform.scale(
    pygame.image.load("graphics/enemies/spear1.png").convert_alpha(), (90,30)
)
spear_list = []
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
                    spear_list.clear()
                    player_rect.midbottom = (80, GROUND_Y)
                    immunity = False
                    immunity_used_this_round = False
                    hearts_locked = False
                    new_record = False
                    current_time = 0
                    lives = 0

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
                obstacles()
                spawn_delay = max(600, 1500 - game_speed * 60)
                pygame.time.set_timer(boulder_timer, spawn_delay)

    if is_playing:
        screen.blit(dungeon_background, (0,0))

        if show_immunity_banner:
            elapsed = pygame.time.get_ticks() - banner_start_time
            color = banner_colors[(elapsed // 200) % len(banner_colors)]
            banner = title_font.render("IMMUNITY ACTIVATED!", True, color)
            screen.blit(banner, banner.get_rect(center=(400,200)))
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

        else:
            display_score()
            game_speed = min(18, 6 + current_time // 2)

            players_gravity_speed += 1
            player_rect.y += players_gravity_speed
            if player_rect.bottom > GROUND_Y:
                player_rect.bottom = GROUND_Y

            player_animations()

            collision_rect = (
                player_crouch.get_rect(midbottom=(player_rect.centerx, GROUND_Y))
                if is_crouching else player_rect
            )
            screen.blit(player_crouch if is_crouching else player_surf, collision_rect)

            boulder_angle += 10

            if immunity:
                remaining = max(0, (IMMUNITY_DURATION - (pygame.time.get_ticks() - immunity_start_time)) / 1000)
                screen.blit(small_font.render(f"Immunity: {remaining:.1f}s", True, "yellow"), (10, 10))
                if pygame.time.get_ticks() - immunity_start_time >= IMMUNITY_DURATION:
                    immunity = False

            for i in range(lives):
                screen.blit(heart_surf, (700 + i*35, 10))

            for b in boulder_rect_list[:]:
                b.x -= game_speed
                rotated = pygame.transform.rotate(boulder_surf, boulder_angle)
                screen.blit(rotated, rotated.get_rect(center=b.center))
                if not immunity and collision_rect.colliderect(b):
                    lives -= 1
                    boulder_rect_list.remove(b)
                    if lives <= 0:
                        is_playing = False
                        last_score = current_time

            for s in spear_list[:]:
                s.x -= game_speed
                screen.blit(spear_surf, s)
                if not immunity and collision_rect.colliderect(s):
                    lives -= 1
                    spear_list.remove(s)
                    if lives <= 0:
                        is_playing = False
                        last_score = current_time

            if perfect_popup_time and pygame.time.get_ticks() - perfect_popup_time < 700:
                screen.blit(small_font.render("PERFECT +5", True, "cyan"), (340, 90))

            if new_record and pygame.time.get_ticks() - record_time < 1200:
                screen.blit(game_font.render("NEW RECORD!", True, "yellow"), (300, 70))

            if current_time > high_score:
                high_score = current_time

    else:
        screen.blit(menu_background, (0,0))
        screen.blit(start_player, start_player_rect)
        screen.blit(title_text, title_rect)
        pygame.draw.rect(screen, "green", start_border, 3)
        screen.blit(start_text, start_rect)
        pygame.draw.rect(screen, "black", instructions_border)
        screen.blit(instructions_text, instructions_rect)
        screen.blit(game_font.render(f"High score: {high_score}", True, "white"), (300, 360))

        if show_instructions:
            screen.blit(instructions_surface, instructions_box)
            screen.blit(exit_text, exit_rect)
            screen.blit(title_font.render("Instructions", True, "white"),
                        (instructions_box.centerx - 90, instructions_box.top + 20))
            text_area = pygame.Rect(
                instructions_box.left + 40,
                instructions_box.top + 80,
                instructions_box.width - 80,
                instructions_box.height - 120
            )
            draw_wrapped_text(screen,
                "- Jump with SPACE or UP\n- Duck with DOWN\n- Press I once per run for immunity\n- Perfect jumps give bonus points",
                small_font, "white", text_area)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
