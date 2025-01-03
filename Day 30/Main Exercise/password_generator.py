#Password Generator Project
import random

LETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
NUMBERS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
SYMBOLS = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

def generate_password():
  password_list = ([random.choice(LETTERS) for _ in range(random.randint(8, 10))]
                   + [random.choice(NUMBERS) for _ in range(random.randint(2, 4))]
                   + [random.choice(SYMBOLS) for _ in range(random.randint(2, 4))])

  random.shuffle(password_list)
  password = "".join(password_list)
  return password