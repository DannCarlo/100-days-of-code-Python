from menu import Menu, MenuItem
from coffee_maker import CoffeeMaker
from money_machine import MoneyMachine

off = False

menu = Menu()
coffee_maker_obj = CoffeeMaker()
money_counter = MoneyMachine()

while not(off):
	choices = menu.get_items().split('/') + ['report']

	user_choice = None

	while user_choice not in choices:
		user_choice = input(f"What would you like? ({menu.get_items()}):")

	if user_choice == 'report':
		coffee_maker_obj.report()

	else:
		coffee = menu.find_drink(user_choice)

		if coffee_maker_obj.is_resource_sufficient(coffee) and money_counter.make_payment(coffee.cost):
			coffee_maker_obj.make_coffee(coffee)
		else:
			off = True