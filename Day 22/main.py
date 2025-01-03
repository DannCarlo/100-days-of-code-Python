import turtle as t
from gamescreen import GameScreen
from paddle import Paddle, BLOCK_WIDTH, STRETCH_WIDTH
from opponent import Opponent
from ball import Ball
from scoreboard import Scoreboard
import time

screen = t.Screen()

BLOCK_WIDTH += 5

screen.title("Snake Game 101!")
screen.bgcolor("black")
screen.screensize(1500, 800)
screen.setup(1600, 900)
screen.tracer(0)

screen_width, screen_height = screen.screensize()[0], screen.screensize()[1]

gamescreen = GameScreen(screen_height)
user = Paddle(screen.screensize())
opponent = Opponent(screen.screensize())
ball = Ball()
scoreboard = Scoreboard(screen_height)

screen.listen()
screen.onkey(user.up, "Up")
screen.onkey(user.down, "Down")

bounce_wall = screen_height // 2
score_wall = screen_width // 2

game_is_on = True

while game_is_on:
	screen.update()
	time.sleep(.025)

	opponent.move()
	ball.move()

	if abs(ball.ycor()) == bounce_wall: ball.y_direction *= -1

	if ((ball.distance(user.block) <= (STRETCH_WIDTH / 2 * BLOCK_WIDTH) and ball.xcor() <= user.block.xcor() + BLOCK_WIDTH // 2) or
		(ball.distance(opponent.block) <= (STRETCH_WIDTH / 2 * BLOCK_WIDTH) and ball.xcor() >= opponent.block.xcor() - BLOCK_WIDTH // 2)): 
		ball.x_direction *= -1

	if ball.xcor() > score_wall:
		ball.refresh()
		scoreboard.add_user_score()

	if ball.xcor() < -score_wall:
		ball.refresh()
		scoreboard.add_opponent_score()


screen.exitonclick()
