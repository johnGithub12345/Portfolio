# game_utils.py
import pygame
from bullet_heck_config import *

def draw_hud(screen, player, turrets, level):
    y_offset = HEIGHT - 20
    for i, turret in enumerate(turrets):
        if not turret.destroyed:
            max_hp = LEVEL_CONFIG[level]["boss_hp"]
            pygame.draw.rect(screen, RED, (0, y_offset, WIDTH * turret.hp / max_hp, 20))
            font = pygame.font.Font(None, 36)
            text = font.render(f"Boss {i+1} HP", True, BLACK)
            screen.blit(text, (10, y_offset))
            y_offset -= 20

    pygame.draw.rect(screen, CPLAYER, (0, HEIGHT - 40 - len(turrets) * 20, 
                                     WIDTH * player.hp / PLAYER_HP, 20))
    font = pygame.font.Font(None, 36)
    text = font.render("Player HP", True, BLACK)
    screen.blit(text, (10, HEIGHT - 40 - len(turrets) * 20))

    font = pygame.font.Font(None, 36)
    text = font.render(f"Level {level}", True, BLACK)
    screen.blit(text, (WIDTH - 100, 10))

def show_title_screen(screen):
    font = pygame.font.Font(None, 74)
    title_text = font.render("Bullet Heck", True, BLACK)
    
    screen.fill(WHITE)
    screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, HEIGHT//2 - 50))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False
    return True

def show_level_select(screen):
    font = pygame.font.Font(None, 74)
    title_text = font.render("Select Level", True, BLACK)
    level_texts = [
        pygame.font.Font(None, 36).render(f"Level {i}", True, BLACK)
        for i in range(1, len(LEVEL_CONFIG) + 1)
    ]
    
    screen.fill(WHITE)
    screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, HEIGHT//4))
    for i, text in enumerate(level_texts):
        screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 + i * 50))
    pygame.display.flip()

    waiting = True
    selected_level = 1
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_level = max(1, selected_level - 1)
                elif event.key == pygame.K_DOWN:
                    selected_level = min(len(LEVEL_CONFIG), selected_level + 1)
                elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    return selected_level
                
        # Redraw screen with selection highlight
        level_texts = [
        pygame.font.Font(None, 36).render(f"Level {i}", True, BLACK)
        for i in range(1, len(LEVEL_CONFIG) + 1)
        ]
        level_texts[selected_level-1] = pygame.font.Font(None, 36).render(f"Level {selected_level}", True, RED)

        screen.fill(WHITE)
        screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, HEIGHT//4))
        for i, text in enumerate(level_texts):
            screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 + i * 50))
        pygame.display.flip()
    return selected_level

def show_game_over_screen(screen, won=False):
    font = pygame.font.Font(None, 74)
    result_text = font.render("You Win!" if won else "Game Over", True, BLACK)
    
    screen.fill(WHITE)
    screen.blit(result_text, (WIDTH//2 - result_text.get_width()//2, HEIGHT//2 - 50))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False
    return True