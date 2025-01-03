from turtle import Turtle

FONT = ("Courier", 24, "normal")

class Scoreboard:
    
    def __init__(self, screen_dim):
        self.screen_width, self.screen_height = screen_dim[0], screen_dim[1]

        self.level = 0

        self.score_text = Turtle()
        self.score_text.setpos(-self.screen_width / 2, self.screen_height / 2 + 80)
        self.score_text.hideturtle()
        self.update_level_text()

    def update_level_text(self):
        self.score_text.clear()
        self.score_text.write(f"Level: {self.level}", align = "center", font=FONT)

    def add_level(self):
        self.level += 1

    def game_over(self):
        text = Turtle()
        text.hideturtle()
        text.setpos(0, 0)
        text.write("GAME OVER", align = "center", font=FONT)

    def reset(self):
        self.score_text.setpos(-self.screen_width / 2, self.screen_height / 2 + 80)
        self.score_text.hideturtle()
        self.update_level_text()
