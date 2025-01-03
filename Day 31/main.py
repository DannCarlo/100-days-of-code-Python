import tkinter as tk
from tkinter import messagebox
import pandas as pd
import random

BACKGROUND_COLOR = "#B1DDC6"
CANVAS_IMG_DIR_FRONT = "images/card_front.png"
CANVAS_IMG_DIR_BACK = "images/card_back.png"
WRONG_BUTTON_DIR = "images/wrong.png"
RIGHT_BUTTON_DIR = "images/right.png"

words_already_shown = []

show_english_timer = None
countdown_timer = None

try:
    words_dataframe = pd.read_csv("data/to_learn.csv")
except FileNotFoundError:
    words_dataframe = pd.read_csv("data/french_words.csv")

words_dataframe_len = words_dataframe.shape[0]

language_to_learn = words_dataframe.keys()[0]

window = tk.Tk()
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

window.title("Duolingo")

card_front_img = tk.PhotoImage(file=CANVAS_IMG_DIR_FRONT)
card_back_img = tk.PhotoImage(file=CANVAS_IMG_DIR_BACK)

right_button_img = tk.PhotoImage(file=RIGHT_BUTTON_DIR)
wrong_button_img = tk.PhotoImage(file=WRONG_BUTTON_DIR)

# ---------------------------- BUTTON FUNCTION ------------------------------- #
def next_word():
    save()
    global show_english_timer, countdown_timer

    if show_english_timer: window.after_cancel(show_english_timer)
    if countdown_timer: window.after_cancel(countdown_timer)

    random_word_lang = None

    if len(words_already_shown) >= words_dataframe_len:
        tk.messagebox.showinfo(title="Congratulations!", message="You've already learned all words.")
    else:
        while random_word_lang in words_already_shown or random_word_lang is None:
            random_word_obj = words_dataframe.iloc[random.randint(0, words_dataframe_len - 1)]
            # random_word_lang is the word to be learned, depending on language
            random_word_eng, random_word_lang = random_word_obj["English"], random_word_obj[language_to_learn]

        words_already_shown.append(random_word_lang)

        show_original_word_func(language_to_learn, random_word_lang)

        show_english_timer = window.after(3000, show_translation_word_func, random_word_eng)

def save():
    words_already_shown_index = []

    for word in words_already_shown:
        words_already_shown_index.append(words_dataframe[words_dataframe[language_to_learn] == word].index[0])

    to_learn_dataframe = words_dataframe.drop(words_already_shown_index)

    to_learn_dataframe.to_csv("data/to_learn.csv", index=False)

def show_original_word_func(language, word):
    timer_countdown(3)
    canvas.itemconfig(canvas_card_img, image=card_front_img)
    canvas.itemconfig(language_text, text=language)
    canvas.itemconfig(word_text, text=word)

def show_translation_word_func(english_word):
    canvas.itemconfig(canvas_card_img, image=card_back_img)
    canvas.itemconfig(language_text, text="English")
    canvas.itemconfig(word_text, text=english_word)

def timer_countdown(sec):
    global countdown_timer

    canvas.itemconfig(timer_text, text=sec)

    sec -= 1

    if sec >= 0: countdown_timer = window.after(1000, timer_countdown, sec)
    else: canvas.itemconfig(timer_text, text="")
    return

# ---------------------------- CANVAS SETUP ------------------------------- #
canvas = tk.Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
canvas_card_img = canvas.create_image(400, 526/2, image=card_front_img)
canvas.grid_configure(column=0, row=0, columnspan=2)

language_text = canvas.create_text(400, 150, text="Language", font=("Arial", 40, "italic"))
timer_text = canvas.create_text(700, 75, text="3", font=("Arial", 50, "bold"))
word_text = canvas.create_text(400, 263, text="Word", font=("Arial", 60, "bold"))


# ---------------------------- BUTTONS SETUP ------------------------------- #
button_wrong = tk.Button(image=wrong_button_img, highlightthickness=0, bg=BACKGROUND_COLOR, borderwidth=0, command=next_word)
button_wrong.grid_configure(column=0, row=1)

right = tk.Button(image=right_button_img, highlightthickness=0, bg=BACKGROUND_COLOR, borderwidth=0, command=next_word)
right.grid_configure(column=1, row=1)

next_word()


window.mainloop()
