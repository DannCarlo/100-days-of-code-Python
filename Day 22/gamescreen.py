import turtle as t

class GameScreen:

	def __init__(self, screen_height):
		self.turtle = t.Turtle()
		self.divider_count = screen_height // (20 * 2)

		self.turtle.speed("fastest")
		self.turtle.penup()
		self.turtle.pencolor("white")
		self.turtle.setposition(0, -screen_height // 2)
		self.turtle.left(90)
		self.turtle.pensize(5)
		
		for _ in range(self.divider_count):
			self.turtle.pendown()
			self.turtle.forward(20)
			self.turtle.penup()
			self.turtle.forward(20)

		self.turtle.hideturtle()