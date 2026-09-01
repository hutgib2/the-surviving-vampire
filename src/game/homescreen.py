from game.settings import *
from game.the_surviving_vampire import Game
from game.button import InteractiveButton
from game.textSprite import TextSprite

# TASK:
# We need to add the functionality to the high score button
# When its clicked we want to display a popup with the top 5 high scores in
# e.g. 1. NAME: SCORE
    #  2. NAME: SCORE

# Use the button image as the popup background
# Just use dummy data for now, I will connect to a database once its set up
# use a List of tuples for the dummy data, [(name, score), (name, score) ...]

# STEP 1:
# show / hide the popup when the high score button is clicked

# STEP 2:
# Write a TextSprite saying "High Scores"
# draw the scores list underneath in order

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
        self.hs_button = InteractiveButton(button_surf, (WINDOW_WIDTH - 200, 100), (WINDOW_WIDTH / 8, WINDOW_WIDTH / 16), "#FF8080", self.menu_sprites, lambda: self.display_high_score(), 'High Scores')

        self.hs_sprites = pygame.sprite.Group()
        self.hs_popup_surf = pygame.transform.smoothscale(button_surf, (WINDOW_WIDTH / 3, 5*WINDOW_HEIGHT / 6))
        self.hs_popup_rect = self.hs_popup_surf.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.show_highscores = False

        line_spacing = self.hs_popup_surf.get_height() / 10
        TextSprite('High Scores: ', self.hs_popup_rect.move(0, 2.2 * line_spacing).midtop, "#FF8080", 1.3 * line_spacing, self.hs_sprites)
        self.high_scores = [("Hugo", 375), ("Eden", 24), ("Ronan", 230), ("John", 67), ("Mary", 125)]
        self.high_scores = sorted(self.high_scores, key=lambda t: t[1], reverse=True)

        # for each score we will create a textsprite, with even vertical spacing between them
        for i, score in enumerate(self.high_scores):
            TextSprite(f'{i+1}. {score[0]}: {score[1]}', self.hs_popup_rect.move(0, (3.5 * line_spacing + (i * line_spacing))).midtop, "#FF8080", line_spacing, self.hs_sprites)

    def play_game(self):
        if self.show_highscores:
            return
        self.pending_game = Game()
    
    def display_high_score(self):
        self.show_highscores = not self.show_highscores
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
            if self.show_highscores:
                screen.blit(self.hs_popup_surf, self.hs_popup_rect)
                self.hs_sprites.update()
            pygame.display.update()
            await asyncio.sleep(0)

            if self.pending_game:
                await self.pending_game.run()
                self.pending_game = None
                # self.background = self.game_over_screen