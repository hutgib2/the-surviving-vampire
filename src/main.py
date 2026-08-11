# /// script
# dependencies = [
#   "pytmx",
# ]
# ///

import asyncio
import pygame
from game.homescreen import HomeScreen

async def main():
    homescreen = HomeScreen()
    await homescreen.run()
    
asyncio.run(main())