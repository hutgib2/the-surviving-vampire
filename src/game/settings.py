import asyncio
import pygame

pygame.init()
screen = pygame.display.set_mode((1280 * 1.8, 720 * 1.8))
pygame.display.set_caption("Vampire Survivor")

WINDOW_WIDTH, WINDOW_HEIGHT = screen.get_size()
TILE_SIZE = 48