import turtle as t

FONT = ('Arial', 24, 'normal')
ALIGN = "center"

class Scoreboard(t.Turtle):

	def __init__(self):
		self.score = 0

		super().__init__()
		self.setpos(0, 400)
		self.color("white")
		self.hideturtle()
		self.update_score()

	def update_score(self):
		self.clear()
		self.write(f"Score: {self.score}", align = "center", font=('Arial', 24, 'normal'))

	def gameover(self):
		self.setpos(0, 0)
		self.write("GAME OVER", align = "center", font=('Arial', 50, 'bold'))

	def add_score(self):
		self.score += 1

		self.update_score()
