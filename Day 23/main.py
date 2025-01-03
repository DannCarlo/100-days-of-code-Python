import time
from turtle import Screen
from player import Player, FINISH_LINE_Y
from car_manager import CarManager
from scoreboard import Scoreboard
import random

screen = Screen()
screen.setup(width=600, height=600)
screen.tracer(0)

print(screen.screensize())

player = Player()
cars = CarManager()
scoreboard = Scoreboard(screen.screensize())

level = scoreboard.level

screen.listen()
screen.onkey(player.up, "Up")

game_is_on = True

while game_is_on:
    time.sleep(0.1)
    screen.update()

    if random.choice([True, False, False, False]):
        cars.generate_cars()
    
    cars.move(level)

    if player.ycor() >= FINISH_LINE_Y:
        screen.reset()
        scoreboard.add_level()
        level = scoreboard.level
        cars.reset()
        player.reset()
        scoreboard.reset()

    if cars.is_player_hit(player):
        screen.update()
        scoreboard.game_over()
        game_is_on = False

screen.exitonclick()