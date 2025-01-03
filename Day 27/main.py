import tkinter as tk

def convert():
    km = round(float(entry.get()) * 1.60934, 2)
    answer.config(text=km)

window = tk.Tk()
window.title("Mile to km converter")

label1 = tk.Label(text="is equal to")
label1.grid(column=0, row=1, padx=10, pady=10)

label2 = tk.Label(text="Miles")
label2.grid(column=2, row=1, padx=10, pady=10)

label3 = tk.Label(text="Km")
label3.grid(column=2, row=0, padx=10, pady=10)

answer = tk.Label(text="0")
answer.grid(column=1, row=1, padx=10, pady=10)

#Text Input
entry = tk.Entry(width=10)
entry.insert(1, string="0")
entry.grid(column=1, row=0, padx=10, pady=10)

button = tk.Button(text="Calculate", command=convert)
button.grid(column=1, row=2, padx=10, pady=10)

window.mainloop()