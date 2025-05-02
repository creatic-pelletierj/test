import arcade
import random
from attack_animation import AttackAnimation, AttackType
from game_state import GameState

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Roche Papier Ciseaux"

CHOICES = ["pierre", "papier", "ciseaux"]

CHOICE_TO_ATTACK_TYPE = {
    "pierre": AttackType.ROCK,
    "papier": AttackType.PAPER,
    "ciseaux": AttackType.SCISSORS,
}

class GameView(arcade.View):
    def __init__(self):
        super().__init__()

        self.hide_choices = None
        self.player_choice = None
        self.computer_choice = None
        self.result = ""

        self.player_score = 0
        self.computer_score = 0

        self.game_state = GameState.NOT_STARTED

        self.instruction_text = arcade.Text(
            "Appuyez sur ESPACE pour commencer la partie",
            150, 300, arcade.color.BLACK, 24, bold=True
        )
        self.instruction_text2 = arcade.Text(
            "Appuyez sur le choix voulu.",
            200, 400, arcade.color.BLACK, 24, bold=True
        )
        self.continue_text = arcade.Text(
            "Appuyez sur ESPACE pour continuer",
            220, 200, arcade.color.BLACK, 20
        )
        self.score_text = None
        self.choice_text = None
        self.computer_text = None
        self.result_text = None
        self.game_over_text = None

        self.player_attack_sprite = None
        self.computer_attack_sprite = None
        self.attack_sprites = arcade.SpriteList()

        self.all_attacks_sprites = arcade.SpriteList()
        self.create_all_attacks()

        self.player_face_sprite = arcade.Sprite("assets/faceBeard.png", scale=0.2)
        self.player_face_sprite.center_x = 200
        self.player_face_sprite.center_y = 320
        self.player_face_sprite_list = arcade.SpriteList()
        self.player_face_sprite_list.append(self.player_face_sprite)

        self.computer_face_sprite = arcade.Sprite("assets/compy.png", scale=1)
        self.computer_face_sprite.center_x = 600
        self.computer_face_sprite.center_y = 320
        self.computer_face_sprite_list = arcade.SpriteList()
        self.computer_face_sprite_list.append(self.computer_face_sprite)

    def create_all_attacks(self):
        positions = [(200, 100), (400, 100), (600, 100)]
        self.all_attacks_sprites = arcade.SpriteList()
        for attack_type, pos in zip([AttackType.ROCK, AttackType.PAPER, AttackType.SCISSORS], positions):
            sprite = AttackAnimation(attack_type, center_x=pos[0], center_y=pos[1])
            sprite.alpha = 255
            self.all_attacks_sprites.append(sprite)

    def setup(self):
        self.player_choice = None
        self.computer_choice = None
        self.result = ""
        self.player_score = 0
        self.computer_score = 0
        self.game_state = GameState.NOT_STARTED

        self.choice_text = None
        self.computer_text = None
        self.result_text = None
        self.game_over_text = None

        self.hide_choices = False

        for sprite in self.all_attacks_sprites:
            sprite.alpha = 255

        self.attack_sprites.clear()
        self.player_attack_sprite = None
        self.computer_attack_sprite = None

        self.update_score_text()

    def update_score_text(self):
        self.score_text = arcade.Text(
            f"Score - Vous: {self.player_score}  Ordinateur: {self.computer_score}",
            50, 500, arcade.color.BLACK, 20
        )

    def on_draw(self):
        self.clear()

        if self.game_state == GameState.NOT_STARTED:
            self.instruction_text.draw()
        else:
            self.score_text.draw()

            if self.game_state == GameState.ROUND_ACTIVE:
                if not self.hide_choices:
                    self.all_attacks_sprites.draw()
                    self.instruction_text2.draw()

                if self.player_choice:
                    self.choice_text.draw()
                    self.computer_text.draw()
                    self.result_text.draw()
                    self.attack_sprites.draw()


            elif self.game_state == GameState.ROUND_DONE:
                if self.player_choice:
                    self.choice_text.draw()
                    self.computer_text.draw()
                    self.result_text.draw()
                    self.attack_sprites.draw()
                    self.player_face_sprite_list.draw()
                    self.computer_face_sprite_list.draw()

                self.continue_text.draw()

            elif self.game_state == GameState.GAME_OVER:
                if self.game_over_text:
                    self.game_over_text.draw()
                self.continue_text.draw()

    def on_key_press(self, key, modifiers):
        if self.game_state == GameState.NOT_STARTED and key == arcade.key.SPACE:
            self.start_new_game()
        elif self.game_state == GameState.ROUND_DONE and key == arcade.key.SPACE:
            self.start_new_round()
        elif self.game_state == GameState.GAME_OVER and key == arcade.key.SPACE:
            self.start_new_game()

    def on_mouse_press(self, x, y, button, modifiers):
        if self.game_state != GameState.ROUND_ACTIVE or self.hide_choices:
            return

        clicked_sprites = arcade.get_sprites_at_point((x, y), self.all_attacks_sprites)
        if not clicked_sprites:
            return

        clicked_sprite = clicked_sprites[0]

        if clicked_sprite.attack_type == AttackType.ROCK:
            self.player_choice = "pierre"
        elif clicked_sprite.attack_type == AttackType.PAPER:
            self.player_choice = "papier"
        elif clicked_sprite.attack_type == AttackType.SCISSORS:
            self.player_choice = "ciseaux"
        else:
            return

        self.computer_choice = random.choice(CHOICES)
        self.result = self.get_result()

        if self.result == "Gagné !":
            self.player_score += 1
        elif self.result == "Perdu.":
            self.computer_score += 1

        self.update_score_text()

        if self.player_attack_sprite and self.player_attack_sprite in self.attack_sprites:
            self.attack_sprites.remove(self.player_attack_sprite)
        if self.computer_attack_sprite and self.computer_attack_sprite in self.attack_sprites:
            self.attack_sprites.remove(self.computer_attack_sprite)

        self.player_attack_sprite = AttackAnimation(
            CHOICE_TO_ATTACK_TYPE[self.player_choice], center_x=200, center_y=250
        )
        self.computer_attack_sprite = AttackAnimation(
            CHOICE_TO_ATTACK_TYPE[self.computer_choice], center_x=600, center_y=250
        )

        self.attack_sprites.append(self.player_attack_sprite)
        self.attack_sprites.append(self.computer_attack_sprite)

        self.choice_text = arcade.Text(
            f"Vous avez choisi: {self.player_choice}", 1000, 400, arcade.color.BLUE, 20
        )
        self.computer_text = arcade.Text(
            f"L'ordinateur a choisi: {self.computer_choice}", 1000, 350, arcade.color.RED, 20
        )
        self.result_text = arcade.Text(
            f"Résultat: {self.result}", 100, 450, arcade.color.BLACK, 24
        )

        self.hide_choices = True
        for sprite in self.all_attacks_sprites:
            sprite.alpha = 0

        self.game_state = GameState.ROUND_DONE

    def on_update(self, delta_time):
        self.attack_sprites.update_animation(delta_time)
        self.all_attacks_sprites.update_animation(delta_time)

    def start_new_game(self):
        self.player_score = 0
        self.computer_score = 0
        self.update_score_text()

        self.player_choice = None
        self.computer_choice = None
        self.result = ""
        self.choice_text = None
        self.computer_text = None
        self.result_text = None
        self.game_over_text = None

        self.attack_sprites.clear()
        self.player_attack_sprite = None
        self.computer_attack_sprite = None

        for sprite in self.all_attacks_sprites:
            sprite.alpha = 255

        self.hide_choices = False
        self.game_state = GameState.ROUND_ACTIVE

    def start_new_round(self):
        # Vérifier si la partie est terminée
        if self.player_score >= 3 or self.computer_score >= 3:
            self.game_state = GameState.GAME_OVER
            if self.player_score > self.computer_score:
                message = "Vous avez gagné la partie !"
            else:
                message = "L'ordinateur a gagné la partie."
            self.game_over_text = arcade.Text(
                message, 170, 150, arcade.color.DARK_RED, 30, bold=True
            )
            for sprite in self.all_attacks_sprites:
                sprite.alpha = 0
            return

        self.player_choice = None
        self.computer_choice = None
        self.result = ""
        self.choice_text = None
        self.computer_text = None
        self.result_text = None

        self.attack_sprites.clear()
        self.player_attack_sprite = None
        self.computer_attack_sprite = None

        for sprite in self.all_attacks_sprites:
            sprite.alpha = 255

        self.hide_choices = False
        self.game_state = GameState.ROUND_ACTIVE

    def get_result(self):
        if self.player_choice == self.computer_choice:
            return "Égalité"
        elif (self.player_choice == "pierre" and self.computer_choice == "ciseaux") or \
             (self.player_choice == "papier" and self.computer_choice == "pierre") or \
             (self.player_choice == "ciseaux" and self.computer_choice == "papier"):
            return "Gagné !"
        else:
            return "Perdu."

def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.set_background_color(arcade.color.BROWN_NOSE)
    game_view = GameView()
    game_view.setup()
    window.show_view(game_view)
    arcade.run()

if __name__ == "__main__":
    main()
