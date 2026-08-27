from game.settings import *
from game.projectiles import Bullet, Laser, Orb, Flame
from game.enemies import Enemy, Boss
from math import atan2, degrees

class Pistol(pygame.sprite.Sprite):
    def __init__(self, surf, player, groups, game):
        super().__init__(groups)
        self.player = player
        self.distance = 120
        self.game = game
        self.player_direction = pygame.Vector2(1, -1)
        
        self.static_frame = surf
        self.image = self.static_frame # what we display after rotation
        self.current_image = self.image # what we set the image to be depending on whether animation is running
        self.rect = self.image.get_frect(center = self.player.rect.center + self.player_direction * self.distance)
        
        self.can_shoot = True
        self.shoot_time = 0
        self.cooldown = 300
        
        self.frame_index = 0
        self.animation_frames = pistol_frames
        self.animation_speed = self.cooldown / 7.5
        self.animation_running = False

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
        Bullet(bullet_surf, pos, self.player_direction, (self.game.all_sprites, self.game.bullet_sprites))

    def shoot(self):
        if pygame.mouse.get_pressed()[0] and self.can_shoot:
            self.animation_running = True
            self.game.shoot_sound.play()
            self.create_bullet()
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()
    
    def shoot_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time >= self.cooldown:
                self.can_shoot = True
    
    def bullet_collision(self):
        collision_sprites = pygame.sprite.groupcollide(self.game.bullet_sprites, self.game.enemy_sprites, False, False, pygame.sprite.collide_mask)
        for bullet, enemies in collision_sprites.items():
            for enemy in enemies:
                if type(enemy) == Orb:
                    continue
                self.game.impact_sound.play()
                bullet.kill()
                if type(enemy) == Boss:
                    enemy.lives -= 1
                    if enemy.lives > 0:
                        continue
                enemy.destroy(False)
                self.game.kill_count += 1

    def update(self, dt):
        self.animate(dt)
        self.get_direction()
        self.rotate()
        self.rect.center = self.player.rect.center + (self.player_direction + pygame.Vector2(0, -0.2)) * self.distance
        self.shoot_timer()
        self.shoot()
        self.bullet_collision()

class Rifle(Pistol):
    def __init__(self, surf, player, groups, game):
        super().__init__(surf, player, groups, game)
        self.animation_frames = rifle_frames
        self.animation_speed = self.cooldown / 4

    def bullet_collision(self):
        collision_sprites = pygame.sprite.groupcollide(self.game.bullet_sprites, self.game.enemy_sprites, False, False, pygame.sprite.collide_mask)
        for bullet, enemies in collision_sprites.items():
            for enemy in enemies:
                if type(enemy) == Orb:
                    continue
                self.game.impact_sound.play()
                if type(enemy) == Boss:
                    enemy.lives -= 1
                    bullet.kill()
                    if enemy.lives > 0:
                        continue
                enemy.destroy(False)
                self.game.kill_count += 1

class Shotgun(Pistol):
    def __init__(self, surf, player, groups, game):
        super().__init__(surf, player, groups, game)
        self.animation_frames = shotgun_frames
        self.cooldown = 500

    def create_bullet(self):
        pos = self.rect.center + self.player_direction * 64
        Bullet(bullet_surf, pos, self.player_direction, (self.game.all_sprites, self.game.bullet_sprites))
        Bullet(bullet_surf, pos, self.player_direction.rotate(15), (self.game.all_sprites, self.game.bullet_sprites))
        Bullet(bullet_surf, pos, self.player_direction.rotate(-15), (self.game.all_sprites, self.game.bullet_sprites))
        Bullet(bullet_surf, pos, self.player_direction.rotate(30), (self.game.all_sprites, self.game.bullet_sprites))
        Bullet(bullet_surf, pos, self.player_direction.rotate(-30), (self.game.all_sprites, self.game.bullet_sprites))

