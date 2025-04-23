import random

class Perk:
    def __init__(self, name, description, effect_type, modifier=None, value=0):
        self.name = name
        self.description = description
        self.effect_type = effect_type  # 'passive' or 'active'
        self.modifier = modifier  # What attribute this perk modifies
        self.value = value  # The amount of modification
        self.active = False  # For active abilities
        self.cooldown = 0  # For active abilities
        self.max_cooldown = 0  # For active abilities

    def apply(self, player):
        """Apply the perk effect to the player"""
        if self.effect_type == 'passive':
            self._apply_passive(player)

    def _apply_passive(self, player):
        """Apply passive perk effects"""
        if self.modifier == 'speed':
            player.speed_multiplier += self.value
        elif self.modifier == 'hp':
            player.max_hp += self.value
            player.hp += self.value
        elif self.modifier == 'fire_rate':
            player.fire_rate_multiplier += self.value
        elif self.modifier == 'pierce':
            player.bullet_pierce += self.value

class PerkManager:
    def __init__(self):
        self.available_perks = []
        self.init_perks()

    def init_perks(self):
        """Initialize the list of available perks"""
        # Movement perks
        self.available_perks.append(
            Perk("Speed Boost", "Increase movement speed by 15%",
                 'passive', 'speed', 0.15)
        )

        # HP perks
        self.available_perks.append(
            Perk("Reinforced Hull", "+1 Max HP",
                 'passive', 'hp', 1)
        )

        # Weapon perks
        self.available_perks.append(
            Perk("Rapid Fire", "Decrease shoot cooldown by 25%",
                 'passive', 'fire_rate', 0.25)
        )

        self.available_perks.append(
            Perk("Piercing Shot", "Bullets pierce through 1 asteroid",
                 'passive', 'pierce', 1)
        )

        # More powerful perks for variety
        self.available_perks.append(
            Perk("Turbo Thrust", "Increase movement speed by 30%",
                 'passive', 'speed', 0.3)
        )

        self.available_perks.append(
            Perk("Twin Cannons", "Decrease shoot cooldown by 40%",
                 'passive', 'fire_rate', 0.4)
        )

    def get_random_perks(self, count=3):
        """Get a random selection of perks"""
        if len(self.available_perks) <= count:
            return self.available_perks

        return random.sample(self.available_perks, count)