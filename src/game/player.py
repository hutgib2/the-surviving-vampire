from utils.timer import Timer
from game.settings import *
from game.weapons import (
    Pistol,
    Rifle,
    Shotgun,
    Machinegun,
    Lasergun,
    Sideshotgun,
    Sword,
    Flamegun,
)

# TODO: Add special move that kills all enemies on screen
# Special move:
# - has its own special animation
# - kills every player on the screen, does 1 damage to the boss
# - 100s cooldown
# - Press SPACE to activate
# - player does NOT start with one in the bank
# - Movement and weapon disabled during special move animation
# - He can still take damage

# STEPS:
# 1. Import the files and get the animation working
# 2. Detect SPACE press and print "ultimate move",
#      -  then run animation
# 3. Make the powerup kill the enemies
# 4. Add cooldown
# 5. Restrict movement and weapon during animation

# 6. Add a visual timer to see when powerup is ready to use


# from game.homescreen import save_high_score
from game.projectiles import Orb, Mine
from game.enemies import Boss
from utils.file_importer import load_image_states

PLAYER_SPEED = 350
ANIMATION_SPEED = 8

class Aura(pygame.sprite.Sprite):
    def __init__(self, groups, surf, player):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center=player.rect.center)
        self.player = player
        self.radius = 800

    def update(self, _):
        self.rect.center = self.player.rect.center

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites, pistol_static, game):
        super().__init__(groups)
        self.idle_frames = load_image_states("assets", "images", "vampire", "idle", scale=3)
        self.walk_frames = load_image_states("assets", "images", "vampire", "walk", scale=3)
        self.hurt_frames = load_image_states("assets", "images", "vampire", "hurt", scale=3)
        self.dead_frames = load_image_states("assets", "images", "vampire", "dead", scale=3)
        self.fly_frames = load_image_states("assets", "images", "vampire", "fly", scale=3)
        self.ultimate_move_frames = load_image_states("assets", "images", "vampire", "ultimate_move", scale=3)
        self.image = self.walk_frames["down"][0]

        self.animation_state = "idle" # "idle" | "walk" | "hurt" | "dead" | "ultimate_move"
        self.animation_direction = "down"
        self.animation_speed = ANIMATION_SPEED
        self.animation_finished = False
        self.frame_index = 0

        self.game = game
        self.rect = self.image.get_frect(center=pos)
        self.move_direction = pygame.math.Vector2()
        self.speed = PLAYER_SPEED
        self.collision_sprites = collision_sprites
        self.hitbox_rect = self.rect.inflate(-self.rect.width * 0.2, -self.rect.height * 0.9)
        self.hitbox_rect.midbottom = self.rect.midbottom
        self.lives = 3
        # self.is_dead = False
        
        self.weapon = Pistol(pistol_static, self, self.game.all_sprites, self.game)
        # self.weapon = Rifle(rifle_static, self, self.game.all_sprites, self.game)
        # self.weapon = Lasergun(lasergun_static, self, self.game.all_sprites, self.game)
        # self.weapon = Flamegun(flamegun_static, self, self.game.all_sprites, self.game)
        
        # powerup
        self.powerup_activated = None
        self.powerup_cooldown = 7000
        self.powerup_activated_at = 0
        self.aura = None
        self.minedrop_time = 0
        self.minedrop_cooldown = 500
        self.can_drop_mine = False

        self.ultimate_move_timer = Timer(5 * 1000, self.activate_ultimate_move, autostart=True)
        self.can_use_ultimate = False
    
    def move(self, dt):
        if self.animation_state == "ultimate_move":
            return
        self.hitbox_rect.x += self.move_direction.x * self.speed * dt
        self.object_collision("horizontal")
        self.hitbox_rect.y += self.move_direction.y * self.speed * dt
        self.object_collision("vertical")
        self.rect.center = self.hitbox_rect.center

    def object_collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction == "horizontal":
                    if self.move_direction.x > 0:
                        self.hitbox_rect.right = sprite.rect.left
                    if self.move_direction.x < 0:
                        self.hitbox_rect.left = sprite.rect.right
                if direction == "vertical":
                    if self.move_direction.y > 0:
                        self.hitbox_rect.bottom = sprite.rect.top
                    if self.move_direction.y < 0:
                        self.hitbox_rect.top = sprite.rect.bottom

    def user_input(self):
        keys = pygame.key.get_pressed()
        self.move_direction.x = int(keys[pygame.K_RIGHT] or keys[pygame.K_d]) - int(keys[pygame.K_LEFT] or keys[pygame.K_a])
        self.move_direction.y = int(keys[pygame.K_DOWN] or keys[pygame.K_s]) - int(keys[pygame.K_UP] or keys[pygame.K_w])
        if self.move_direction:
            self.move_direction = self.move_direction.normalize()
        if keys[pygame.K_SPACE]:
            self.use_ultimate_move()

    def activate_ultimate_move(self):
        self.can_use_ultimate = True
    
    def use_ultimate_move(self):
        if not self.can_use_ultimate:
            return
            
        self.weapon.shoot_timer.stop()
        self.can_use_ultimate = False
        self.ultimate_move_timer.activate()
        self.set_animation_state('ultimate_move')
        self.game.impact_sound.play()
        for enemy in self.game.enemy_sprites:
            if type(enemy) == Orb:
                continue
            if type(enemy) == Boss:
                enemy.lives -= 1
                if enemy.lives > 0:
                    continue
            enemy.destroy()
            self.game.kill_count += 1

    def run_animation(self, frames, dt, loop=False):
        if self.move_direction:
            statex = 'right' if self.move_direction.x > 0 else 'left'
            statey = 'down' if self.move_direction.y > 0 else 'up'
            self.animation_direction = statex if abs(self.move_direction.x) > abs(self.move_direction.y) else statey
        
        self.frame_index += self.animation_speed * dt
        current = frames[self.animation_direction]

        if loop:
            index = int(self.frame_index) % len(current)
        else:
            index = min(int(self.frame_index), len(current) - 1)
            if int(self.frame_index) > len(current) - 1:
                self.animation_finished = True

        self.image = frames[self.animation_direction][index] 

    def animate(self, dt):
        if self.animation_state == "dead":
            self.run_animation(self.dead_frames, dt)
        elif self.animation_state == "hurt":
            self.run_animation(self.hurt_frames, dt)
        elif self.animation_state == "idle":
            self.run_animation(self.idle_frames, dt, loop=True)
        elif self.animation_state == "walk":
            self.run_animation(self.walk_frames, dt, loop=True)
        elif self.animation_state == "fly":
            self.run_animation(self.fly_frames, dt, loop=True)
        elif self.animation_state == "ultimate_move":
            self.run_animation(self.ultimate_move_frames, dt)

        if self.powerup_activated == "shield":
            self.image.set_alpha(130)
        else:
            self.image.set_alpha(255)

    def set_animation_state(self, state):
        if self.animation_state == "dead" or state == self.animation_state:
            return
        self.animation_state = state
        self.frame_index = 0
        self.animation_finished = False

    def update_animation_state(self):
        if self.animation_state == "dead":
            # TODO: fix the playing of dead animation
            # if self.animation_finished:
            #     self.is_dead = True
            return

        if self.animation_state == "hurt":
            if not self.animation_finished:
                return
            if self.powerup_activated == "superspeed":
                self.set_animation_state("fly")

        if self.animation_state == "fly" and not self.animation_finished:
            return
        
        if self.animation_state == "ultimate_move":
            if not self.animation_finished:
                return
            self.weapon.shoot_timer.resume()
        
        self.set_animation_state("walk" if self.move_direction else "idle")

    def enemy_collision(self):
        if self.lives <= 0:
            return
        collision_sprites = pygame.sprite.spritecollide(self, self.game.enemy_sprites, False, pygame.sprite.collide_mask)
        for enemy in collision_sprites:
            if self.powerup_activated != "shield":
                if type(enemy) == Orb:
                    enemy.kill()
                elif type(enemy) == Boss:
                    pass
                else:
                    enemy.destroy(hit_player=True)
                self.game.impact_sound.play()
                self.lives -= 1
                if self.lives <= 0:
                    self.kill()
                self.set_animation_state("hurt" if self.lives > 0 else "dead")

    def explosion_collisions(self):
        collision_sprites = pygame.sprite.groupcollide(
            self.game.explosion_sprites,
            self.game.enemy_sprites,
            False,
            False,
            pygame.sprite.collide_mask,
        )
        for explosion, enemies in collision_sprites.items():
            for enemy in enemies:
                if type(enemy) == Orb:
                    continue
                self.game.impact_sound.play()
                if type(enemy) == Boss:
                    explosion.kill()
                    enemy.lives -= 1
                    if enemy.lives > 0:
                        continue
                enemy.destroy()
                self.game.kill_count += 1

    def powerup_collision(self):
        powerup_collisions = pygame.sprite.spritecollide(self, self.game.powerup_sprites, True, pygame.sprite.collide_mask)
        for powerup in powerup_collisions:
            self.deactivate_powerup()
            self.game.powerup_spawn_positions.append(powerup.rect.center)
            if powerup.type == "life":
                if self.lives < 3:
                    self.lives += 1
                continue
            self.powerup_activated_at = pygame.time.get_ticks()
            self.powerup_activated = powerup.type
            if powerup.type == "superspeed":
                self.speed = PLAYER_SPEED * 3
                self.animation_speed = ANIMATION_SPEED * 2
                self.set_animation_state("fly")
                continue
            if powerup.type == "shield":
                return
            if powerup.type == "slowaura":
                if self.aura != None:
                    self.aura.kill()
                self.aura = Aura(self.game.all_sprites, aura_surf, self)
                return
            if powerup.type == "timestop":
                continue
            if powerup.type == "mine":
                self.can_drop_mine = True
                continue

            # Weapon change
            self.weapon.kill()
            if powerup.type == "rifle":
                self.weapon = Rifle(rifle_static, self, self.game.all_sprites, self.game)
            elif powerup.type == "machinegun":
                self.weapon = Machinegun(machinegun_static, self, self.game.all_sprites, self.game)
            elif powerup.type == "laser":
                self.weapon = Lasergun(lasergun_static, self, self.game.all_sprites, self.game)
            elif powerup.type == "shotgun":
                self.weapon = Shotgun(shotgun_static, self, self.game.all_sprites, self.game)
            elif powerup.type == "sideshot":
                self.weapon = Sideshotgun(pistol_static, self, self.game.all_sprites, self.game)
            elif powerup.type == "sword":
                self.weapon = Sword(sword_surf,self,self.game.all_sprites,self.game)
            elif powerup.type == "flamegun":
                self.weapon = Flamegun(flamegun_static, self, self.game.all_sprites, self.game)

    def deactivate_powerup(self):
        if self.powerup_activated == "superspeed":
            self.speed = PLAYER_SPEED
            self.animation_speed = ANIMATION_SPEED
            self.set_animation_state("walk")
        elif self.powerup_activated == "slowaura":
            self.aura.kill()
            self.aura = None
        elif self.powerup_activated == "timestop" or self.powerup_activated == "mine":
            pass
        else:
            self.weapon.kill()
            self.weapon = Pistol(pistol_static, self, self.game.all_sprites, self.game)

        self.powerup_activated = None

    def powerup_timer(self):
        if self.powerup_activated != None:
            current_time = pygame.time.get_ticks()
            if current_time - self.powerup_activated_at >= self.powerup_cooldown:
                self.deactivate_powerup()

    def mine_timer(self):
        if self.powerup_activated == "mine" and self.can_drop_mine:
            Mine(POWERUP_SURFS['mine'], self.rect.center, self.game.all_sprites, self.game)
            self.minedrop_time = pygame.time.get_ticks()
            self.can_drop_mine = False
        elif pygame.time.get_ticks() - self.minedrop_time >= self.minedrop_cooldown:
            self.can_drop_mine = True

    def kill(self):
        self.speed = 0
        # self.animation_direction = 'down'
        if self.weapon:
            self.weapon.kill()
        self.weapon = None

    def update(self, dt):
        self.user_input()
        self.move(dt)
        self.enemy_collision()
        self.powerup_collision()
        self.explosion_collisions()
        self.powerup_timer()
        self.mine_timer()
        self.ultimate_move_timer.update()
        self.update_animation_state()
        self.animate(dt)

