import random   #for secret number generator
import time     #time counter (bonus)
import json     #for saving statistics
import os       #for file operations
from datetime import datetime  #for timestamps

DIGIT = 4          #we are looking for 4 digit number
STATS_FILE = "game_statistics.json"  #file to store statistics

def get_guess_number():
    """Get guess number input from user"""
    guess = input(f"Please enter your guess: ")
    return guess
    
def guess_number_validation(guess):
    """Validate user's guess input"""
    if not guess.isdigit(): #Insert only numbers
        print("Wrong input - Insert only numbers")
        return False
    
    if len(guess) != DIGIT: #length is not correct
        print("Wrong input - Length is not correct")
        return False 
    
    if guess[0] == "0": #0 on first position
        print ("Wrong input - There is 0 on the first position")
        return False
    
    if len(guess) != len(set(guess)): #duplicity
        print("Wrong input - Duplicate digits are not allowed")
        return False
    
    return True
    
def get_secret_number():
    """Generate random secret number for the game"""
    digits = list(range(10))
    first_digit = random.choice(digits[1:])  # Avoid 0 as first digit
    digits.remove(first_digit) #in other 3 digits can be 0
    remaining_digits = random.sample(digits, DIGIT - 1) 
    secret = str(first_digit) + ''.join(map(str, remaining_digits))
    return secret  

def get_bulls_and_cows(secret, guess):
    """Calculate bulls and cows for the guess"""
    bulls = 0
    cows = 0

    for i in range(DIGIT):
        if guess[i] == secret[i]:
            bulls += 1
        elif guess[i] in secret:
            cows += 1

    return bulls, cows

def format_count(count, singular, plural):
    """Format count with proper singular/plural form"""
    if count == 0:
        return ""
    elif count == 1:
        return f"1 {singular}"
    else:
        return f"{count} {plural}"

def load_statistics():
    """Load statistics from file"""
    if os.path.exists(STATS_FILE):
        try:
            with open(STATS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []

def save_statistics(stats):
    """Save statistics to file"""
    with open(STATS_FILE, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2)

def add_game_result(guesses, time_taken):
    """Add a new game result to statistics"""
    stats = load_statistics()
    game_data = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "guesses": guesses,
        "time": round(time_taken, 2)
    }
    
    stats.append(game_data)
    save_statistics(stats)

def display_statistics():
    """Display all-time statistics"""
    stats = load_statistics()
    
    if not stats:
        print("\nNo statistics available yet. Play some games first!")
        return
    
    print("\n" + 35*"==")
    print("GAME STATISTICS")
    print(35*"==")
    print(f"Total games played: {len(stats)}")
    
    try:
        guesses = [game["guesses"] for game in stats]
        times = [game["time"] for game in stats]
    except KeyError:
        print("Error: Statistics file is corrupted.")
        return
    
    print(f"Best score (fewest guesses): {min(guesses)}")
    print(f"Average guesses: {sum(guesses) / len(guesses):.1f}")
    print(f"Fastest time: {min(times)} seconds")
    print(f"Average time: {sum(times) / len(times):.1f} seconds")
    
    print("\nLast 5 games:")
    print(35*"--")
    for game in stats[-5:]:
        print(f"{game['date']} - {game['guesses']} guesses in {game['time']} seconds")
    print(35*"==")
    print()
    
def main():
    print("Hi there!")
    print(35*"--")
    print(f"Welcome to Bulls and Cows game!")
    print(35*"--")
    print("")

    while True:
        print("Menu:")
        print("1. Play game")
        print("2. View statistics")
        print("3. Exit")
        
        choice = input("Choose an option (1-3): ").strip()
        
        if choice == "1":
            play_game()
        elif choice == "2":
            display_statistics()
        elif choice == "3":
            print("Thanks for playing! Goodbye! 👋")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.\n")

def play_game():
    """Play one round of the game"""
    secret = get_secret_number()
    score = 0
    start_time = time.time()

    while True:
        guess = get_guess_number()

        if not guess_number_validation(guess):
            continue

        score += 1
        bulls, cows = get_bulls_and_cows(secret, guess)

        if bulls == DIGIT:
            end_time = time.time()
            elapsed = round(end_time - start_time, 2)

            print(f"\nCorrect! You win 🎉")
            print(f"Guesses: {score}")
            print(f"Time: {elapsed} seconds ⏱️")
            
            # Save statistics
            add_game_result(score, elapsed)
            print("Your result has been saved!\n")
            break

        bulls_text = format_count(bulls, "bull", "bulls")
        cows_text = format_count(cows, "cow", "cows")

        if bulls_text and cows_text:
            print(f"{bulls_text}, {cows_text}")
        elif bulls_text:
            print(bulls_text)
        elif cows_text:
            print(cows_text)
        else:
            print("No bulls, no cows")
    

if __name__ == "__main__":
    main()