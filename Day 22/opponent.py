from paddle import Paddle
import turtle as t
import random

STRETCH_WIDTH = 7

class Opponent(Paddle):

	def __init__(self, screen_dim):
		super().__init__(screen_dim)

		self.directions = ["Up", "Down"]
		self.direction = random.choice(self.directions)

	def create_body(self, screen_width):
		block = t.Turtle()
		block.penup()
		block.color("white")
		block.shape("square")
		block.setx(screen_width // 2 - 30)
		block.shapesize(stretch_wid = STRETCH_WIDTH, stretch_len = 1)
		return block

	def move(self):
		if self.direction == "Up":
			super().up()
		else:
			super().down()

		if super().is_on_edge(self.direction): self.change_direction()

	def change_direction(self):
		if self.direction == "Up": self.direction = "Down"
		else: self.direction = "Up"