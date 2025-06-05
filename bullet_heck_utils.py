### Constants and classes and such

import pygame
import math
import random

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 800, 600
PLAYER_SPEED = 5
PROJECTILE_SPEED = 3
REFLECTED_PROJECTILE_SPEED = 10
BOSS_HP = 10
PLAYER_HP = 5
PARRY_COOLDOWN = 2000

# Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 255, 0)
GREEN = (0, 0, 255)
CPLAYER = (0, 230, 230)
CPLAYERP = (0, 60, 60)
CPLAYERNP = (0, 160, 160)
CTURRET = (150, 0, 0)
CSPROJECTILE = (200, 0, 0)

# Create the game screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Create player
class Player:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.velocity_x = 0
        self.velocity_y = 0
        self.lastx = ""
        self.lasty = ""
        self.rect = pygame.Rect(self.x, self.y, 40, 40)
        self.parried_status = False    # Whether the player is currently parried
        self.off_cooldown = True       # Whether the player's parry is off cooldown
        self.last_parried_time = -PARRY_COOLDOWN     # The last time the player parried
        self.last_invulnerable_time = 0   # The last time the player became invulnerable from being hit
        self.hp = PLAYER_HP

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d] and not keys[pygame.K_a]:
            self.velocity_x = PLAYER_SPEED
            self.lastx = "right"
        elif keys[pygame.K_a] and not keys[pygame.K_d]:
            self.velocity_x = -PLAYER_SPEED
            self.lastx = "left"
        elif keys[pygame.K_d] and keys[pygame.K_a]:
            if self.lastx == "right":
                self.velocity_x = -PLAYER_SPEED
            else:
                self.velocity_x = PLAYER_SPEED
        else:
            self.velocity_x = 0

        if keys[pygame.K_s] and not keys[pygame.K_w]:
            self.velocity_y = PLAYER_SPEED
            self.lasty = "down"
        elif keys[pygame.K_w] and not keys[pygame.K_s]:
            self.velocity_y = -PLAYER_SPEED
            self.lasty = "up"
        elif keys[pygame.K_s] and keys[pygame.K_w]:
            if self.lasty == "down":
                self.velocity_y = -PLAYER_SPEED
            else:
                self.velocity_y = PLAYER_SPEED
        else:
            self.velocity_y = 0

        if self.velocity_x != 0 and self.velocity_y != 0:
            self.velocity_x *= 0.85  
            self.velocity_y *= 0.85 # 1 / sqrt(2)

        self.x += self.velocity_x
        self.y += self.velocity_y
        self.rect.x = self.x
        self.rect.y = self.y


    def draw(self):
        # Draw player square
        if self.parried_status:
            pygame.draw.rect(screen, CPLAYERP, self.rect)
        elif self.off_cooldown:
            pygame.draw.rect(screen, CPLAYER, self.rect)
        else:
            pygame.draw.rect(screen, CPLAYERNP, self.rect)

class Projectile:
    def __init__(self, x, y, target):
        self.x = x
        self.y = y
        self.target = target
        self.reflected = False # Whether the projectile's been reflected 
        self.rect = pygame.Rect(self.x, self.y, 20, 20)

    def move(self):
        target_x = self.target.rect.centerx if hasattr(self.target, 'rect') else self.target.x
        target_y = self.target.rect.centery if hasattr(self.target, 'rect') else self.target.y
        dx = target_x - self.rect.centerx
        dy = target_y - self.rect.centery
        angle = math.atan2(dy, dx)

        if self.reflected:
            self.x += math.cos(angle) * REFLECTED_PROJECTILE_SPEED
            self.y += math.sin(angle) * REFLECTED_PROJECTILE_SPEED
        else:
            self.x += math.cos(angle) * PROJECTILE_SPEED
            self.y += math.sin(angle) * PROJECTILE_SPEED
        self.rect.x = self.x
        self.rect.y = self.y

    def draw(self):
        dx = self.target.rect.centerx - self.rect.centerx
        dy = self.target.rect.centery - self.rect.centery

        # Horrific maths to rotate the triangle sprite to fit the hitbox
        angle = math.atan2(dy, dx)
        offset = abs((angle - math.pi/2)) / (math.pi/2)
        offset_angle = offset if offset < 2 else 4 - offset
        y_offset = 0.5 * -20 * offset_angle
        x_offset_factor = 2 - offset_angle if offset_angle > 1 else offset_angle
        if dx != 0:
            x_offset = ((y_offset / math.sqrt(2)) * (abs(dx)/dx)) * x_offset_factor
        else:
            x_offset = 0

        # Draw triangle
        points = [(self.rect.centerx + x_offset + math.cos(angle + math.pi / 2) * 10, self.rect.centery - 10 - y_offset + math.sin(angle + math.pi / 2) * 10),
                    (self.rect.centerx + x_offset + math.cos(angle) * 20, self.rect.centery - 10 - y_offset + math.sin(angle) * 20),
                    (self.rect.centerx + x_offset + math.cos(angle - math.pi / 2) * 10, self.rect.centery - 10 - y_offset + math.sin(angle - math.pi / 2) * 10)]
        pygame.draw.polygon(screen, RED, points)
        #pygame.draw.rect(screen, GREEN, self.rect, 1) # Hitbox

class Turret:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = 0
        self.hp = BOSS_HP
        self.rect = pygame.Rect(self.x, self.y, 50, 50)
        self.destroyed = False

    def draw(self):
        pygame.draw.rect(screen, CTURRET, self.rect)

class StageProjectile():
    def __init__(self):
        self.rect = pygame.Rect(random.randint(0, WIDTH - 10 * 2), 
                               random.randint(0, HEIGHT - 10 * 2), 
                               10 * 2, 10 * 2)
        self.velocity = pygame.math.Vector2(random.choice([-PROJECTILE_SPEED, PROJECTILE_SPEED]), 
                                            random.choice([-PROJECTILE_SPEED, PROJECTILE_SPEED]))

    def draw(self):
        pygame.draw.rect(screen, CSPROJECTILE, self.rect)

    def move(self):
        self.rect.move_ip(self.velocity)
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.velocity.x *= -1
        if self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.velocity.y *= -1 


def draw_screen(screen, player, turret, projectiles, stage_projectiles):
    # Draw everything
    screen.fill(WHITE)
    player.draw()
    turret.draw()
    for projectile in projectiles:
        projectile.draw()
    for s_projectile in stage_projectiles:
        s_projectile.draw()

    # Draw boss HP bar
    pygame.draw.rect(screen, RED, (0, HEIGHT - 20, WIDTH * turret.hp / BOSS_HP, 20))
    font = pygame.font.Font(None, 36)
    text = font.render("Boss HP", True, BLACK)
    screen.blit(text, (10, HEIGHT - 20))

    # Draw player HP bar
    pygame.draw.rect(screen, CPLAYER, (0, HEIGHT - 40, WIDTH * player.hp / PLAYER_HP, 20))
    font = pygame.font.Font(None, 36)
    text = font.render("Player HP", True, BLACK)
    screen.blit(text, (10, HEIGHT - 40))

def level_select():
    pass

def next_screen():
    pass