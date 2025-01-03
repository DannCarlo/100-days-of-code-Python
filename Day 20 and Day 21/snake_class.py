import turtle as t

MOVE_DISTANCE = 20

class Snake:

	def __init__(self):
		self.length = 3
		self.body = []
		self.direction = "Right"

		self.create_snake()

		self.head = self.body[0]
		self.tail = self.body[-1]


	def create_snake(self):
		for i in range(0, self.length):
			self.increase_length([i * -MOVE_DISTANCE, 0])

	def move(self):
		for i in range(len(self.body) - 1, 0, -1):
			new_x_coord, new_y_coord = self.body[i - 1].position()[0], self.body[i - 1].position()[1]
			self.body[i].setposition(new_x_coord, new_y_coord)

		head_x_coord, head_y_coord = self.head.position()[0], self.head.position()[1]

		if self.direction == "Up":
			self.head.setposition(head_x_coord, head_y_coord + MOVE_DISTANCE)
		elif self.direction == "Down":
			self.head.setposition(head_x_coord, head_y_coord - MOVE_DISTANCE)
		elif self.direction == "Left":
			self.head.setposition(head_x_coord - MOVE_DISTANCE, head_y_coord)
		elif self.direction == "Right":
			self.head.setposition(head_x_coord + MOVE_DISTANCE, head_y_coord)

	def up(self):
		if self.direction != "Down": self.direction = "Up"

	def down(self):
		if self.direction != "Up": self.direction = "Down"

	def left(self):
		if self.direction != "Right": self.direction = "Left"

	def right(self):
		if self.direction != "Left": self.direction = "Right"

	def hit_tail(self):
		for i in range(1, len(self.body)):
			if self.head.distance(self.body[i]) < 10:
				return True
		return False

	def extend(self):
		self.increase_length(self.tail.pos())

	def increase_length(self, position):
		new_square = t.Turtle(shape = "square")
		new_square.color("white")
		new_square.penup()
		new_square.setposition(position)
		self.body.append(new_square)

		self.tail = new_square