class Sideshotgun(Pistol):
    def create_bullet(self):
        pos = self.rect.center + self.player_direction * 64
        Bullet(bullet_surf, pos, self.player_direction, (self.game.all_sprites, self.game.bullet_sprites))
        Bullet(bullet_surf, pos, self.player_direction.rotate(90), (self.game.all_sprites, self.game.bullet_sprites))
        Bullet(bullet_surf, pos, self.player_direction.rotate(-90), (self.game.all_sprites, self.game.bullet_sprites))
        Bullet(bullet_surf, pos, self.player_direction.rotate(180), (self.game.all_sprites, self.game.bullet_sprites))

class Machinegun(Pistol):
    def __init__(self, surf, player, groups, game):
        super().__init__(surf, player, groups, game)
        self.cooldown = 100
        self.animation_frames = machinegun_frames

class Lasergun(Pistol):
    def __init__(self, surf, player, groups, game):
        super().__init__(surf, player, groups, game)
        self.animation_frames = lasergun_frames

    def create_bullet(self):
        pos = self.rect.center + self.player_direction * 50
        Bullet(laser_bullet_surf, pos, self.player_direction, (self.game.all_sprites, self.game.bullet_sprites))
        
    def bullet_collision(self):
        collision_sprites = pygame.sprite.groupcollide(self.game.bullet_sprites, self.game.enemy_sprites, False, False, pygame.sprite.collide_mask)
        for bullet, enemies in collision_sprites.items():
            for enemy in enemies:
                if type(enemy) == Orb:
                    continue
                self.game.impact_sound.play()
                if type(bullet) == Bullet:
                    bullet.kill()
                    Laser(laser_surf, enemy.rect.center, bullet.direction, (self.game.all_sprites, self.game.bullet_sprites))
                if type(enemy) == Boss:
                    if type(bullet) == Laser:
                        bullet.kill()
                    enemy.lives -= 1
                    if enemy.lives > 0:
                        continue
                enemy.destroy(False)
                self.game.kill_count += 1

class Sword(Pistol):
    def __init__(self, surf, player, groups, game):
        super().__init__(surf, player, groups, game)
        self.distance = 250

    def Sword_collision(self):
        collision_sprites = pygame.sprite.spritecollide(self, self.game.enemy_sprites, False, pygame.sprite.collide_mask)
        for enemy in collision_sprites:
            if type(enemy) != Orb and enemy.death_time == 0:
                self.game.impact_sound.play()
                if type(enemy) == Boss:
                    enemy.lives -= 1
                    if enemy.lives > 0:
                        continue
                enemy.destroy(False)
                self.game.kill_count += 1

    def update(self, _):
        self.get_direction()
        self.rotate()
        self.rect = self.image.get_frect(center = self.player.rect.center + self.player_direction * self.distance)
        self.Sword_collision()

class Flamegun(Pistol):
    def __init__(self, surf, player, groups, game):
        super().__init__(surf, player, groups, game)
        self.animation_frames = flamegun_frames
        
    def create_bullet(self):
        pos = self.rect.center + self.player_direction * 50
        Bullet(flame_bullet_surf, pos, self.player_direction, (self.game.all_sprites, self.game.bullet_sprites))
        
    def bullet_collision(self):
        collision_sprites = pygame.sprite.groupcollide(self.game.bullet_sprites, self.game.enemy_sprites, False, False, pygame.sprite.collide_mask)
        for bullet, enemies in collision_sprites.items():
            for enemy in enemies:
                if type(enemy) == Orb:
                    continue
                self.game.impact_sound.play()
                if type(bullet) == Bullet:
                    bullet.kill()
                    Flame(flame_frames, enemy.rect.center, (self.game.all_sprites, self.game.bullet_sprites))
                if type(enemy) == Boss:
                    if type(bullet) == Flame:
                        bullet.kill()
                    enemy.lives -= 1
                    if enemy.lives > 0:
                        continue
                enemy.destroy(False)
                self.game.kill_count += 1
