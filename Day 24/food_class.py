import turtle as t
import random

class Food(t.Turtle):

	def __init__(self):
		super().__init__()
		self.shape("circle")
		self.penup()
		self.shapesize(stretch_len = .5, stretch_wid = .5)
		self.color("blue")
		self.refresh()

	def refresh(self):
		self.setpos(random.randint(-395, 395), random.randint(-395, 395))
		