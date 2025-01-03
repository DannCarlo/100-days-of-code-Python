import tkinter as tk
from quiz_brain import QuizBrain
from tkinter import messagebox

THEME_COLOR = "#375362"
CANVAS_WIDTH = 300
CANVAS_HEIGHT = 250
FONT = ("Arial", 20, "italic")

TRUE_BUTTON_IMG_DIR = "images/true.png"
FALSE_BUTTON_IMG_DIR = "images/false.png"

class QuizInterface:
    def __init__(self, quiz_brain: QuizBrain):
        self.quiz_brain = quiz_brain

        self.window = tk.Tk()
        self.window.title("Quizzler")
        self.window.config(padx=20, pady=20, bg=THEME_COLOR)

        self.score_label = tk.Label(text="Score: 0", bg=THEME_COLOR, fg="white")
        self.score_label.grid_configure(column=1, row=0)

        self.canvas = tk.Canvas(width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
        self.canvas.grid_configure(column=0, row=1, columnspan=2, pady=20)
        self.question_text = self.canvas.create_text(CANVAS_WIDTH/2, CANVAS_HEIGHT/2, width=CANVAS_WIDTH-10, text="", font=FONT)
        self.get_next_question()

        self.true_button_img = tk.PhotoImage(file=TRUE_BUTTON_IMG_DIR)
        self.false_button_img = tk.PhotoImage(file=FALSE_BUTTON_IMG_DIR)

        self.true_button = tk.Button(image=self.true_button_img, border=0,
                                     highlightthickness=0, command=self.clicked_true_button)
        self.true_button.grid_configure(column=0, row=2)

        self.false_button = tk.Button(image=self.false_button_img, border=0,
                                      highlightthickness=0, command=self.clicked_false_button)
        self.false_button.grid_configure(column=1, row=2)

        self.window.mainloop()

    def get_next_question(self):
        if not(self.still_has_questions()):
            if self.quiz_brain.score > 0:
                messagebox.showinfo(title="Getting Questions...",
                                    message="Please wait while we are getting more questions.")
            self.quiz_brain.get_questions_online()

        next_question = self.quiz_brain.next_question()
        self.canvas.itemconfigure(self.question_text, text=next_question)

    def clicked_true_button(self):
        self.check_answer("True")

    def clicked_false_button(self):
        self.check_answer("False")

    def check_answer(self, answer):
        is_correct = self.quiz_brain.check_answer(answer)
        if is_correct:
            self.quiz_brain.add_score()
            self.score_label.configure(text=f"Score: {self.quiz_brain.get_score()}")

        self.get_next_question()

    def still_has_questions(self):
        return self.quiz_brain.still_has_questions()