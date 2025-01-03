import turtle as t
import turtle_functions

turtle = t.Turtle()
screen = t.Screen()

initial_x = -235

screen.screensize(500, 500)
screen.setup(600, 600)
screen.colormode(255)

turtle.penup()
turtle.speed("fastest")
turtle.setposition(-235, -235)

while turtle.pos()[1] < 235:
	turtle_functions.draw_in_line(turtle)
	turtle.setposition(initial_x, turtle.pos()[1] + 50)

turtle.hideturtle()

t.exitonclick()