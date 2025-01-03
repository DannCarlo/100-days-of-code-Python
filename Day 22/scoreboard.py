import turtle as t

class Scoreboard():

	def __init__(self, screen_height):
		self.user_score, self.opponent_score = 0, 0

		self.left_board = t.Turtle()
		self.left_board.setpos(-50, screen_height // 2 - 100)
		self.left_board.color("white")
		self.left_board.hideturtle()

		self.right_board = t.Turtle()
		self.right_board.setpos(50, screen_height // 2 - 100)
		self.right_board.color("white")
		self.right_board.hideturtle()

		self.update_score()

	def update_score(self):
		self.left_board.clear()
		self.left_board.write(f"{self.user_score}", align = "center", font=('Arial', 75, 'normal'))

		self.right_board.clear()
		self.right_board.write(f"{self.opponent_score}", align = "center", font=('Arial', 75, 'normal'))

	def add_user_score(self):
		self.user_score += 1

		self.update_score()

	def add_opponent_score(self):
		self.opponent_score += 1

		self.update_score()