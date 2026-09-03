from game.settings import *


class TextBox(pygame.sprite.Sprite):
    def __init__(self, pos, size, font, groups, max_len=24):
        super().__init__(groups)
        self.rect = pygame.Rect((0, 0), size).move_to(center=pos)
        self.font = font
        self.text = ""
        self.max_len = max_len
        self.active = False

        self.text_color = "#FF8080"
        self.bg_color = (30, 30, 30)
        self.border_color = (200, 200, 200)
        self.border_width = 8
        self.padding = 8

    def activate(self):
        pygame.key.start_text_input()
        self.active = True

    def deactivate(self):
        pygame.key.stop_text_input()
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.activate() if self.rect.collidepoint(event.pos) else self.deactivate()
        if not self.active:
            return
        if event.type == pygame.TEXTINPUT:
            if len(self.text) < self.max_len:
                self.text += event.text
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            # elif event.key == pygame.K_RETURN:
            # 	self.active = False

    def update(self):
        # Draw text box
        pygame.draw.rect(screen, self.bg_color, self.rect)
        pygame.draw.rect(screen, self.border_color, self.rect, self.border_width)
        img = self.font.render(self.text, True, self.text_color)
        screen.blit(img, (self.rect.x + self.padding, self.rect.y + self.padding))

        # Draw blinking cursor
        if self.active and (pygame.time.get_ticks() // 500) % 2 == 0:
            cursor_x = self.rect.x + self.padding + img.get_width() + self.padding
            line_height = self.font.get_height()
            pygame.draw.line(
                screen,
                self.text_color,
                (cursor_x, self.rect.y + self.padding),
                (cursor_x, self.rect.y + self.padding + line_height),
                4, # line width
            )
