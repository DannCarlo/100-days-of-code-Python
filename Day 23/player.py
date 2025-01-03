from turtle import Turtle

STARTING_POSITION = (0, -280)
MOVE_DISTANCE = 10
FINISH_LINE_Y = -250


class Player(Turtle):
    
    def __init__(self):
        super().__init__()
        self.shape("turtle")
        self.penup()
        self.left(90)
        self.reset()

    def up(self):
        self.sety(self.ycor() + MOVE_DISTANCE)

    def reset(self):
        self.setpos(STARTING_POSITION)
