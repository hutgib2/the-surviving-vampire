import asyncio
import pygame
from os.path import join
from os import walk
from utils.file_importer import load_images, load_image_states

pygame.init()
screen = pygame.display.set_mode((2560, 1440))
pygame.display.set_caption("Vampire Survivor")

WINDOW_WIDTH, WINDOW_HEIGHT = screen.get_size()
TILE_SIZE = 64

# ----------------------------------- SURFS ---------------------------------- #

life_surf = pygame.transform.scale(
    pygame.image.load(join("assets", "images", "powerups", "life.png")), (75, 75)
).convert_alpha()
pierce_surf = pygame.transform.scale(
    pygame.image.load(join("assets", "images", "powerups", "pierce.png")), (75, 75)
).convert_alpha()
machinegun_surf = pygame.transform.scale(
    pygame.image.load(join("assets", "images", "powerups", "machinegun.png")), (125, 60)
).convert_alpha()
lasergun_surf = pygame.transform.scale(
    pygame.image.load(join("assets", "images", "powerups", "lasergun.png")), (100, 75)
).convert_alpha()
lasergun_surf = pygame.transform.flip(lasergun_surf, True, False)
laser_surf = pygame.transform.scale(
    pygame.image.load(join("assets", "images", "powerups", "laserbeam.png")),
    (WINDOW_WIDTH, 2),
).convert_alpha()
shotgun_surf = pygame.transform.scale(
    pygame.image.load(join("assets", "images", "powerups", "shotgun.png")), (150, 40)
).convert_alpha()
gun_surf = pygame.transform.scale(
    pygame.image.load(join("assets", "images", "gun", "gun.png")), (100, 54)
).convert_alpha()
sword_surf = pygame.transform.scale(
    pygame.image.load(join("assets", "images", "powerups", "sword.png")),
    (1490 / 6, 328 / 6),
).convert_alpha()
superspeed_surf = pygame.transform.scale(
    pygame.image.load(join("assets", "images", "powerups", "superspeed.png")), (81, 81)
).convert_alpha()
shield_surf = pygame.transform.scale(
    pygame.image.load(join("assets", "images", "powerups", "shield.png")), (81, 81)
).convert_alpha()
slow_surf = pygame.transform.scale(
    pygame.image.load(join("assets", "images", "powerups", "snail.png")), (96, 96)
).convert_alpha()
aura_surf = pygame.transform.scale(
    pygame.image.load(join("assets", "images", "powerups", "aura.png")), (800, 800)
).convert_alpha()
timestop_surf = pygame.transform.scale(
    pygame.image.load(join("assets", "images", "powerups", "clock.png")), (83, 99)
).convert_alpha()
flamegun_surf = pygame.transform.scale(
    pygame.image.load(join("assets", "images", "powerups", "flamegun.png")), (100, 75)
).convert_alpha()
mine_surf = pygame.transform.scale(
    pygame.image.load(join("assets", "images", "powerups", "mine.png")), (92, 42)
).convert_alpha()
bullet_surf = pygame.transform.scale(
    pygame.image.load(join("assets", "images", "gun", "bullet.png")), (25, 25)
).convert_alpha()
orb_surf = pygame.transform.scale(
    pygame.image.load(join("assets", "images", "enemies", "orb.png")), (52, 52)
).convert_alpha()

POWERUP_SURFS = {
    # 'life':life_surf,
    # 'pierce':pierce_surf,
    # 'machinegun':machinegun_surf,
    # 'laser':lasergun_surf,
    # 'shotgun':shotgun_surf,
    # 'sideshot':gun_surf,
    # 'sword':sword_surf,
    # 'superspeed':superspeed_surf,
    # 'shield':shield_surf,
    # 'slowaura': slow_surf,
    # 'timestop': timestop_surf,
    "flamegun": flamegun_surf,
    # 'mine': mine_surf
}

enemy_frames = {
    "bat": load_image_states("assets", "images", "enemies", "bat", scale=3)
    # 'skeleton': load_image_states('assets', 'images', 'skeleton'),
}

flame_frames = load_images("assets", "images", "powerups", "flame", scale=0.75)
explosion_frames = load_images("assets", "images", "powerups", "explosion")
