secret_number=50
while  True:
    guess = input("Enter number: ")
    if (int(guess) ==secret_number):
        print("Your guest is right")
        break