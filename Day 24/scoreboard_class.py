import turtle as t

FONT = ('Arial', 24, 'normal')
ALIGN = "center"

class Scoreboard(t.Turtle):

	def __init__(self):
		self.scores = []
		self.score = 0

		try:
			score_data = open("data.txt")
		except FileNotFoundError:
			score_data = open("data.txt", mode = 'w')
		else:
			for line in score_data:
				self.scores.append(int(line.strip()))

		score_data.close()

		super().__init__()
		self.setpos(0, 400)
		self.color("white")
		self.hideturtle()
		self.update_score()

	def update_score(self):
		self.clear()
		self.write(f"Score: {self.score} , Highscore: {max(self.scores + [self.score])}", align = "center", font=('Arial', 24, 'normal'))

	def gameover(self):
		self.setpos(0, 0)
		self.write("GAME OVER", align = "center", font=('Arial', 50, 'bold'))

	def add_score(self):
		self.score += 1

		self.update_score()

	def reset(self):
		with open("data.txt", mode = "a") as score_data:
			score_data.write(f"{self.score}\n")

		self.scores.append(self.score)

		self.score = 0
		self.update_score()
