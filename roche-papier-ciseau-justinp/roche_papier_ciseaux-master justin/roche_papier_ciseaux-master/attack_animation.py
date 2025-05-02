import arcade
from enum import Enum

class AttackType(Enum):
    ROCK = 0
    PAPER = 1
    SCISSORS = 2

class AttackAnimation(arcade.Sprite):
    ATTACK_SCALE = 0.5
    ANIMATION_SPEED = 5.0  # images par seconde

    def __init__(self, attack_type: AttackType, center_x: float = 0, center_y: float = 0):
        super().__init__()

        self.attack_type = attack_type

        if attack_type == AttackType.ROCK:
            self.textures = [
                arcade.load_texture("assets/srock.png"),
                arcade.load_texture("assets/srock-attack.png")
            ]
        elif attack_type == AttackType.PAPER:
            self.textures = [
                arcade.load_texture("assets/spaper.png"),
                arcade.load_texture("assets/spaper-attack.png")
            ]
        else:
            self.textures = [
                arcade.load_texture("assets/scissors.png"),
                arcade.load_texture("assets/scissors-close.png")
            ]

        self.scale = self.ATTACK_SCALE
        self.current_texture = 0
        self.texture = self.textures[self.current_texture]
        self.animation_update_time = 1.0 / self.ANIMATION_SPEED
        self.time_since_last_swap = 0.0

        self.center_x = center_x
        self.center_y = center_y

    def update_animation(self, delta_time: float = 1/60):
        self.time_since_last_swap += delta_time
        if self.time_since_last_swap >= self.animation_update_time:
            self.time_since_last_swap = 0.0
            self.current_texture = (self.current_texture + 1) % len(self.textures)
            self.texture = self.textures[self.current_texture]
