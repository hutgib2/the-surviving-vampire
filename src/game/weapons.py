from game.settings import *
from game.projectiles import Bullet, Laser, Orb, Flame
from game.enemies import Boss
from utils.timer import Timer
from math import atan2, degrees
from game.surfs import (
    WEAPON_FRAMES,
    LASER_SURF, 
    BULLET_SURF, 
    FLAME_BULLET_SURF, 
    LASER_BULLET_SURF, 
    FLAME_FRAMES,
)
from game.audio import (
    SHOTGUN_SOUND,
    PISTOL_SOUND, 
    MACHINEGUN_SOUND, 
    LASER_SOUND, 
    IMPACT_SOUND, 
    FLAMEGUN_SOUND, 
    RIFLE_SOUND, 
    STAB_SOUND,
)

class Pistol(pygame.sprite.Sprite):
    def __init__(self, surf, player, groups, game):
        super().__init__(groups)
        self.player = player
        self.distance = 80
        self.game = game
        self.player_direction = pygame.Vector2(1, -1)
        
        self.static_frame = surf
        self.image = self.static_frame # what we display after rotation
        self.current_image = self.image # what we set the image to be depending on whether animation is running
        self.rect = self.image.get_frect(center = self.player.rect.center + self.player_direction * self.distance)
        
        self.can_shoot = False
        self.shoot_cooldown = 300
        self.shoot_timer = Timer(self.shoot_cooldown, self.allow_shoot, repeat=True, autostart=True)
        self.shoot_sound = PISTOL_SOUND
        self.impact_sound = IMPACT_SOUND
        
        self.frame_index = 0
        self.animation_frames = WEAPON_FRAMES['pistol']
        self.animation_speed = self.shoot_cooldown / 7.5
        self.animation_running = False

    def allow_shoot(self):
        self.can_shoot = True

    def run_animation(self, frames, dt):
        self.frame_index += self.animation_speed * dt

        # when animation finishes, reset for next time
        if int(self.frame_index) >= len(frames):
            self.animation_running = False
            self.frame_index = 0
            return
        
        self.current_image = frames[int(self.frame_index)]
        
    def animate(self, dt):
        if self.animation_running:
            self.run_animation(self.animation_frames, dt)
        else:
            self.current_image = self.static_frame

    def get_direction(self):
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        player_pos = pygame.Vector2(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        if mouse_pos - player_pos != 0:
            self.player_direction = (mouse_pos - player_pos).normalize()
        else:
            self.player_direction = 0
    
    def rotate(self):
        angle = degrees(atan2(self.player_direction.x, self.player_direction.y)) - 90
        if self.player_direction.x > 0:
            self.image = pygame.transform.rotozoom(self.current_image, angle, 1)
        else:
            self.image = pygame.transform.rotozoom(self.current_image, abs(angle), 1)
            self.image = pygame.transform.flip(self.image, False, True)

    def create_bullet(self):
        pos = self.rect.center + self.player_direction * 50
        Bullet(BULLET_SURF, pos, self.player_direction, (self.game.all_sprites, self.game.bullet_sprites))

    def shoot(self):
        if pygame.mouse.get_pressed()[0] and self.can_shoot:
            self.animation_running = True
            self.shoot_sound.play()
            self.create_bullet()
            self.can_shoot = False
    
    def bullet_collision(self):
        collision_sprites = pygame.sprite.groupcollide(self.game.bullet_sprites, self.game.enemy_sprites, False, False, pygame.sprite.collide_mask)
        for bullet, enemies in collision_sprites.items():
            for enemy in enemies:
                if type(enemy) == Orb:
                    continue
                self.impact_sound.play()
                self.bullet_impact(bullet, enemy)
                if type(enemy) == Boss:
                    enemy.lives -= 1
                    if enemy.lives > 0:
                        continue
                enemy.destroy()
                self.game.kill_count += 1

    # Used for Polymorphism to reduce duplication
    def bullet_impact(self, bullet, enemy):
        bullet.kill()

    def update(self, dt):
        self.animate(dt)
        self.get_direction()
        self.rotate()
        self.rect.center = self.player.rect.center + (self.player_direction + pygame.Vector2(0, -0.2)) * self.distance
        self.shoot_timer.update()
        self.shoot()
        self.bullet_collision()

class Rifle(Pistol):
    def __init__(self, surf, player, groups, game):
        super().__init__(surf, player, groups, game)
        self.animation_frames = WEAPON_FRAMES['rifle']
        self.animation_speed = self.shoot_cooldown / 4
        self.shoot_sound = RIFLE_SOUND

    def bullet_impact(self, bullet, enemy):
        if type(enemy) == Boss:
            bullet.kill()

class Shotgun(Pistol):
    def __init__(self, surf, player, groups, game):
        super().__init__(surf, player, groups, game)
        self.animation_frames = WEAPON_FRAMES['shotgun']
        self.shoot_sound = SHOTGUN_SOUND
        self.shoot_cooldown = 500
        self.shoot_timer = Timer(self.shoot_cooldown, self.allow_shoot, repeat=True, autostart=True)

    def create_bullet(self):
        pos = self.rect.center + self.player_direction * 64
        Bullet(BULLET_SURF, pos, self.player_direction, (self.game.all_sprites, self.game.bullet_sprites))
        Bullet(BULLET_SURF, pos, self.player_direction.rotate(15), (self.game.all_sprites, self.game.bullet_sprites))
        Bullet(BULLET_SURF, pos, self.player_direction.rotate(-15), (self.game.all_sprites, self.game.bullet_sprites))
        Bullet(BULLET_SURF, pos, self.player_direction.rotate(30), (self.game.all_sprites, self.game.bullet_sprites))
        Bullet(BULLET_SURF, pos, self.player_direction.rotate(-30), (self.game.all_sprites, self.game.bullet_sprites))

class Sideshotgun(Pistol):
    def create_bullet(self):
        pos = self.rect.center + self.player_direction * 64
        Bullet(BULLET_SURF, pos, self.player_direction, (self.game.all_sprites, self.game.bullet_sprites))
        Bullet(BULLET_SURF, pos, self.player_direction.rotate(90), (self.game.all_sprites, self.game.bullet_sprites))
        Bullet(BULLET_SURF, pos, self.player_direction.rotate(-90), (self.game.all_sprites, self.game.bullet_sprites))
        Bullet(BULLET_SURF, pos, self.player_direction.rotate(180), (self.game.all_sprites, self.game.bullet_sprites))

class Machinegun(Pistol):
    def __init__(self, surf, player, groups, game):
        super().__init__(surf, player, groups, game)
        self.animation_frames = WEAPON_FRAMES['machinegun']
        self.shoot_sound = MACHINEGUN_SOUND
        self.shoot_cooldown = 100
        self.shoot_timer = Timer(self.shoot_cooldown, self.allow_shoot, repeat=True, autostart=True)

class Lasergun(Pistol):
    def __init__(self, surf, player, groups, game):
        super().__init__(surf, player, groups, game)
        self.animation_frames = WEAPON_FRAMES['lasergun']
        self.shoot_sound = LASER_SOUND
        self.impact_sound = LASER_SOUND

    def create_bullet(self):
        pos = self.rect.center + self.player_direction * 50
        Bullet(LASER_BULLET_SURF, pos, self.player_direction, (self.game.all_sprites, self.game.bullet_sprites))

    def bullet_impact(self, bullet, enemy):
        if type(bullet) == Bullet:
            bullet.kill()
            Laser(LASER_SURF, enemy.rect.center, bullet.direction, (self.game.all_sprites, self.game.bullet_sprites))
        if type(enemy) == Boss and type(bullet) == Laser:
            bullet.kill()

class Sword(Pistol):
    def __init__(self, surf, player, groups, game):
        super().__init__(surf, player, groups, game)
        self.distance = 150
        self.impact_sound = STAB_SOUND

    def sword_collision(self):
        collision_sprites = pygame.sprite.spritecollide(self, self.game.enemy_sprites, False, pygame.sprite.collide_mask)
        for enemy in collision_sprites:
            if type(enemy) != Orb and enemy.death_time == 0:
                self.impact_sound.play()
                if type(enemy) == Boss:
                    enemy.lives -= 1
                    if enemy.lives > 0:
                        continue
                enemy.destroy()
                self.game.kill_count += 1

    def update(self, _):
        self.get_direction()
        self.rotate()
        self.rect = self.image.get_frect(center = self.player.rect.center + self.player_direction * self.distance)
        self.sword_collision()

class Flamegun(Pistol):
    def __init__(self, surf, player, groups, game):
        super().__init__(surf, player, groups, game)
        self.animation_frames = WEAPON_FRAMES['flamegun']
        self.shoot_sound = FLAMEGUN_SOUND
        
    def create_bullet(self):
        pos = self.rect.center + self.player_direction * 50
        Bullet(FLAME_BULLET_SURF, pos, self.player_direction, (self.game.all_sprites, self.game.bullet_sprites))

    def bullet_impact(self, bullet, enemy):
        if type(bullet) == Bullet:
            bullet.kill()
            Flame(FLAME_FRAMES, enemy.rect.center, (self.game.all_sprites, self.game.bullet_sprites))
        if type(enemy) == Boss and type(bullet) == Flame:
            bullet.kill()

# Maps strings to class name for easy indexing
WEAPON_MAP = {
    "rifle": Rifle,
    "machinegun": Machinegun,
    "lasergun": Lasergun,
    "shotgun": Shotgun,
    "sideshot": Sideshotgun,
    "sword": Sword,
    "flamegun": Flamegun,
}