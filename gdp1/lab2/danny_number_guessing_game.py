import random

secret_number = random.randrange(1,129)

guess = 0
guesses = []
stop = False
while guess != secret_number:
    guess = input("Guess a number 1 to 128: ")
    if str(guess) == "q":
        stop = True
        print("You have quit, thank you for playing")
        break
    if not stop:
        if len(guesses) < 7:
            guess = int(guess)
            guesses.append(guess)
            if guess < secret_number:
                print( "Too low." )
            elif guess > secret_number:
                print( "Too high." )
            else:
                print( "Correct!")
        else:
            print("Number of guesses exceeded, Game Over")
            break

if not stop:
    print("Your guesses: " + " ".join(str(y) for y in guesses))
