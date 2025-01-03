import turtle as t
import random

tim = t.Turtle()

########### Challenge 4 - Random Walk ########
colours = ["CornflowerBlue", "DarkOrchid", "IndianRed", "DeepSkyBlue", "LightSeaGreen", "wheat", "SlateGray", "SeaGreen"]
directions = [0, 90, 180, 270]

for _ in range(200):
	tim.pensize(random.randint(10, 12))
	tim.forward(30)
	tim.setheading(random.choice(directions))
	tim.color(random.choice(colours))