from question_model import Question
from quiz_brain import Quiz
from data import question_data

question_list = []

for i in range(0, len(question_data)):
	question_list.append(Question(question_data[i]["question"], question_data[i]["answer"]))

quiz = Quiz(question_list)

while quiz.still_has_questions():
	quiz.next_question()

print(f"Your total score is {quiz.correct_answers}")

