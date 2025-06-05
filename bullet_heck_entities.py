# entities.py
import pygame
import math
import random
from bullet_heck_config import *

class Player:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.velocity_x = 0
        self.velocity_y = 0
        self.lastx = ""
        self.lasty = ""
        self.rect = pygame.Rect(self.x, self.y, 40, 40)
        self.parried_status = False
        self.off_cooldown = True
        self.last_parried_time = -PARRY_COOLDOWN
        self.last_invulnerable_time = 0
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
            self.velocity_x *= 0.707  
            self.velocity_y *= 0.707 # 1 / sqrt(2)

        self.x += self.velocity_x
        self.y += self.velocity_y
        self.rect.x = self.x
        self.rect.y = self.y
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

    def draw(self, screen):
        colour = CPLAYER if self.off_cooldown else CPLAYERNP
        if self.parried_status:
            colour = CPLAYERP
        pygame.draw.rect(screen, colour, self.rect)

class Projectile:
    def __init__(self, x, y, target, speed=PROJECTILE_SPEED):
        self.x = x
        self.y = y
        self.target = target
        self.reflected = False
        self.rect = pygame.Rect(self.x, self.y, 20, 20)
        self.speed = speed

    def move(self):
        target_x = self.target.rect.centerx if hasattr(self.target, 'rect') else self.target.x
        target_y = self.target.rect.centery if hasattr(self.target, 'rect') else self.target.y
        dx = target_x - self.rect.centerx
        dy = target_y - self.rect.centery
        angle = math.atan2(dy, dx)
        speed = REFLECTED_PROJECTILE_SPEED if self.reflected else self.speed
        self.x += math.cos(angle) * speed
        self.y += math.sin(angle) * speed
        self.rect.x = self.x
        self.rect.y = self.y

    def draw(self, screen):
        dx = self.target.rect.centerx - self.rect.centerx
        dy = self.target.rect.centery - self.rect.centery
        angle = math.atan2(dy, dx)
        offset = abs((angle - math.pi/2)) / (math.pi/2)
        offset_angle = offset if offset < 2 else 4 - offset
        y_offset = 0.5 * -20 * offset_angle
        x_offset_factor = 2 - offset_angle if offset_angle > 1 else offset_angle
        x_offset = ((y_offset / math.sqrt(2)) * (abs(dx)/dx)) * x_offset_factor if dx != 0 else 0

        points = [
            (self.rect.centerx + x_offset + math.cos(angle + math.pi/2) * 10,
             self.rect.centery - 10 - y_offset + math.sin(angle + math.pi/2) * 10),
            (self.rect.centerx + x_offset + math.cos(angle) * 20,
             self.rect.centery - 10 - y_offset + math.sin(angle) * 20),
            (self.rect.centerx + x_offset + math.cos(angle - math.pi/2) * 10,
             self.rect.centery - 10 - y_offset + math.sin(angle - math.pi/2) * 10)
        ]
        pygame.draw.polygon(screen, RED, points)

class Turret:
    def __init__(self, x, y, hp):
        self.x = x
        self.y = y
        self.hp = hp
        self.rect = pygame.Rect(self.x, self.y, 50, 50)
        self.destroyed = False

    def draw(self, screen):
        pygame.draw.rect(screen, CTURRET, self.rect)

class StageProjectile:
    def __init__(self, speed):
        self.rect = pygame.Rect(random.randint(0, WIDTH - 20), 
                              random.randint(0, HEIGHT - 20), 
                              20, 20)
        self.velocity = pygame.math.Vector2(
            random.choice([-speed, speed]),
            random.choice([-speed, speed])
        )

    def move(self):
        self.rect.move_ip(self.velocity)
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.velocity.x *= -1
        if self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.velocity.y *= -1

    def draw(self, screen):
        pygame.draw.rect(screen, CSPROJECTILE, self.rect)