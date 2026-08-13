import pygame
import asyncio


class AsyncClock:
	def __init__(self, fps=60):
		self.previous_tick = pygame.time.get_ticks()
		self.frame_duration = 1000 / fps # milliseconds

	async def tick(self):
		elapsed_time = pygame.time.get_ticks() - self.previous_tick
		await asyncio.sleep((max(0, self.frame_duration - elapsed_time)) / 1000)
		
		now = pygame.time.get_ticks()
		dt = now - self.previous_tick
		self.previous_tick = now
		return dt
