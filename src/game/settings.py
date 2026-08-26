import asyncio
import pygame
from os.path import join
from utils.file_importer import load_images, load_image_states, load_image

pygame.init()
screen = pygame.display.set_mode((2560, 1080))
pygame.display.set_caption("Vampire Survivor")

WINDOW_WIDTH, WINDOW_HEIGHT = screen.get_size()
TILE_SIZE = 48

# ----------------------------------- SURFS ---------------------------------- #

life_surf = load_image("assets", "images", "powerups", "life.png", scale=1/4)

machinegun_surf = load_image("assets", "images", "machinegun", "0.png", scale=3)

rifle_surf = load_image("assets", "images", "rifle", "0.png", scale=3)

lasergun_surf = load_image("assets", "images", "powerups", "lasergun.png", scale=1/6)

laser_surf = pygame.transform.scale(
    pygame.image.load(join("assets", "images", "powerups", "laserbeam.png")), (WINDOW_WIDTH, 2),
).convert_alpha()

shotgun_surf = load_image("assets", "images", "shotgun", "0.png", scale=3)

gun_surf = load_image("assets", "images", "gun", "gun.png", scale=2.5)

sword_surf = load_image("assets", "images", "powerups", "sword.png", scale=1/6)

superspeed_surf = load_image("assets", "images", "powerups", "superspeed.png", scale=1/4)

shield_surf = load_image("assets", "images", "powerups", "shield.png", scale=1/32)

slow_surf = load_image("assets", "images", "powerups", "snail.png", scale=1/5)

aura_surf = load_image("assets", "images", "powerups", "aura.png", scale=1)

timestop_surf = load_image("assets", "images", "powerups", "clock.png", scale=1/12)

flamegun_surf = load_image("assets", "images", "powerups", "flamegun.png", scale=1/4)

mine_surf = load_image("assets", "images", "powerups", "mine.png", scale=3/4)

bullet_surf = load_image("assets", "images", "gun", "bullet.png", scale=1/4)

laser_bullet_surf = load_image("assets", "images", "gun", "laser_bullet.png", scale=1/4)

flame_bullet_surf = load_image("assets", "images", "gun", "flame_bullet.png", scale=1/4)

orb_surf = load_image("assets", "images", "enemies", "orb.png", scale=1.5)

POWERUP_SURFS = {
    'life':life_surf,
    'rifle':rifle_surf,
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

# -------------------------------- ANIMATIONS -------------------------------- #

enemy_frames = {
    "bat": load_image_states("assets", "images", "enemies", "bat", scale=3),
    "skeleton": load_image_states("assets", "images", "enemies", "skeleton", scale=2)
}

boss_frames = {
    'walk': load_image_states("assets", "images", "boss", "walk", scale=4),
    'attack': load_image_states("assets", "images", "boss", "attack", scale=4)
}

flame_frames = load_images("assets", "images", "powerups", "flame", scale=0.75)
explosion_frames = load_images("assets", "images", "powerups", "explosion")
pistol_frames = load_images("assets", "images", "gun", "shoot", scale=2.5)
machinegun_frames = load_images("assets", "images", "machinegun", scale=3)
shotgun_frames = load_images("assets", "images", "shotgun", scale=3)
rifle_frames = load_images("assets", "images", "rifle", scale=3)
lasergun_frames = load_images("assets", "images", "laser_shoot", scale=1/6)