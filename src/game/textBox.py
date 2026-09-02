from settings import *

class TextBox:
	def __init__(self, pos, size, font, max_len=12):
		self.rect = pygame.Rect(pos, size)
		self.font = font
		self.text = ''
		self.max_len = max_len
		self.active = True

		self.text_color = 'white'
		self.bg_color = (30, 30, 30)
		self.border_color = (200, 200, 200)
		self.border_width = 2
		self.padding = 8

	def handle_event(self, event):
		if not self.active:
			return
		if event.type == pygame.TEXTINPUT:
			if len(self.text) < self.max_len:
				self.text += event.text
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_BACKSPACE:
				self.text = self.text[:-1]
			elif event.key == pygame.K_RETURN:
				self.active = False

	def update(self):
		pygame.draw.rect(screen, self.bg_color, self.rect)
		pygame.draw.rect(screen, self.border_color , self.rect, self.border_width)
		img = self.font.render(self.text, True, self.text_color)
		screen.blit(img, (self.rect.x + self.padding, self.rect.y + self.padding))
		
		# Draw blinking cursor
		if self.active and (pygame.time.get_ticks() // 500) % 2 == 0:
			cursor_x = self.rect.x + self.padding + img.get_width() + 2
			line_height = self.font.get_height()
			pygame.draw.line(screen, self.text_color, (cursor_x, self.rect.y + self.padding), (cursor_x, self.rect.y + self.padding + line_height), 2)