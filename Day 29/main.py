import tkinter as tk
import tkinter.messagebox
import pyperclip
from password_generator import generate_password as password_generator

IMG_DIR = "logo.png"
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    password_input.delete(0, tk.END)
    password = password_generator()
    password_input.insert(0, password)

    pyperclip.copy(password)
# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_input.get()
    username = username_input.get()
    password = password_input.get()

    if not(website) or not(username) or not(password):
        tkinter.messagebox.showerror(title="Oops", message="Please don't leave any fields empty!")
    else:
        is_ok = tkinter.messagebox.askokcancel(title=website, message=f"These are the details entered:\nUsername/Email: {username}\nPassword: {password}\nIs it ok to save?")

        if is_ok:
            with open('data.txt', mode='a') as data_file:
                data_file.write(f"{website} | {username} | {password}\n")
                website_input.delete(0, tk.END)
                password_input.delete(0, tk.END)
# ---------------------------- UI SETUP ------------------------------- #
window = tk.Tk()
window.title('Password Manager')
window.config(padx=20, pady=20)

canvas = tk.Canvas(width=200, height=200)
password_img = tk.PhotoImage(file=IMG_DIR)
canvas.create_image(100, 100, image=password_img)
canvas.grid(column=1, row=0)

website_text = tk.Label(text='Website:')
website_text.grid(column=0, row=1)

username_text = tk.Label(text='Email/Username:')
username_text.grid(column=0, row=2)

password_text = tk.Label(text='Password:')
password_text.grid(column=0, row=3)

website_input = tk.Entry(width=35)
website_input.grid_configure(column=1, row=1, columnspan=2)

username_input = tk.Entry(width=35)
username_input.insert(0, 'danncarlo@gmail.com')
username_input.grid_configure(column=1, row=2, columnspan=2)

password_input = tk.Entry(width=21)
password_input.grid_configure(column=1, row=3)

generate_button = tk.Button(text='Generate Password', command=generate_password)
generate_button.grid_configure(column=2, row=3)

add_button = tk.Button(text='Add', width=35, command=save)
add_button.grid_configure(column=1, row=4, columnspan=2)


window.mainloop()