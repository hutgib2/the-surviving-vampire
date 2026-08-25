"""
	Cross-platform audio for pygame (desktop) and pygbag (browser).

	-> Desktop wraps pygame.mixer.Sound. 
	-> Browser bypasses pygbag's SDL2 mixer -- whose output is distorted -- 
   	   and drives a named HTMLAudioElement via the DOM.
"""

import sys

WEB = sys.platform == "emscripten"

if WEB:
	import platform as _js  # pygbag's JS bridge, NOT the stdlib platform module
else:
	import pygame

class AudioPlayer:
	def __init__(self, file_name):
		self.file_name = file_name
		self.audio = None

	def init(self):
		"""Load the sound. Returns self so you can chain off the constructor."""
		if WEB:
			# _js.window.console.warn("PATH NAME", _js.window.location.pathname)
			file_path = f"../../audio/{self.file_name}"
			doc = _js.window.document
			el = doc.getElementById(self.file_name)
			if el is None:
				el = doc.createElement("audio")
				el.id = self.file_name
				doc.body.appendChild(el)
			el.src = file_path
			el.preload = "auto"
			# el.load()
			self.audio = el
		else:
			file_path = f"assets/audio/{self.file_name}"
			self.audio = pygame.mixer.Sound(file_path)
		return self

	def play(self, loops=0): # loops=0 plays once
		if self.audio is None:
			self.init()

		if WEB:
			self.audio.loop = loops != 0
			self.audio.currentTime = 0
			try:
				self.audio.play()
			except Exception:
				pass  # autoplay blocked until the user interacts with the page
		else:
			self.audio.play(loops=loops)

	def stop(self):
		if self.audio is None:
			return
		if WEB:
			self.audio.pause()
			self.audio.currentTime = 0
		else:
			self.audio.stop()

	def set_volume(self, vol):
		if self.audio is None:
			return

		vol = max(0.0, min(1.0, vol))
		if WEB:
			self.audio.volume = vol
		else:
			self.audio.set_volume(vol)
