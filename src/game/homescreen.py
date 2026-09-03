from game.button import InteractiveButton
from game.settings import *
from game.sprites import Sprite
from game.textSprite import TextSprite
from game.the_surviving_vampire import Game
from utils.scores_api import fetch_scores


def load_high_score():
    with open(join('assets', 'data', 'high_score.txt'), 'r') as file:
        content = file.read()
        highscore = int(content.split("=")[1])
        return highscore

def save_high_score(current_score):
    with open(join('assets', 'data', 'high_score.txt'), 'w') as file:
        file.write('highscore=' + str(current_score))

class HomeScreen:
    def __init__(self):
        self.home_screen_image = pygame.transform.smoothscale(pygame.image.load(join('assets', 'images', 'menu', 'home_screen.png')), (WINDOW_WIDTH, WINDOW_HEIGHT))
        # self.game_over_screen = pygame.transform.scale(pygame.image.load(join('assets', 'images', 'menu', 'game_over.png')), (WINDOW_WIDTH, WINDOW_HEIGHT))
        # self.high_score = load_high_score()
        self.background = self.home_screen_image
        self.font = pygame.font.Font(join('assets', 'fonts', 'Oxanium-Bold.ttf'), 40)
        self.pending_game = None
        self.running = True
        
        self.menu_sprites = pygame.sprite.Group()
        self.play_button = InteractiveButton(button_surf, (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 1.4), (WINDOW_WIDTH / 8, WINDOW_WIDTH / 16), "#FF8080", self.menu_sprites, lambda: self.play_game(), 'Play')
        self.hs_button = InteractiveButton(button_surf, (WINDOW_WIDTH - 200, 100), (WINDOW_WIDTH / 8, WINDOW_WIDTH / 16), "#FF8080", self.menu_sprites, lambda: self.show_scores_popup(), 'High Scores')

        self.hs_sprites = pygame.sprite.Group()
        self.show_highscores = False
        self.high_scores = None
        self.hs_popup_surf = pygame.transform.smoothscale(button_surf, (WINDOW_WIDTH / 3, 5*WINDOW_HEIGHT / 6))
        self.hs_popup_rect = self.hs_popup_surf.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        
        self.fetch_task = asyncio.create_task(fetch_scores('the-surviving-vampire'))
        self.build_hs_sprites()

    def build_hs_sprites(self):
        self.hs_sprites.empty()

        font_color = "#FF8080"
        line_spacing = self.hs_popup_rect.height / 10
        title_font_size = 1.3 * line_spacing
        regular_font_size = line_spacing

        TextSprite('High Scores: ', self.hs_popup_rect.move(0, 2.2 * line_spacing).midtop, font_color, title_font_size, self.hs_sprites)
       
        if self.high_scores == None:
            TextSprite('Loading...', self.hs_popup_rect.move(0, 3.5 * line_spacing).midtop, font_color, title_font_size, self.hs_sprites)
        elif len(self.high_scores) == 0:
            TextSprite('No scores yet!', self.hs_popup_rect.move(0, 3.5 * line_spacing).midtop, font_color, regular_font_size, self.hs_sprites)
        else:
            for i, entry in enumerate(self.high_scores):
                TextSprite(f'{i+1}. {entry['username']}: {entry['score']}', self.hs_popup_rect.move(0, (3.5 * line_spacing + (i * line_spacing))).midtop, font_color, regular_font_size, self.hs_sprites)

    def play_game(self):
        if self.show_highscores:
            return
        self.pending_game = Game()
    
    def show_scores_popup(self):
        self.show_highscores = not self.show_highscores

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for menu_sprite in self.menu_sprites:
                    if menu_sprite.rect.collidepoint(event.pos):
                        menu_sprite.is_clicked()

    async def run(self):
        while self.running:
            self.handle_events()
            screen.blit(self.background, (0, 0))
            self.menu_sprites.update()

            # rebuild high score sprites when data is fetched
            if self.fetch_task is not None and self.fetch_task.done():
                self.high_scores = self.fetch_task.result()
                self.fetch_task = None
                self.build_hs_sprites()

            if self.show_highscores:
                screen.blit(self.hs_popup_surf, self.hs_popup_rect)
                self.hs_sprites.update()

            pygame.display.update()
            await asyncio.sleep(0)

            if self.pending_game:
                await self.pending_game.run()
                self.pending_game = None
                # self.background = self.game_over_screen