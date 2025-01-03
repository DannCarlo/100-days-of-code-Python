MENU = {
    "espresso": {
        "ingredients": {
            "water": 50,
            "coffee": 18,
        },
        "cost": 1.5,
    },
    "latte": {
        "ingredients": {
            "water": 200,
            "milk": 150,
            "coffee": 24,
        },
        "cost": 2.5,
    },
    "cappuccino": {
        "ingredients": {
            "water": 250,
            "milk": 100,
            "coffee": 24,
        },
        "cost": 3.0,
    }
}

resources = {
    "water": 300,
    "milk": 200,
    "coffee": 100,
    "money": 0
}

off = False

while not(off):

    choices = ['espresso', 'latte', 'cappuccino', 'report']

    user_choice = None

    while user_choice not in choices:
        user_choice = input("What would you like? (espresso/latte/cappuccino):")

    if user_choice == 'report':
        print(f"Water : {resources['water']}ml")
        print(f"Milk : {resources['milk']}ml")
        print(f"Coffee : {resources['coffee']}g")
        print(f"Money : ${resources['money']}")
    else:
        insufficient_ing = False

        for i in MENU[user_choice]["ingredients"]:
            if resources[i] < MENU[user_choice]["ingredients"][i]:
                print(f"Sorry there is not enough {i}.")
                insufficient_ing = True
                break

        if insufficient_ing == False:
            quarters = int(input("How many quarters? "))
            dimes = int(input("How many dimes? "))
            nickles = int(input("How many nickles? "))
            pennies = int(input("How many pennies? "))

            quarters *= .25
            dimes *= .1
            nickles *= .05
            pennies *= .01

            total_payment = quarters + dimes + nickles + pennies

            if total_payment >= MENU[user_choice]["cost"]:
                if total_payment > MENU[user_choice]["cost"]:
                    change = total_payment - MENU[user_choice]["cost"]

                    print(f"Here is ${change} in change.")

                resources["money"] += MENU[user_choice]["cost"]
                print(f"Here is your {user_choice}. Enjoy!")

                for i in MENU[user_choice]["ingredients"]:
                    resources[i] -= MENU[user_choice]["ingredients"][i]
            else: 
                print("Sorry that's not enough money. Money refunded.")
        else:
            off = True