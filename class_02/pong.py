from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
'''
A note on the imports...
Sometimes PyCharm won't recognize the Property imports. To fix this, add `import kivy.properties` and wait a moment. 
These properties use the Cython system, so PyCharm needs this extra nudge to parse and understand the C-based 
properties. If this doesn't make much sense, don't worry about it. Just know how to fix it when it happens.

We'll cover what each of these things we're importing does in the code below. Don't worry about it for now :)
'''


class PongApp(App):
    """
    As explained in the quickstart project, this is our main class that runs our Kivy app.
    In this project, we're also introducing the concept of kv files. Kv files are specific to Kivy and are used to 
    define how things will appear visually. This separates the visual representations of things (in kv files) 
    from their behaviors (in Python files). 
    For kv files, the name of the file must match the name of the app class before the word "App". Since our class
    here is named PongApp, our kv file should be named pong.kv
    """

    def build(self):
        # Also as mentioned in the quickstart project, this is the method run by our Kivy app as soon as it starts
        game = PongGame()
        # This creates the main game widget, which we'll cover below
        game.serve_ball()
        # In our main game widget, we define a serve_ball method, which we use to start the game
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        '''
        This sets up our "game loop". Games run by using an infinite loop to continuously update game objects and keep
        the game running. Usually, the function run by the loop is called "update", and we maintain that convention 
        here, too. On our main game widget, we defined an update function that we'll use here.
        Clock.schedule_interval is a Kivy method that allows us to setup a function to be called on a repeating 
        schedule until the app is closed. We'll use this to setup our game loop.
        The second parameter, `1.0 / 60.0`, sets up our game loop to run 60 times per second. 
        In reality, video is just still images changing really fast. When you see movies, maybe you've noticed many
        things say "motion pictures". Movies are just tons of individual photos changing really quickly. The images
        are swapped so quickly that your eyes see it as continuous movement rather than images being swapped out.
        Movies actually run at 24 images every second. We call these images "frames" and say that moves run at
        24 frames per second, or 24 fps. Most computer videos and games run at either 30 fps or 60 fps. We'll run ours
        at 60 fps because we're cool like that. Doing 1.0 / 60.0 will get us the amount of time that one second 
        divided into 60 parts gives us, and therefore, how much time to wait between running update each time.
        '''
        return game
        # Everything in our game is inside the PongGame widget, so we return that widget for Kivy to display


class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)

    def serve_ball(self, vel=(4, 0)):
        self.ball.center = self.center
        self.ball.velocity = vel

    def update(self, dt):
        self.ball.move()

        # bounce of paddles
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

        # bounce ball off bottom or top
        if (self.ball.y < self.y) or (self.ball.top > self.top):
            self.ball.velocity_y *= -1

        # went of to a side to score point?
        if self.ball.x < self.x:
            self.player2.score += 1
            self.serve_ball(vel=(4, 0))
        if self.ball.x > self.width:
            self.player1.score += 1
            self.serve_ball(vel=(-4, 0))

    def on_touch_move(self, touch):
        if touch.x < self.width / 3:
            self.player1.center_y = touch.y
        if touch.x > self.width - self.width / 3:
            self.player2.center_y = touch.y


class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class PongPaddle(Widget):
    """
    PongPaddle represents the paddles controlled by the players in the game. Here, they inherit from Widget because
    they are visual elements in the game. We'll draw their visual representation in the kv file.
    """
    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1
            ball.velocity = vel.x, vel.y + offset


if __name__ == '__main__':
    PongApp().run()
