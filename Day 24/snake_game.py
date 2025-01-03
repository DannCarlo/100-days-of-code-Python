from snake_class import Snake
from food_class import Food
from scoreboard_class import Scoreboard
import turtle as t
import time


screen = t.Screen()

screen.title("Snake Game 101!")
screen.bgcolor("black")
screen.screensize(800, 800)
screen.setup(900, 900)
screen.tracer(0)

snake = Snake()
food = Food()
scoreboard = Scoreboard()

screen.listen()
screen.onkey(snake.up, "Up")
screen.onkey(snake.down, "Down")
screen.onkey(snake.left, "Left")
screen.onkey(snake.right, "Right")

game_is_on = True

while game_is_on:
	screen.update()
	time.sleep(.05)

	snake.move()

	if snake.head.xcor() > 390 or snake.head.xcor() < -390 or snake.head.ycor() > 390 or snake.head.ycor() < -390 or snake.hit_tail():
		snake.reset()
		scoreboard.reset()


	if snake.head.distance(food) < 15:
		scoreboard.add_score()
		snake.extend()
		food.refresh()


screen.exitonclick()