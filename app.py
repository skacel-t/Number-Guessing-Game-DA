import random
from statistics import mean, median, multimode


# Create a way to store the current range, so that it doesn't reset between sessions
try:
    range_file = open("range.txt", "r")
except FileNotFoundError:
    lower_value = 1
    upper_value = 10
    # and create the file if it doesn't exist
    create_file = open("range.txt", "w")
    create_file.close()
else:
    range_list = range_file.readlines()
    lower_value = int(range_list[0])
    upper_value = int(range_list[1])
    range_file.close()


def update_range(val1, val2):
    with open("range.txt", "w") as file:
        file.write(str(val1)+"\n")
        file.write(str(val2)+"\n")


# Next, we tackle posting and getting data form a text file, this ensures tracking even if the app is quit
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


def reset_data():
    file_1 = open("high_score.txt", "w")
    file_1.close()
    file_2 = open("scores.txt", "w")
    file_2.close()


# Next, some functions which display information to the user
def show_stats():
    data = get_scores()
    mode_list = multimode(data)
    mode_list_str = [str(num) for num in mode_list]
    mode_print = ", ".join(mode_list_str)
    print("------------------------------------\n"
          "Overall Statistics:\n"
          f"a. Number of guesses last game: {data[-1]}\n"
          f"b. Mean number of guesses: {round(mean(data),2)}\n"
          f"c. Median number of guesses: {int(median(data))}\n"
          f"d. The mode of guesses: {mode_print}\n"
          "------------------------------------\n")


def show_welcome_message():
    welcome_message = "Welcome to the Number Guessing Game!"
    print(f"\n{"-"*len(welcome_message)}\n{welcome_message}\n{"-"*len(welcome_message)}")


# Next, we write the game code
def start_game():
    high_score = get_high_score()
    print(f"------------------------------------\nHigh Score: {high_score}\n")
    player_guess = None
    attempts = 0
    answer = random.randint(lower_value, upper_value)
    while player_guess != answer:
        try:
            player_guess = int(input(f"Guess a number between {lower_value} and {upper_value}:  "))
            if player_guess > upper_value or player_guess < lower_value:
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


def menu():
    print("------------------------------------\n"
          "1. Start a game\n"
          "2. Change range\n"
          "3. View Stats\n"
          "4. Help\n"
          "5. Quit\n"
          "------------------------------------")

    while True:
        try:
            choice = input("Enter a number from the menu above:  ")
            if choice not in ("1", "2", "3", "4", "5"):
                raise Exception("\nInvalid input. Please enter '1', '2', '3', '4' or '5'.\n")
        except Exception as err:
            print(err)
        else:
            break

    if choice == "1":
        play_again = "yes"
        while play_again == "yes":
            start_game()        
            play_again = ask_play_again()
        return True

    elif choice == "2":
        while True:
            try:
                warning = input("\nWARNING: This will reset game statistics, are you sure you wish to proceed? [yes/no]  ")
                if warning not in ("yes", "no"):
                    raise Exception("\nInvalid input. Please enter 'yes' or 'no'.\n")
            except Exception as err:
                print(err)
            else:
                break
        if warning == "no":
            return True
        while True:
            try:
                inf = int(input("\nPlease enter the lower value for the range:  "))
                sup = int(input("Please enter the upper value for the range:  "))
                if inf < 0 or sup < 0:
                    raise ValueError
                if inf >= sup:
                    raise Exception("Invalid input. The lower value must be smaller than the upper value!")
            except ValueError:
                print("At least one invalid input. Please only enter whole numbers greater than zero.\n")
            except Exception as err:
                print(err)
            else:
                break
        global lower_value
        lower_value = inf
        global upper_value
        upper_value = sup
        update_range(lower_value, upper_value)
        reset_data()
        return True

    elif choice == "3":
        try:
            print("")
            show_stats()
            input("Press Enter to return to the menu.")
        except IndexError:
            input("No statistics to show, play a game first. Press Enter to return to menu.")
            return True
        else:
            return True

    elif choice == "4":
        input("\nThe goal of this game is to guess a hidden number in a given range in as few attempts as possible.\n"
              "The default range is set to 0, 1, 2, ..., 10, but you can change this in the menu.\n"
              "Please note that the numbers in your range must be greater than 0.\n"
              "You can view the statistics of all previous games in the menu.\n"
              "\nPress enter to return to the menu.")
        return True

    elif choice == "5":
        print("\nThanks for playing, goodbye!\n")
        return False


# Running the game
create_txt_files()
show_welcome_message()
if __name__ == "__main__":
    run_game = True
    while run_game:
        run_game = menu()










