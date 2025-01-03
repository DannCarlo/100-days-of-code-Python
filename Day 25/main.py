import turtle as t
from state_text import Text
import pandas

data = pandas.read_csv('50_states.csv')

screen = t.Screen()
turtle = t.Turtle()
image = "blank_states_img.gif"

answered = []

score = 0

screen.addshape(image)
turtle.shape(image)

while True:
    if score == 0:
        answer_state = screen.textinput(title = "Guess The State", prompt = "What's another state's name?")
    else:
        answer_state = screen.textinput(title = f"{score}/50 Guess The State", prompt = "What's another state's name?")

    answer_state = answer_state.title()

    if answer_state == 'Exit': break

    if len(data[data['state'] == answer_state]) != 0 and answer_state not in answered:
        answered.append(answer_state)

        x_coord, y_coord = (data[data['state'] == answer_state]['x'].to_list()[0],
                            data[data['state'] == answer_state]['y'].to_list()[0])

        state_text = Text(x_coord, y_coord, answer_state)

        score += 1

    if score == 50: break

answered_panda_index = []

for i in answered:
    answered_panda_index.append(data[data['state'] == i].index[0])

print(answered_panda_index)

data = data.drop(answered_panda_index)

data.to_csv('states_to_learn.csv', index = False)


