import turtle as t
import random

tim = t.Turtle()

########### Challenge 4 - Random Walk ########
colours = ["CornflowerBlue", "DarkOrchid", "IndianRed", "DeepSkyBlue", "LightSeaGreen", "wheat", "SlateGray", "SeaGreen"]
directions = [0, 90, 180, 270]

tim.speed("fastest")

for i in range(0, 361, 15):
	tim.color(random.choice(colours))
	tim.pensize(random.randint(3, 8))
	tim.setheading(i)
	tim.circle(50)