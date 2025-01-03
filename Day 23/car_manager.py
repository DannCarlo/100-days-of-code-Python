from turtle import Turtle
from scoreboard import Scoreboard
import random

COLORS = ["red", "orange", "yellow", "green", "blue", "purple"]
STARTING_MOVE_DISTANCE = 5
MOVE_INCREMENT = 20


class CarManager:
    
    def __init__(self):
        self.cars = []

    def generate_cars(self):
        count = random.randint(1, 2)
        for _ in range(count):
            car = Turtle()
            car.color(random.choice(COLORS))
            car.penup()
            car.shape('square')
            car.shapesize(stretch_wid = 1, stretch_len = 2)
            car.setheading(180)
            car.setpos(320, random.randint(-260, 260))
            self.cars.append(car)

    def move(self, level):
        for car in self.cars:
            car.setx(car.xcor() - (STARTING_MOVE_DISTANCE + MOVE_INCREMENT * level))

    def reset(self):
        for car in self.cars:
            car.penup()
            car.setx(9000)

    def is_player_hit(self, player):
        for car in self.cars:
            if player.distance(car) < 30 and car.xcor() - 20 < player.xcor() + 10: 
                if car.ycor() - 19 < player.ycor() < car.ycor() + 19:
                    return True
        return False

