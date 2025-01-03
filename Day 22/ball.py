import turtle as t
import random

BALL_SPEED = 20

class Ball(t.Turtle):

	def __init__(self):
		super().__init__()

		self.setpos(0, 0)
		self.color('red')
		self.shape('circle')
		self.penup()

		self.x_direction = random.choice([BALL_SPEED, -BALL_SPEED])
		self.y_direction = random.choice([BALL_SPEED, -BALL_SPEED])

	def move(self):
		self.setpos(self.xcor() + self.x_direction, self.ycor() + self.y_direction)

	def refresh(self):
		self.setpos(0, 0)
		self.x_direction = random.choice([BALL_SPEED, -BALL_SPEED])
		self.y_direction = random.choice([BALL_SPEED, -BALL_SPEED])


