import tkinter as tk
import time
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
IMG_DIR = "tomato.png"
CHECKMARK_TEXT = "✔"

reps = 0
checkmarks_list = []
timer = None

def modify_checks(task):
    if task == 'append': checkmarks_list.append(CHECKMARK_TEXT)
    else: checkmarks_list.clear()

    checkmark_text = "  ".join(checkmarks_list)
    check_text.config(text=checkmark_text)

# ---------------------------- TIMER RESET ------------------------------- # 
def reset():
    global reps
    reps = 0

    window.after_cancel(timer)

    modify_checks('clear')

    state_text.config(text='Timer', fg=GREEN)

    canvas.itemconfig(timer_text, text=f"00:00")

# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_countdown():
    global reps
    reps += 1

    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    if reps % 9 == 0 or reps % 2 == 0:
        if reps % 9 == 0:
            reps = 1
            modify_checks('clear')
        else:
            modify_checks('append')

    if reps % 8 == 0:
        state_text.config(text='Break', fg=RED)

        countdown(long_break_sec)
    elif reps % 2 == 0:
        state_text.config(text='Break', fg=PINK)

        countdown(short_break_sec)
    else:
        state_text.config(text='Work', fg=GREEN)

        countdown(work_sec)

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def countdown(sec):

    count_min = sec // 60
    count_sec = sec % 60

    if count_min < 10: count_min = f"0{count_min}"
    if count_sec < 10: count_sec = f"0{count_sec}"

    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")

    if sec >= 0:
        global timer
        timer = window.after(1000, countdown, sec - 1)
    else: start_countdown()

# ---------------------------- UI SETUP ------------------------------- #
window = tk.Tk()
window.title('Pomodoro')
window.config(padx=100, pady=50, bg=YELLOW)

state_text = tk.Label(text='Timer', pady=5, fg=GREEN, bg=YELLOW, font=(FONT_NAME, 35, 'bold'))
state_text.grid(column=1, row=0)

canvas = tk.Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = tk.PhotoImage(file=IMG_DIR)
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text='00:00', fill='white', font=(FONT_NAME, 35, 'bold'))
canvas.grid(column=1, row=1)

button_start = tk.Button(text="Start", command=start_countdown)
button_start.grid(column=0, row=2)

button_reset = tk.Button(text="Reset", command=reset)
button_reset.grid(column=2, row=2)

check_text = tk.Label(text='', pady=5, fg=GREEN, bg=YELLOW, font=(FONT_NAME, 15, 'bold'))
check_text.grid(column=1, row=3)


window.mainloop()