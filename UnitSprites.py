import os
import pygame
import re
import pygame.locals


def get_is_stand_sprites(folder):
    pattern_with_gender = re.compile(r"^(.*?) \((M|F)\) \{IS\}-stand\.png$")
    pattern_without_gender = re.compile(r"^(.*?) \{IS\}-stand\.png$")

    sprite_dict = {}
    for filename in os.listdir(folder):
        if not filename.endswith("-stand.png"):
            continue

        match_gender = pattern_with_gender.match(filename)
        match_nogender = pattern_without_gender.match(filename)

        if match_gender:
            class_name, gender = match_gender.groups()
            gender = "Male" if gender == "M" else "Female"
            sprite_dict[(class_name.strip(), gender)] = os.path.join(folder, filename)
        elif match_nogender:
            class_name = match_nogender.group(1).strip()
            for gender in ["Male", "Female"]:
                sprite_dict[(class_name, gender)] = os.path.join(folder, filename)

    return sprite_dict


class SpriteManager:
    def __init__(self, folder):
        self.sprites = get_is_stand_sprites(folder)
        self.cache = {}

    def get_sprite(self, unit_class, gender):
        key = (unit_class, gender)
        if key not in self.cache:
            path = self.sprites.get(key)
            if path is None:
                print(f"No sprite found for class '{unit_class}', gender '{gender}'")
                return None
            try:
                sheet = pygame.image.load(path).convert_alpha()
                self.cache[key] = sheet
            except pygame.error as e:
                print(f"Failed to load sprite at {path}: {e}")
                return None
        sheet = self.cache[key]

        rect = pygame.Rect(24, 24, 16, 16)
        frame = pygame.Surface((16, 16), pygame.SRCALPHA)
        frame.blit(sheet, (0, 0), rect)

        # Set the background color as transparent
        frame.set_colorkey((128, 160, 128))

        return frame
