from pathlib import Path

import pygame


def _files(folder, *, numeric=False):
    paths = [p for p in Path(folder).iterdir() if p.is_file()]
    return sorted(paths, key=lambda p: int(p.stem) if numeric else p.stem)


def load_image(*path, scale=1):
    surf = pygame.image.load(Path(*path)).convert_alpha()
    if scale == 1:
        return surf
    w, h = surf.get_size()
    return pygame.transform.smoothscale(surf, (int(w * scale), int(h * scale)))


def load_images(*path, scale=1):
    """Folder of numbered frames -> ordered list."""
    return [load_image(p, scale=scale) for p in _files(Path(*path), numeric=True)]


def load_images_named(*path, scale=1):
    """Folder of images -> {stem: surface}."""
    return {p.stem: load_image(p, scale=scale) for p in _files(Path(*path))}


def load_image_states(*path, scale=1):
    """Folder of subfolders -> {subfolder name: ordered frames}."""
    return {
        d.name: load_images(d, scale=scale)
        for d in sorted(Path(*path).iterdir())
        if d.is_dir()
    }


def load_audio(*path):
    return {p.stem: pygame.mixer.Sound(p) for p in _files(Path(*path))}