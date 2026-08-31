from game.settings import *
from game.the_surviving_vampire import Game
from game.button import InteractiveButton

# TASK:
# Add 2 buttons to the homescreen
# One says "Play" the other "Scores"
# When the play button is clicked, the game starts
# Don't worry about the scores button functionality for now

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
        self.home_screen_image = pygame.transform.scale(pygame.image.load(join('assets', 'images', 'menu', 'home_screen.png')), (WINDOW_WIDTH, WINDOW_HEIGHT))
        # self.game_over_screen = pygame.transform.scale(pygame.image.load(join('assets', 'images', 'menu', 'game_over.png')), (WINDOW_WIDTH, WINDOW_HEIGHT))
        # self.high_score = load_high_score()
        self.background = self.home_screen_image
        self.font = pygame.font.Font(join('assets', 'fonts', 'Oxanium-Bold.ttf'), 40)
        self.pending_game = None
        self.running = True
        
        self.menu_sprites = pygame.sprite.Group()
        self.play_button = InteractiveButton(button_surf, (7*WINDOW_WIDTH / 16, WINDOW_HEIGHT / 1.4), (WINDOW_WIDTH / 8, WINDOW_WIDTH / 16), "#FF8080", self.menu_sprites, lambda: self.play_game(), 'Play')
        self.hs_button = InteractiveButton(button_surf, (9*WINDOW_WIDTH / 16, WINDOW_HEIGHT / 1.4), (WINDOW_WIDTH / 8, WINDOW_WIDTH / 16), "#FF8080", self.menu_sprites, lambda: self.display_high_score(), 'High Scores')

    def play_game(self):
        self.pending_game = Game()
    
    def display_high_score(self):
        print("high score pressed")
    #     self.text_surf = self.font.render('high score = ' +str(self.high_score), True, 'gray25')
    #     self.text_rect = self.text_surf.get_frect(midbottom = (WINDOW_WIDTH / 2 - 180 ,WINDOW_HEIGHT - 180))
    #     screen.blit(self.text_surf, self.text_rect)

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
            # self.display_high_score()
            pygame.display.update()
            await asyncio.sleep(0)

            if self.pending_game:
                await self.pending_game.run()
                self.pending_game = None
                # self.background = self.game_over_screen