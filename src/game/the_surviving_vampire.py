from utils.async_clock import AsyncClock
from utils.timer import Timer
from utils.audio_player import AudioPlayer
from random import randint, choice
from game.settings import *  # import everything from settings.py
from game.player import Player
from game.sprites import *
from game.groups import AllSprites
from game.enemies import Enemy, Boss
from game.homescreen import *
from pytmx.util_pygame import load_pygame

class Game:
    def __init__(self):
        self.running = True
        self.clock = AsyncClock(fps=45)
        self.font = pygame.font.Font(join('assets', 'fonts', 'Oxanium-Bold.ttf'), 40)
        self.kill_count = 0
        # self.high_score = load_high_score()

        # groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.powerup_sprites = pygame.sprite.Group()
        self.laser_sprites = pygame.sprite.Group()
        self.orb_sprites = pygame.sprite.Group()
        self.explosion_sprites = pygame.sprite.Group()
        
        #events
        self.enemy_spawn_timer = Timer(400, lambda: self.spawn_enemy(), repeat=True, autostart=True)
        self.powerup_spawn_timer = Timer(15 * 1000, lambda: self.spawn_powerup(), repeat=True, autostart=True)
        self.boss_spawn_timer = Timer(60 * 1000, lambda: self.spawn_boss(), repeat=True, autostart=True)
        self.enemy_spawn_positions = []
        self.powerup_spawn_positions = []
        
        #audio
        self.shoot_sound = AudioPlayer('shoot.ogg')
        self.shoot_sound.set_volume(0.25)
        self.impact_sound = AudioPlayer('new_impact.ogg')
        self.impact_sound.set_volume(0.2)
        # self.music = pygame.mixer.Sound(join('assets', 'audio', 'my_first_mashup.ogg'))
        # self.music.set_volume(0.55)
        # self.music.play(loops = 0)
        
        self.load_map()

    def load_map(self):
        map = load_pygame(join('assets', 'data', 'maps', 'hell_map.tmx'))
        for x, y, image in map.get_layer_by_name('Ground').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites)
        for obj in map.get_layer_by_name('Objects'):
            CollisionSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))
        for collision in map.get_layer_by_name('Collisions'):
            CollisionSprite((collision.x, collision.y), pygame.Surface((collision.width, collision.height)), self.collision_sprites)
        for marker in map.get_layer_by_name('Entities'):
            if marker.name == 'Player':
                self.player = Player((marker.x, marker.y), self.all_sprites, self.collision_sprites, pistol_static, self)
            elif marker.name == 'Power up':
                self.powerup_spawn_positions.append((marker.x, marker.y))
            else:
                self.enemy_spawn_positions.append((marker.x, marker.y))

    def get_spawn_position(self, spawn_positions):
        distance_from_player = 0
        while distance_from_player < 600:
            pos = choice(spawn_positions)
            distance_from_player = pygame.math.Vector2.magnitude(pygame.math.Vector2(pos) - pygame.math.Vector2(self.player.rect.center))
        return pos  
    
    def display_score(self):
        self.text_surf = self.font.render(str(self.kill_count), True, 'gray25')
        self.text_rect = self.text_surf.get_frect(topleft = (300, 25))
        screen.blit(self.text_surf, self.text_rect)
        pygame.draw.rect(screen, 'gray25', self.text_rect.inflate(20, 10).move(0, -6), 5, 10)

    def display_lives(self):
        for i in range(self.player.lives):
            life_rect = POWERUP_SURFS['life'].get_frect(topleft = (10 + (i * 85), 10))
            screen.blit(POWERUP_SURFS['life'], life_rect)
    
    # TEST ONLY: Draw all powerup images statically on left of screen so we can see the sizes
    def display_all_powerups(self):
        for i, powerup_surf in enumerate(POWERUP_SURFS.values()):
            powerup_rect = powerup_surf.get_frect(topleft = (10, 100 + (i * 85)))
            screen.blit(powerup_surf, powerup_rect)

    def spawn_enemy(self):
        if self.player.powerup_activated == "timestop" or self.player.lives <= 0:
            return
        Enemy(self.get_spawn_position(self.enemy_spawn_positions), choice(list(enemy_frames.items())), self.player, self.collision_sprites, self)

    def spawn_boss(self):
        if self.player.powerup_activated == "timestop" or self.player.lives <= 0:
            return
        Boss(self.get_spawn_position(self.enemy_spawn_positions), self.player, self)

    def spawn_powerup(self):
        if self.player.lives <= 0 or len(self.powerup_spawn_positions) <= 0:
            return
        # create a powerup if there is space left in the powerup_spawn_positions
        pos = self.powerup_spawn_positions.pop(randint(0, len(self.powerup_spawn_positions) - 1))
        powerup = choice(list(POWERUP_SURFS.items()))
        Powerup(pos, powerup, (self.all_sprites, self.powerup_sprites), self.player)

    async def run(self):
        while self.running:
            dt = await self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.all_sprites.update(dt)
            # if self.player.is_dead:
                # self.music.stop()
                # return True
            
            self.all_sprites.draw(self.player.rect.center)
            self.display_score()
            self.display_lives()
            self.enemy_spawn_timer.update()
            self.powerup_spawn_timer.update()
            self.boss_spawn_timer.update()
            pygame.display.update()