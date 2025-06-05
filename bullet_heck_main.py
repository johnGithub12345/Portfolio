# main.py
import pygame
import random
from bullet_heck_entities import Player, Projectile, Turret, StageProjectile
from bullet_heck_game_utils import draw_hud, show_title_screen, show_level_select, show_game_over_screen
from bullet_heck_config import *

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

def initialize_level(level):
    player = Player()
    level_config = LEVEL_CONFIG[level]
    
    turrets = []
    if level_config.get("dual_boss", False):
        turrets.append(Turret(WIDTH//4, 0, level_config["boss_hp"]))
        turrets.append(Turret(3*WIDTH//4, 0, level_config["boss_hp"]))
    else:
        turrets.append(Turret(WIDTH//2, 0, level_config["boss_hp"]))

    stage_projectiles = [
        StageProjectile(level_config["stage_projectile_speed"])
        for _ in range(level_config["stage_projectiles"])
    ]
    
    return player, turrets, stage_projectiles, level_config

def main():
    running = True
    
    while running:
        # Show title screen
        if not show_title_screen(screen):
            break

        # Level select
        current_level = show_level_select(screen)
        if current_level is None:
            break

        # Initialize game state
        player, turrets, stage_projectiles, level_config = initialize_level(current_level)
        projectiles = []
        projectile_times = [0] * len(turrets)  
        game_active = True

        while game_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    if pygame.time.get_ticks() - player.last_parried_time > PARRY_COOLDOWN:
                        player.parried_status = True
                        player.off_cooldown = False
                        player.last_parried_time = pygame.time.get_ticks()

            # Update player state
            player.move()
            if pygame.time.get_ticks() - player.last_parried_time > 500:
                player.parried_status = False
            if pygame.time.get_ticks() - player.last_parried_time > PARRY_COOLDOWN:
                player.off_cooldown = True

            # Turret firing with staggered timing
            fire_rate = level_config["turret_fire_rate"]
            for i, turret in enumerate(turrets):
                # Calculate offset for each turret (evenly spaced)
                offset = (fire_rate / len(turrets)) * i
                current_time = pygame.time.get_ticks()
                if (not turret.destroyed and 
                    current_time - projectile_times[i] > fire_rate and
                    (current_time % fire_rate) >= offset and 
                    (current_time % fire_rate) < offset + 100):  # 100ms window for firing
                    projectiles.append(Projectile(turret.x, turret.y, player, level_config["projectile_speed"]))
                    projectile_times[i] = current_time

            # Update projectiles
            for projectile in projectiles[:]:
                projectile.move()
                if player.rect.colliderect(projectile.rect):
                    if player.parried_status:
                        projectile.reflected = True
                        projectile.target = random.choice([t for t in turrets if not t.destroyed])
                        stage_projectiles.append(StageProjectile(level_config["stage_projectile_speed"]))
                        player.last_invulnerable_time = pygame.time.get_ticks()
                    elif pygame.time.get_ticks() - player.last_invulnerable_time > 500:
                        player.hp -= 1
                        projectiles.remove(projectile)
                        if player.hp <= 0:
                            game_active = False
                    else:
                        projectiles.remove(projectile)
                elif projectile.reflected:
                    for turret in turrets:
                        if turret.rect.colliderect(projectile.rect):
                            turret.hp -= 1
                            projectiles.remove(projectile)
                            if turret.hp <= 0:
                                turret.destroyed = True

            # Update stage projectiles
            for s_projectile in stage_projectiles[:]:
                s_projectile.move()
                if (player.rect.colliderect(s_projectile.rect) and 
                    pygame.time.get_ticks() > 2000 and
                    pygame.time.get_ticks() - player.last_invulnerable_time > 500):
                    player.hp -= 1
                    stage_projectiles.remove(s_projectile)
                    if player.hp <= 0:
                        game_active = False

            # Check win/lose condition
            if all(t.destroyed for t in turrets) or player.hp <= 0:
                game_active = False
                won = all(t.destroyed for t in turrets)

            # Draw everything
            screen.fill(WHITE)
            player.draw(screen)
            for turret in turrets:
                turret.draw(screen)
            for projectile in projectiles:
                projectile.draw(screen)
            for s_projectile in stage_projectiles:
                s_projectile.draw(screen)
            draw_hud(screen, player, turrets, current_level)
            pygame.display.flip()
            clock.tick(60)

        # Show game over screen and return to level select
        if not show_game_over_screen(screen, won):
            break

    pygame.quit()

if __name__ == "__main__":
    main()