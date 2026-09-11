import asyncio
import pygame
from os.path import join
from utils.file_importer import load_images, load_image_states, load_image

pygame.init()
screen = pygame.display.set_mode((1280 * 1.8, 720 * 1.8))
pygame.display.set_caption("Vampire Survivor")

WINDOW_WIDTH, WINDOW_HEIGHT = screen.get_size()
TILE_SIZE = 48

# ---------------------------------- PLAYER ---------------------------------- #

player_frames = {
    "idle": load_image_states("assets", "images", "vampire", "idle", scale=3),
    "walk": load_image_states("assets", "images", "vampire", "walk", scale=3),
    "hurt": load_image_states("assets", "images", "vampire", "hurt", scale=3),
    "dead": load_image_states("assets", "images", "vampire", "dead", scale=3),
    "fly": load_image_states("assets", "images", "vampire", "fly", scale=3),
    "ultimate_move": load_image_states("assets", "images", "vampire", "ultimate_move", scale=3)
}

# -------------------------------- ENEMIES -------------------------------- #

enemy_frames = {
    "bat": {
        'walk': load_image_states("assets", "images", "enemies", "bat", 'walk', scale=5/2),
        'dead': load_image_states("assets", "images", "enemies", "bat", 'dead', scale=5/2),
    },
    "skeleton": {
        'walk': load_image_states("assets", "images", "enemies", "skeleton", "walk", scale=3/2),
        'dead': load_image_states("assets", "images", "enemies", "skeleton", "dead", scale=3/2),
    } 
}

boss_frames = {
    'walk': load_image_states("assets", "images", "enemies", "boss", "walk", scale=4),
    'attack': load_image_states("assets", "images", "enemies", "boss", "attack", scale=4)
}

# ---------------------------------- WEAPONS --------------------------------- #

pistol_frames = load_images("assets", "images", "weapons", "pistol", "shoot", scale=2)
machinegun_frames = load_images("assets", "images", "weapons", "machinegun", scale=2.5)
shotgun_frames = load_images("assets", "images", "weapons", "shotgun", scale=2.5)
rifle_frames = load_images("assets", "images", "weapons", "rifle", scale=2.5)
lasergun_frames = load_images("assets", "images", "weapons", "lasergun", "shoot", scale=1/8)
flamegun_frames = load_images("assets", "images", "weapons", "flamegun", "shoot", scale=2)

pistol_static = load_image("assets", "images", "weapons", "pistol", "pistol_static.png", scale=2)
machinegun_static = machinegun_frames[0]
shotgun_static = shotgun_frames[0]
rifle_static = rifle_frames[0]
lasergun_static = load_image("assets", "images", "weapons", "lasergun", "lasergun_static.png", scale=1/8)
flamegun_static = load_image("assets", "images", "weapons", "flamegun", "flamegun_static.png", scale=2)
sword_surf = load_image("assets", "images", "weapons", "sword.png", scale=1/8)

# ----------------------------------- PROJECTILES ---------------------------------- #

bullet_surf = load_image("assets", "images", "projectiles", "bullet.png", scale=1/5)
laser_bullet_surf = load_image("assets", "images", "projectiles", "laser_bullet.png", scale=1/5)
flame_bullet_surf = load_image("assets", "images", "projectiles", "flame_bullet.png", scale=1/5)
orb_surf = load_image("assets", "images", "projectiles", "orb.png", scale=1.5)
laser_surf = pygame.transform.scale(pygame.image.load(join("assets", "images", "projectiles", "laserbeam.png")), (WINDOW_WIDTH, 3)).convert_alpha()

flame_frames = load_images("assets", "images", "flame", scale=1/3)
explosion_frames = load_images("assets", "images", "explosion")

# --------------------------------- POWERUPS --------------------------------- #

ultimate_progress_frames = load_images("assets", "images", "ultimate_progress", scale=4)
life_surf = load_image("assets", "images", "powerups", "life.png", scale=1/5)
aura_surf = load_image("assets", "images", "powerups", "aura.png", scale=2)
aura_surf.set_alpha(50)

POWERUP_SURFS = {
    'rifle': rifle_static,
    'machinegun': machinegun_static,
    'laser': lasergun_static,
    'shotgun': shotgun_static,
    'sideshot': pistol_static,
    'sword': sword_surf,
    'life': life_surf,
    'superspeed': load_image("assets", "images", "powerups", "superspeed.png", scale=1/5),
    'shield': load_image("assets", "images", "powerups", "shield.png", scale=1/40),
    'slowaura': load_image("assets", "images", "powerups", "snail.png", scale=1/7),
    'timestop': load_image("assets", "images", "powerups", "clock.png", scale=1/16),
    "flamegun": flamegun_static,
    'mine': load_image("assets", "images", "powerups", "mine.png", scale=2/3)
}

# ----------------------------------- MENU ----------------------------------- #
button_surf = load_image("assets", "images", "menu", "button.png")