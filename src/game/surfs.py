from utils.file_importer import load_images, load_image_states, load_image, scale_image
from game.settings import *
from os.path import join

# ---------------------------------- PLAYER ---------------------------------- #

PLAYER_FRAMES = {
    "idle": load_image_states("assets", "images", "vampire", "idle", scale=3),
    "walk": load_image_states("assets", "images", "vampire", "walk", scale=3),
    "hurt": load_image_states("assets", "images", "vampire", "hurt", scale=3),
    "dead": load_image_states("assets", "images", "vampire", "dead", scale=3),
    "fly": load_image_states("assets", "images", "vampire", "fly", scale=3),
    "ultimate_move": load_image_states("assets", "images", "vampire", "ultimate_move", scale=3)
}

# -------------------------------- ENEMIES -------------------------------- #

ENEMY_FRAMES = {
    "bat": {
        'walk': load_image_states("assets", "images", "enemies", "bat", 'walk', scale=5/2),
        'dead': load_image_states("assets", "images", "enemies", "bat", 'dead', scale=5/2),
    },
    "skeleton": {
        'walk': load_image_states("assets", "images", "enemies", "skeleton", "walk", scale=3/2),
        'dead': load_image_states("assets", "images", "enemies", "skeleton", "dead", scale=3/2),
    } 
}

BOSS_FRAMES = {
    'walk': load_image_states("assets", "images", "enemies", "boss", "walk", scale=4),
    'attack': load_image_states("assets", "images", "enemies", "boss", "attack", scale=4)
}

# ---------------------------------- WEAPONS --------------------------------- #

WEAPON_FRAMES = {
    'pistol': load_images("assets", "images", "weapons", "pistol", "shoot", scale=2),
    'machinegun': load_images("assets", "images", "weapons", "machinegun", scale=2.5),
    'shotgun': load_images("assets", "images", "weapons", "shotgun", scale=2.5),
    'rifle': load_images("assets", "images", "weapons", "rifle", scale=2.5),
    'lasergun': load_images("assets", "images", "weapons", "lasergun", "shoot", scale=1/8),
    'flamegun': load_images("assets", "images", "weapons", "flamegun", "shoot", scale=2)
}

pistol_surf = load_image("assets", "images", "weapons", "pistol", "pistol_static.png", scale=2)

WEAPON_SURFS = {
    'pistol': pistol_surf,
    'sideshot': pistol_surf,
    'machinegun': WEAPON_FRAMES['machinegun'][0],
    'shotgun': WEAPON_FRAMES['shotgun'][0],
    'rifle': WEAPON_FRAMES['rifle'][0],
    'lasergun': load_image("assets", "images", "weapons", "lasergun", "lasergun_static.png", scale=1/8),
    'flamegun': load_image("assets", "images", "weapons", "flamegun", "flamegun_static.png", scale=2),
    'sword': load_image("assets", "images", "weapons", "sword.png", scale=1/6),
}

# ----------------------------------- PROJECTILES ---------------------------------- #

BULLET_SURF = load_image("assets", "images", "projectiles", "bullet.png", scale=1/5)
LASER_BULLET_SURF = load_image("assets", "images", "projectiles", "laser_bullet.png", scale=1/5)
FLAME_BULLET_SURF = load_image("assets", "images", "projectiles", "flame_bullet.png", scale=1/5)

ORB_SURF = load_image("assets", "images", "projectiles", "orb.png", scale=1.5)
LASER_SURF = pygame.transform.scale(pygame.image.load(join("assets", "images", "projectiles", "laserbeam.png")), (WINDOW_WIDTH, 3)).convert_alpha()

FLAME_FRAMES = load_images("assets", "images", "flame", scale=1/3)
EXPLOSION_FRAMES = load_images("assets", "images", "explosion")

# --------------------------------- POWERUPS --------------------------------- #

LIFE_SURF = load_image("assets", "images", "powerups", "life.png", scale=1/5)
AURA_SURF = load_image("assets", "images", "powerups", "aura.png", scale=2)
AURA_SURF.set_alpha(50)

POWERUP_SURFS = {
    'rifle': WEAPON_SURFS['rifle'],
    'machinegun': WEAPON_SURFS['machinegun'],
    'lasergun': WEAPON_SURFS['lasergun'],
    'shotgun': WEAPON_SURFS['shotgun'],
    'sideshot': WEAPON_SURFS['pistol'],
    'sword': scale_image(WEAPON_SURFS['sword'], 0.5),
    "flamegun": WEAPON_SURFS['flamegun'],
    'life': LIFE_SURF,
    'superspeed': load_image("assets", "images", "powerups", "superspeed.png", scale=1/5),
    'shield': load_image("assets", "images", "powerups", "shield.png", scale=1/40),
    'slowaura': load_image("assets", "images", "powerups", "snail.png", scale=1/7),
    'timestop': load_image("assets", "images", "powerups", "clock.png", scale=1/16),
    'mine': load_image("assets", "images", "powerups", "mine.png", scale=2/3)
}

# ----------------------------------- MENU ----------------------------------- #

BUTTON_SURF = load_image("assets", "images", "menu", "button.png")
ULTIMATE_MOVE_PROGRESS_FRAMES = load_images("assets", "images", "ultimate_progress", scale=4)