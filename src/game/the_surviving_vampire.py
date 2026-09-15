from utils.async_clock import AsyncClock
from utils.timer import Timer
from utils.scores_api import post_score
from random import randint, choice
from game.settings import *  # import everything from settings.py
from game.player import Player
from game.sprites import *
from game.groups import AllSprites
from game.textSprite import TextSprite
from game.textBox import TextBox
from game.button import InteractiveButton
from game.enemies import Enemy, Boss
from game.homescreen import *
from pytmx.util_pygame import load_pygame
from os.path import join
from game.surfs import life_surf, POWERUP_SURFS, button_surf, pistol_static, ultimate_progress_frames, enemy_frames

# TODO: add new audio for different weapons
# TODO: Look into sideshot powerup
# TODO: Fix enemies being drawn behind objects
# TODO: see if possible to make enemies stop short of player when shield active
# TODO: change progress bar to line bar 

class Game:
    def __init__(self):
        self.running = True
        self.clock = AsyncClock(fps=45)
        self.font = pygame.font.Font(join('assets', 'fonts', 'Oxanium-Bold.ttf'), 60)
        self.kill_count = 0

        # groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.powerup_sprites = pygame.sprite.Group()
        self.laser_sprites = pygame.sprite.Group()
        self.orb_sprites = pygame.sprite.Group()
        self.explosion_sprites = pygame.sprite.Group()
        self.gameover_sprites = pygame.sprite.Group()
        
        #events
        self.enemy_spawn_timer = Timer(400, lambda: self.spawn_enemy(), repeat=True, autostart=True)
        self.powerup_spawn_timer = Timer(15 * 1000, lambda: self.spawn_powerup(), repeat=True, autostart=True)
        self.boss_spawn_timer = Timer(60 * 1000, lambda: self.spawn_boss(), repeat=True, autostart=True)
        self.enemy_spawn_positions = []
        self.powerup_spawn_positions = []
        
        self.load_map()

    def load_map(self):
        map = load_pygame(join('assets', 'data', 'maps', 'hell_map.tmx'))
        for x, y, image in map.get_layer_by_name('Ground').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites)
        for x, y, image in map.get_layer_by_name('Objects').tiles():
            CollisionSprite((x * TILE_SIZE, y * TILE_SIZE), image, (self.all_sprites))
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

    def display_header(self):
        top_offset = 60
        left_offset = 60
        spacing = 85
        
        # Drawing Lives
        for i in range(self.player.lives):
            life_rect = life_surf.get_frect(center = (left_offset + (i * spacing), top_offset))
            screen.blit(life_surf, life_rect)

        # Drawing Ultimate Progress bar
        progress = self.player.ultimate_move_timer.get_progress()
        i = int(progress * (len(ultimate_progress_frames) - 1))
        image = ultimate_progress_frames[i]
        ultimate_progress_rect = image.get_frect(center = (left_offset + 3*spacing, top_offset))
        screen.blit(image, ultimate_progress_rect)

        # Drawing score
        self.text_surf = self.font.render(str(self.kill_count), True, 'gray25')
        self.text_rect = self.text_surf.get_frect(center = (left_offset + 4*spacing, top_offset))
        screen.blit(self.text_surf, self.text_rect)
        border_thickness = 7
        border_radius = 10
        pygame.draw.rect(screen, 'gray25', self.text_rect.inflate(20, 10).move(0, -6), border_thickness, border_radius)
 
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


    # Now i want you to use the function i created to save the score to the database
    def save_score(self):
        if self.text_box.text == ''  or self.text_box.text.strip() == '':
            return
        
        username = self.text_box.text.strip().lower()
        post_score("the-surviving-vampire", username, self.kill_count)
        self.save_button.deactivate()

    async def display_gameover_popup(self):
        # create the popup + text + textbox
        self.gameover_popup_surf = pygame.transform.smoothscale(button_surf, (2*WINDOW_WIDTH / 3, 5*WINDOW_HEIGHT / 6))
        self.gameover_popup_rect = self.gameover_popup_surf.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        line_spacing = self.gameover_popup_surf.get_height() / 8

        TextSprite('Game Over!', self.gameover_popup_rect.move(0, 1.8 * line_spacing).midtop, "#FF8080", 1.3 * line_spacing, self.gameover_sprites)
        TextSprite(f'You killed {self.kill_count} enemies!', self.gameover_popup_rect.move(0, 3 * line_spacing).midtop, "#FF8080",  0.5 * line_spacing, self.gameover_sprites)
        
        self.text_box = TextBox(self.gameover_popup_rect.move(0, 4.5 * line_spacing).midtop, (self.gameover_popup_rect.width / 2, line_spacing * 0.7), self.font, self.gameover_sprites)
        TextSprite('Enter your name to save your score: ', self.text_box.rect.move(0, -0.3 * line_spacing).midtop, "#FF8080",  0.4 * line_spacing, self.gameover_sprites)
        self.save_button = InteractiveButton(button_surf, self.text_box.rect.move(0, 0.7 * line_spacing).midbottom, (WINDOW_WIDTH / 8, line_spacing), "#FF8080", self.gameover_sprites, lambda:  self.save_score(), 'Save')
        TextSprite('Press ESC to return to main menu.', self.save_button.rect.move(0, 0.5 * line_spacing).midbottom, "#FF8080",  0.4 * line_spacing, self.gameover_sprites)

        while True:
            dt = await self.clock.tick() / 1000
            for event in pygame.event.get():
                self.text_box.handle_event(event)
                self.save_button.handle_event(event)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return
                
            screen.blit(self.gameover_popup_surf, self.gameover_popup_rect)
            self.gameover_sprites.update()
            pygame.display.update()
        

    async def run(self):
        while self.running:
            dt = await self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False
            
            if self.player.is_dead:
                self.running = False

            self.all_sprites.update(dt)
            self.all_sprites.draw(self.player.rect.center)
            
            self.display_header()
            # self.display_all_powerups()
            self.enemy_spawn_timer.update()
            self.powerup_spawn_timer.update()
            self.boss_spawn_timer.update()
            pygame.display.update()
        
        await self.display_gameover_popup()
