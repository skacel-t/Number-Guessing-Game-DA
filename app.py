import random
from statistics import mean, median, multimode


# First, we tackle posting and getting data form a text file, this ensures tracking even if the app is quit
# Note that I save scores into a text file rather than into a list to ensure tracking when the app is quit
# I do however recover this data into a list in the get_scores() function.
def update_high_score(score):
    with open("high_score.txt", "w") as file:
        file.write(score)


def get_high_score():
    with open("high_score.txt", "r") as file:
        score = file.read()
        if score == "":
            return "No high score yet!"
        else:
            return score


def save_score(score):
    with open("scores.txt", "a") as file:
        file.write(score+"\n")


def get_scores():
    scores_list = []
    with open("scores.txt", "r") as file:
        for line in file:
            scores_list.append(int(line))
    return scores_list


def create_txt_files():
    file_1 = open("high_score.txt", "a")
    file_1.close()
    file_2 = open("scores.txt", "a")
    file_2.close()


# Next, some functions which display information to the user
def show_stats():
    data = get_scores()
    mode_list = multimode(data)
    mode_list_str = [str(num) for num in mode_list]
    mode_print = ", ".join(mode_list_str)
    print(f"Overall Statistics:\n"
          f"a. Number of guesses last game: {data[-1]}\n"
          f"b. Mean number of guesses: {round(mean(data),2)}\n"
          f"c. Median number of guesses: {int(median(data))}\n"
          f"d. The mode of guesses: {mode_print}\n")


def show_welcome_message():
    welcome_message = "Welcome to the Number Guessing Game!"
    print(f"\n{"-"*len(welcome_message)}\n{welcome_message}\n{"-"*len(welcome_message)}\n")


# Next, we write the game code
def start_game():
    player_guess = None
    attempts = 0
    answer = random.randint(1,10)
    while player_guess != answer:
        try:
            player_guess = int(input(f"Guess a number between 1 and 10:  "))
            if player_guess > 10 or player_guess < 1:
                raise Exception("That number is out of range. Try again.")
        except ValueError as err: 
            print("Please enter a whole number.")
        except Exception as err:
            print(f"{err}")
        else:    
            attempts += 1
            if player_guess < answer:
                print("It's higher!")
            elif player_guess > answer:
                print("It's lower!")
    return attempts          

def ask_play_again():
    while True:
        try:
            play_again = input("Would you like to play again? [yes/no]  ")
            if play_again not in ("yes", "no"):
                raise Exception("\nInvalid input. Please enter 'yes' or 'no'.\n")
        except Exception as err:
            print(err)
        else:
            break
    return play_again  


# Running the game -------------------------------------------------------------------------------- 
create_txt_files()
show_welcome_message()
play_again = "yes"

while play_again == "yes":
    high_score = get_high_score()
    print(f"------------------------------------\nHigh Score: {high_score}\n")
    attempts = start_game()
    if high_score == "No high score yet!":
        update_high_score(str(attempts))
        print(f"\nCongratulations, you got it in {attempts} attempts! That is a new High Score!\n")
    elif int(high_score) > attempts:
        update_high_score(str(attempts))
        print(f"\nCongratulations, you got it in {attempts} attempts! That is a new High Score!\n")
    elif int(high_score) == attempts:
        print(f"\nCongratulations, you got it in {attempts} attempts! You tied the High Score!\n")
    else:
        print(f"\nCongratulations, you got it in {attempts} attempts!\n")

    save_score(str(attempts))
    show_stats()
    play_again = ask_play_again()

print("\nThanks for playing, goodbye!\n")









