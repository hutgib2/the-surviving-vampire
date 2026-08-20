from game.settings import *
from game.projectiles import Bullet, Laser, Orb, Flame
from game.enemies import Enemy, Boss
from math import atan2, degrees

''' TASK
    - we want to add the shoot animation to the Gun,
    - we have a static gun image which should be displayed when not shooting
    - we have an animation that we want to run when shooting
    - after the shoot animation is finished we want to display the static image again

    - reuse a lot of the code from the player animation, but this one doesnt have direction
    - i.e. there is no 'left' 'up' 'down' 'right' options

    - we will need to rotate each frame for this animation (I WILL HELP WITH THIS AT THE END)
'''
class Gun(pygame.sprite.Sprite):
    def __init__(self, surf, player, groups, game):
        super().__init__(groups)
        self.player = player
        self.distance = 120
        self.game = game
        self.player_direction = pygame.Vector2(1, -1)
        self.original_surf = surf
        self.image = self.original_surf # what we display after rotation
        self.current_image = self.image # what we set the image to be depending on whether animation is running
        self.rect = self.image.get_frect(center = self.player.rect.center + self.player_direction * self.distance)
        self.can_shoot = True
        self.shoot_time = 0
        self.cooldown = 300
        
        self.frame_index = 0
        self.animation_speed = 40
        self.is_shooting = False

    def run_animation(self, frames, dt):
        self.frame_index += self.animation_speed * dt

        # when animation finishes, reset for next time
        if int(self.frame_index) >= len(frames):
            self.is_shooting = False
            self.frame_index = 0
            return
        
        self.current_image = frames[int(self.frame_index)]
        
    def animate(self, dt):
        if self.is_shooting:
            self.run_animation(shoot_frames, dt)
        else:
            self.current_image = self.original_surf

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

    def shoot(self):
        if pygame.mouse.get_pressed()[0] and self.can_shoot:
            self.is_shooting = True
            self.game.shoot_sound.play()
            pos = self.rect.center + self.player_direction * 50
            Bullet(bullet_surf, pos, self.player_direction, (self.game.all_sprites, self.game.bullet_sprites))
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

class PiercingGun(Gun):
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

class Shotgun(Gun):        
    def shoot(self):
        if pygame.mouse.get_pressed()[0] and self.can_shoot:
            self.game.shoot_sound.play()
            pos = self.rect.center + self.player_direction * 64
            Bullet(bullet_surf, pos, self.player_direction, (self.game.all_sprites, self.game.bullet_sprites))
            Bullet(bullet_surf, pos, self.player_direction.rotate(45), (self.game.all_sprites, self.game.bullet_sprites))
            Bullet(bullet_surf, pos, self.player_direction.rotate(-45), (self.game.all_sprites, self.game.bullet_sprites))
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()

class Sideshotgun(Gun):
    def shoot(self):
        if pygame.mouse.get_pressed()[0] and self.can_shoot:
            self.game.shoot_sound.play()
            pos = self.rect.center + self.player_direction * 64
            Bullet(bullet_surf, pos, self.player_direction, (self.game.all_sprites, self.game.bullet_sprites))
            Bullet(bullet_surf, pos, self.player_direction.rotate(90), (self.game.all_sprites, self.game.bullet_sprites))
            Bullet(bullet_surf, pos, self.player_direction.rotate(-90), (self.game.all_sprites, self.game.bullet_sprites))
            Bullet(bullet_surf, pos, self.player_direction.rotate(180), (self.game.all_sprites, self.game.bullet_sprites))
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()

class Machinegun(Gun):
    def __init__(self, surf, player, groups, game):
        super().__init__(surf, player, groups, game)
        self.cooldown = 100

class Lasergun(Gun):
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


class Sword(Gun):
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

class Flamegun(Gun):
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