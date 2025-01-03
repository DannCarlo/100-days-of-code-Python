#TODO: Create a letter using starting_letter.txt 
#for each name in invited_names.txt
#Replace the [name] placeholder with the actual name.
#Save the letters in the folder "ReadyToSend".
    
#Hint1: This method will help you: https://www.w3schools.com/python/ref_file_readlines.asp
    #Hint2: This method will also help you: https://www.w3schools.com/python/ref_string_replace.asp
        #Hint3: THis method will help you: https://www.w3schools.com/python/ref_string_strip.asp

with open('Input/Letters/starting_letter.txt') as letter:
    original_template = letter.readlines()

    original_template = "".join(original_template)

    changeable_template = original_template
    with open('Input/Names/invited_names.txt') as names:
        for name in names:
            name = name.strip()

            changeable_template = changeable_template.replace('[name]', name)

            print(changeable_template)

            with open(f'Output/ReadyToSend/{name}.txt', mode = 'w') as output:
                output.write(changeable_template)

            changeable_template = original_template