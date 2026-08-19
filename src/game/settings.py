import asyncio
import pygame
from os.path import join
from os import walk
from utils.file_importer import load_images, load_image_states, load_image

pygame.init()
screen = pygame.display.set_mode((2560, 1440))
pygame.display.set_caption("Vampire Survivor")

WINDOW_WIDTH, WINDOW_HEIGHT = screen.get_size()
TILE_SIZE = 64

# ----------------------------------- SURFS ---------------------------------- #

life_surf = load_image("assets", "images", "powerups", "life.png", scale=1/4)

pierce_surf = load_image("assets", "images", "powerups", "pierce.png", scale=1)

machinegun_surf = load_image("assets", "images", "powerups", "machinegun.png", scale=1/4)

lasergun_surf = load_image("assets", "images", "powerups", "lasergun.png", scale=1/4)

lasergun_surf = pygame.transform.flip(lasergun_surf, True, False)

laser_surf = pygame.transform.scale(
    pygame.image.load(join("assets", "images", "powerups", "laserbeam.png")), (WINDOW_WIDTH, 2),
).convert_alpha()

shotgun_surf = load_image("assets", "images", "powerups", "shotgun.png", scale=1/5)

gun_surf = load_image("assets", "images", "gun", "gun.png", scale=2.5)

sword_surf = load_image("assets", "images", "powerups", "sword.png", scale=1/6)

superspeed_surf = load_image("assets", "images", "powerups", "superspeed.png", scale=1/4)

shield_surf = load_image("assets", "images", "powerups", "shield.png", scale=1/16)

slow_surf = load_image("assets", "images", "powerups", "snail.png", scale=1/5)

aura_surf = load_image("assets", "images", "powerups", "aura.png", scale=1)

timestop_surf = load_image("assets", "images", "powerups", "clock.png", scale=1/10)

flamegun_surf = load_image("assets", "images", "powerups", "flamegun.png", scale=1/4)

mine_surf = load_image("assets", "images", "powerups", "mine.png", scale=1)

bullet_surf = load_image("assets", "images", "gun", "bullet.png", scale=1/4)

orb_surf = pygame.transform.scale(
    pygame.image.load(join("assets", "images", "enemies", "orb.png")), (52, 52)
).convert_alpha()

POWERUP_SURFS = {
    'life':life_surf,
    'pierce':pierce_surf,
    'machinegun':machinegun_surf,
    'laser':lasergun_surf,
    'shotgun':shotgun_surf,
    'sideshot':gun_surf,
    'sword':sword_surf,
    'superspeed':superspeed_surf,
    'shield':shield_surf,
    'slowaura': slow_surf,
    'timestop': timestop_surf,
    "flamegun": flamegun_surf,
    'mine': mine_surf
}

enemy_frames = {
    "bat": load_image_states("assets", "images", "enemies", "bat", scale=3),
    "skeleton": load_image_states("assets", "images", "enemies", "skeleton", scale=2)
}

flame_frames = load_images("assets", "images", "powerups", "flame", scale=0.75)
explosion_frames = load_images("assets", "images", "powerups", "explosion")
