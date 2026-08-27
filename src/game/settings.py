import asyncio
import pygame
from os.path import join
from utils.file_importer import load_images, load_image_states, load_image

pygame.init()
screen = pygame.display.set_mode((2560, 1080))
pygame.display.set_caption("Vampire Survivor")

WINDOW_WIDTH, WINDOW_HEIGHT = screen.get_size()
TILE_SIZE = 48

# -------------------------------- ENEMIES -------------------------------- #

enemy_frames = {
    "bat": load_image_states("assets", "images", "enemies", "bat", scale=3),
    "skeleton": load_image_states("assets", "images", "enemies", "skeleton", scale=2)
}

boss_frames = {
    'walk': load_image_states("assets", "images", "enemies", "boss", "walk", scale=4),
    'attack': load_image_states("assets", "images", "enemies", "boss", "attack", scale=4)
}

# ---------------------------------- WEAPONS --------------------------------- #

pistol_frames = load_images("assets", "images", "weapons", "pistol", "shoot", scale=2.5)
machinegun_frames = load_images("assets", "images", "weapons", "machinegun", scale=3)
shotgun_frames = load_images("assets", "images", "weapons", "shotgun", scale=3)
rifle_frames = load_images("assets", "images", "weapons", "rifle", scale=3)
lasergun_frames = load_images("assets", "images", "weapons", "lasergun", "shoot", scale=1/6)
flamegun_frames = load_images("assets", "images", "weapons", "flamegun", "shoot", scale=2)

pistol_static = load_image("assets", "images", "weapons", "pistol", "pistol_static.png", scale=2.5)
machinegun_static = machinegun_frames[0]
rifle_static = rifle_frames[0]
shotgun_static = shotgun_frames[0]
lasergun_static = load_image("assets", "images", "weapons", "lasergun", "lasergun_static.png", scale=1/6)
flamegun_static = load_image("assets", "images", "weapons", "flamegun", "flamegun_static.png", scale=2)
sword_surf = load_image("assets", "images", "weapons", "sword.png", scale=1/6)

# ----------------------------------- PROJECTILES ---------------------------------- #

bullet_surf = load_image("assets", "images", "projectiles", "bullet.png", scale=1/4)
laser_bullet_surf = load_image("assets", "images", "projectiles", "laser_bullet.png", scale=1/4)
flame_bullet_surf = load_image("assets", "images", "projectiles", "flame_bullet.png", scale=1/4)
orb_surf = load_image("assets", "images", "projectiles", "orb.png", scale=1)
laser_surf = pygame.transform.scale(
    pygame.image.load(join("assets", "images", "projectiles", "laserbeam.png")), (WINDOW_WIDTH, 2)
).convert_alpha()

flame_frames = load_images("assets", "images", "flame", scale=0.5)
explosion_frames = load_images("assets", "images", "explosion")

# --------------------------------- POWERUPS --------------------------------- #

POWERUP_SURFS = {
    'life':load_image("assets", "images", "powerups", "life.png", scale=1/4),
    'rifle': rifle_static,
    'machinegun': machinegun_static,
    'laser': lasergun_static,
    'shotgun': shotgun_static,
    'sideshot': pistol_static,
    'sword': sword_surf,
    'superspeed': load_image("assets", "images", "powerups", "superspeed.png", scale=1/4),
    'shield': load_image("assets", "images", "powerups", "shield.png", scale=1/32),
    'slowaura': load_image("assets", "images", "powerups", "snail.png", scale=1/5),
    'timestop': load_image("assets", "images", "powerups", "clock.png", scale=1/12),
    "flamegun": flamegun_static,
    'mine': load_image("assets", "images", "powerups", "mine.png", scale=3/4)
}

aura_surf = load_image("assets", "images", "powerups", "aura.png", scale=1)
