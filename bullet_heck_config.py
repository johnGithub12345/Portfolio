# config.py
WIDTH, HEIGHT = 800, 600
PLAYER_SPEED = 5
PROJECTILE_SPEED = 3
REFLECTED_PROJECTILE_SPEED = 10
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

# Level configurations
LEVEL_CONFIG = {
    1: {
        "boss_hp": 5,
        "stage_projectiles": 4,
        "turret_fire_rate": 4000,
        "projectile_speed": 2,
        "stage_projectile_speed": 2
    },
    2: {
        "boss_hp": 10,
        "stage_projectiles": 8,
        "turret_fire_rate": 3000,
        "projectile_speed": 3,
        "stage_projectile_speed": 3
    },
    3: {
        "boss_hp": 10, 
        "stage_projectiles": 12,
        "turret_fire_rate": 2000,
        "projectile_speed": 4,
        "stage_projectile_speed": 4,
        "dual_boss": True
    }
}