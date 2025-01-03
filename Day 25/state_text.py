import turtle as t

class Text(t.Turtle):

    def __init__(self, x_coord, y_coord, answer_state):
        super().__init__()
        super().speed('fastest')
        super().hideturtle()
        super().penup()
        super().setpos(x_coord, y_coord)
        super().write(answer_state)