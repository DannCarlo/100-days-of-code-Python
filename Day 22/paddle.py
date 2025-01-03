import turtle as t

SCROLL_SPEED = 50
BLOCK_WIDTH = 20
STRETCH_WIDTH = 7

class Paddle:

	def __init__(self, screen_dim):
		self.screen_height = screen_dim[1]

		self.block = self.create_body(screen_dim[0])

		self.update_y_coord()


	def create_body(self, screen_width):
		block = t.Turtle()
		block.penup()
		block.color("white")
		block.shape("square")
		block.setx(-screen_width // 2 + 30)
		block.shapesize(stretch_wid = STRETCH_WIDTH, stretch_len = 1)
		return block

	def update_y_coord(self):
		self.y_coord = self.block.ycor()

	def edge_y_coord(self, direction):
		if direction == 'Up': return self.y_coord + BLOCK_WIDTH * self.block.shapesize()[0] / 2
		elif direction == 'Down': return self.y_coord - BLOCK_WIDTH * self.block.shapesize()[0] / 2

	def up(self):
		edge_y_coord = self.edge_y_coord('Up')

		if edge_y_coord + SCROLL_SPEED < self.screen_height // 2: 
			self.block.sety(self.y_coord + SCROLL_SPEED)
		elif edge_y_coord + SCROLL_SPEED > self.screen_height // 2: 
			self.block.sety(self.y_coord + (self.screen_height // 2 - edge_y_coord))

		self.update_y_coord()

	def down(self):
		edge_y_coord = self.edge_y_coord('Down')

		if edge_y_coord - SCROLL_SPEED > -self.screen_height // 2: 
			self.block.sety(self.y_coord - SCROLL_SPEED)
		elif edge_y_coord - SCROLL_SPEED < -self.screen_height // 2:
			self.block.sety(self.y_coord -(self.screen_height // 2 + edge_y_coord) )

		self.update_y_coord()

	def is_on_edge(self, direction):
		edge_coord = self.edge_y_coord(direction)

		screen_edge = self.screen_height // 2

		if direction == "Down": screen_edge = -screen_edge

		if edge_coord == screen_edge: return True
		else: return False	
