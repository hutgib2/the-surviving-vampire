import pygame

# TASK:
# Create a function in Timer that return the current progress of the timer
# i.e. how long its been since the last execution, proportional to the duration
# e.g. if duration is 10s, and its been 5 seconds, it returns 0.5 == 5/10

class Timer:
    def __init__(self, duration, func = None, repeat = None, autostart = False):
        self.duration = duration
        self.start_time = 0
        self.active = False
        self.func = func
        self.repeat = repeat

        if autostart:
            self.activate()

    def __bool__(self):
        return self.active

    def activate(self):
        self.active = True
        self.start_time = pygame.time.get_ticks()
    
    def deactivate(self):
        self.active = False
        self.start_time = 0
        if self.repeat:
            self.activate()
    
    def stop(self): # Use to temporarily pause a repeating timer
        if self.repeat:
            self.repeat = False

    def resume(self):
        self.repeat = True

    def get_progress(self):
        elapsed_time = pygame.time.get_ticks() - self.start_time
        progress = elapsed_time / self.duration
        return min(progress, 1)

    def update(self):
        if pygame.time.get_ticks() - self.start_time >= self.duration:
            if self.func and self.start_time != 0:
                self.func()
            self.deactivate()