from game.settings import *


def scale_image(surf, scale):
    width, height = surf.get_size()
    return pygame.transform.smoothscale(surf, (width * scale, height * scale))


def load_image_states(*path, scale=1):
    frames = {"left": [], "right": [], "up": [], "down": []}
    for state in frames.keys():  # frames.keys() => ('left', 'right', 'up', 'down')
        for folder_path, _, file_names in walk(join(*path, state)):
            if file_names:
                for file_name in sorted(
                    file_names, key=lambda name: int(name.split(".")[0])
                ):
                    full_path = join(folder_path, file_name)
                    surf = pygame.image.load(full_path).convert_alpha()
                    surf = scale_image(surf, scale)
                    frames[state].append(surf)
    return frames


def load_images_named(*path):
    surfs = {}
    for folder_path, _, file_names in walk(join(*path)):
        for file_name in file_names:
            full_path = join(folder_path, file_name)
            surfs[file_name.split(".")[0]] = pygame.image.load(
                full_path
            ).convert_alpha()
    return surfs


def load_image(*path, scale=1):
    surf = pygame.image.load(join(*path)).convert_alpha()
    scale_image(surf, scale)
    return surf


def load_images(*path, scale=1):
    surf_list = []
    for folder_path, _, file_names in walk(join(*path)):
        for file_name in sorted(file_names, key=lambda name: int(name.split(".")[0])):
            full_path = join(folder_path, file_name)
            surf = pygame.image.load(full_path).convert_alpha()
            surf = scale_image(surf, scale)
            surf_list.append(surf)
    return surf_list


def audio_importer(*path):
    audio_dict = {}
    for folder_path, _, file_names in walk(join(*path)):
        for file_name in file_names:
            audio_dict[file_name.split(".")[0]] = pygame.mixer.Sound(
                join(folder_path, file_name)
            )
    return audio_dict
