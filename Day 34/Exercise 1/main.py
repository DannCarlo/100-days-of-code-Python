from question_model import Question
from data import question_data
from quiz_brain import QuizBrain
import requests
import html

requests_param = {
    "amount" : 10,
    "category" : 18,
    "type" : "boolean"
}

question_request = requests.get("https://opentdb.com/api.php", params=requests_param)
question_list = question_request.json()["results"]

question_bank = []

for question in question_list:
    question_text = html.unescape(question["question"])
    question_answer = question["correct_answer"]
    new_question = Question(question_text, question_answer)
    question_bank.append(new_question)

quiz = QuizBrain(question_bank)

while quiz.still_has_questions():
    quiz.next_question()

print("You've completed the quiz")
print(f"Your final score was: {quiz.score}/{quiz.question_number}")
