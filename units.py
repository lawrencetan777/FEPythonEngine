from UnitSprites import SpriteManager

sprites = SpriteManager("resources/map_sprites")


class Unit:
    def __init__(
        self, name, rpgclass, gender, startX, startY, class_data=None, level=1
    ):
        self.name = name
        self.rpgclass = rpgclass
        self.gender = gender  # "Male" or "Female"
        self.x = startX
        self.y = startY
        self.level = level

        # Convert gender to short code for matching JSON 'nid'
        gender_code = "M" if gender.lower().startswith("m") else "F"
        target_nid = f"{rpgclass} ({gender_code}) {{IS}}"

        # Find the class info in the JSON list using 'nid'
        self.class_info = None
        if class_data:
            for c in class_data:
                if c.get("nid") == target_nid:
                    self.class_info = c
                    break

        if self.class_info is None:
            raise Exception(f"Class info for '{target_nid}' not found in JSON data")

        # Store stats sections
        self.bases = self.class_info["bases"]
        self.growths = self.class_info["growths"]
        self.max_stats = self.class_info["max_stats"]
        self.promotion_bonus = self.class_info.get("promotion", {})

        # Calculate stats based on level
        self.stats = self.calculate_stats(level)

        # Load sprite based on rpgclass and gender
        # Assumes your SpriteManager expects rpgclass and gender ("Male"/"Female")
        from UnitSprites import SpriteManager

        self.sprites = SpriteManager("resources/map_sprites")
        self.image = self.sprites.get_sprite(rpgclass, gender)

    def calculate_stats(self, level):
        stats = {}
        for stat, base_val in self.bases.items():
            growth = self.growths.get(stat, 0)
            gained = int((growth * level) / 100)
            val = base_val + gained
            val = min(val, self.max_stats.get(stat, val))
            stats[stat] = val
        return stats

    def draw(self, surface, x_offset, y_offset):
        screen_x = (self.x - x_offset) * 16
        screen_y = (self.y - y_offset) * 16
        if self.image:
            surface.blit(self.image, (screen_x, screen_y))
