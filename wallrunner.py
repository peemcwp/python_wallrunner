import arcade
from models import World
import pyglet.gl as gl

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

GAME_RUNNING = 0
GAME_OVER = 1

class ModelSprite(arcade.Sprite):
    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop('model', None)

        super().__init__(*args, **kwargs)

    def sync_with_model(self):
        if self.model:
            self.set_position(self.model.x, self.model.y)

    def draw(self):
        self.sync_with_model()
        super().draw()

class WallRunnerGameWindow(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)

        arcade.set_background_color(arcade.color.AMAZON)

        self.current_state = GAME_RUNNING

        self.world = World(SCREEN_WIDTH, SCREEN_HEIGHT)

        self.man_sprite = ModelSprite('images/man.png',model=self.world.man)
        self.rip_sprite = ModelSprite('images/rip.png',model=self.world.man)
        self.heart_sprite = ModelSprite('images/heart.png',model=self.world.heart)

        self.rock_sprites = []
        for rock in self.world.rocks:
            self.rock_sprites.append(ModelSprite(
                'images/rock.png', model=rock))

    def animate(self, delta):
        self.world.animate(delta)
        if(self.world.hp <= 0):
            self.current_state = GAME_OVER

    def game_over_screen(self):
            self.rip_sprite.draw()
            arcade.draw_text("YOU DEAD!", self.width / 2 - 105, self.height / 2 + 100, arcade.color.BLACK, 30)
            arcade.draw_text("SURVIVE TIME : " + str(int(self.world.time)), self.width / 2 - 170, self.height / 2, arcade.color.BLACK, 30)

    def on_draw(self):
        arcade.start_render()
        if(self.current_state == GAME_RUNNING):
            self.heart_sprite.draw()
            for sprite in self.rock_sprites:
                sprite.draw()
            self.man_sprite.draw()
            

            arcade.draw_text("SURVIVE TIME : " + str(int(self.world.time)),self.width - 260, self.height - 40,arcade.color.BURNT_SIENNA, 20)
            arcade.draw_text("HP : " + str(self.world.hp),self.width - 570, self.height - 40,arcade.color.BURNT_SIENNA, 20)

        else:
            self.game_over_screen()


    def on_key_press(self, key, key_modifiers):
        self.world.on_key_press(key, key_modifiers)

if __name__ == '__main__':
    window = WallRunnerGameWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.set_window(window)
    arcade.run()
