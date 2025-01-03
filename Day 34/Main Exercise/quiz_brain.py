from question_model import Question
import requests

NEW_QUESTION_COUNT = 10

REQUEST_PARAMETER = {
    "amount" : 10,
    "category" : 23,
    "type" : "boolean"
}

class QuizBrain:

    def __init__(self):
        self.question_number = 0
        self.score = 0
        self.question_list = []
        self.current_question = None

        self.get_questions_online()

    def get_questions_online(self):
        question_request = requests.get("https://opentdb.com/api.php", params=REQUEST_PARAMETER)
        question_list = question_request.json()["results"]

        question_bank = []

        for question in question_list:
            question_text = question["question"]
            question_answer = question["correct_answer"]
            new_question = Question(question_text, question_answer)
            question_bank.append(new_question)

        self.question_list += question_bank

    def still_has_questions(self):
        return self.question_number < len(self.question_list) - 1

    def next_question(self):
        self.current_question = self.question_list[self.question_number]
        self.question_number += 1
        return self.current_question.text

    def check_answer(self, user_answer):
        correct_answer = self.current_question.answer
        if user_answer.lower() == correct_answer.lower(): return True
        else: return False

    def get_score(self):
        return self.score

    def add_score(self):
        self.score += 1
