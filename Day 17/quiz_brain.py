class Quiz:

	def __init__(self, q_list):
		self.question_number = 0
		self.question_list = q_list
		self.correct_answers = 0

	def still_has_questions(self):
		return self.question_number < len(self.question_list)

	def next_question(self):
		current_question = self.question_list[self.question_number]
		self.question_number += 1
		answer = input(f"Q.{self.question_number}: {current_question.question} (True/False): ")
		self.check_answer(current_question.answer, answer)

	def check_answer(self, correct_answer, user_answer):
		if correct_answer == user_answer:
			self.correct_answers += 1
			print("You got it right!")
		else:
			print(f"That is wrong. The correct answer is {correct_answer}")

