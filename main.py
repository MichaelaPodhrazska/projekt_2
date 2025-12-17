"""Bulls and Cows game with statistics tracking."""
import random   #for secret number generator
import time     #time counter (bonus)
import json     #for saving statistics
import os       #for file operations
from datetime import datetime  #for timestamps

DIGIT = 4
STATS_FILE = "game_statistics.json"

def get_guess_number():
    """Get and return user's guess."""
    return input(f"Please enter a {DIGIT} digit number: ")
    
def guess_number_validation(guess):
    """Validate guess input and return True if valid."""
    if not guess.isdigit():
        print("Wrong input - Insert only numbers")
        return False
    if len(guess) != DIGIT:
        print("Wrong input - Length is not correct")
        return False
    if guess[0] == "0":
        print("Wrong input - There is 0 on the first position")
        return False
    if len(guess) != len(set(guess)):
        print("Wrong input - Duplicate digits are not allowed")
        return False
    return True
    
def get_secret_number():
    """Generate and return random secret number."""
    digits = list(range(10))
    first_digit = random.choice(digits[1:])
    digits.remove(first_digit)
    remaining_digits = random.sample(digits, DIGIT - 1)
    return str(first_digit) + ''.join(map(str, remaining_digits))  

def get_bulls_and_cows(secret, guess):
    """Calculate and return bulls and cows count."""
    bulls = sum(1 for i in range(DIGIT) if guess[i] == secret[i])
    cows = sum(1 for i in range(DIGIT) if guess[i] in secret and guess[i] != secret[i])
    return bulls, cows

def format_count(count, singular, plural):
    """Format count with proper singular/plural form."""
    if count == 0: return ""
    return f"{count} {singular if count == 1 else plural}"

def load_statistics():
    """Load and return statistics from JSON file."""
    if not os.path.exists(STATS_FILE): return []
    try:
        with open(STATS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

def save_statistics(stats):
    """Save statistics list to JSON file."""
    with open(STATS_FILE, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2)

def add_game_result(guesses, time_taken):
    """Add new game result to statistics."""
    stats = load_statistics()
    stats.append({"date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                  "guesses": guesses, "time": round(time_taken, 2)})
    save_statistics(stats)

def display_statistics():
    """Display game statistics summary."""
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
    print(f"Best score: {min(guesses)} | Avg: {sum(guesses)/len(guesses):.1f}")
    print(f"Fastest: {min(times)}s | Avg: {sum(times)/len(times):.1f}s")
    print("\nLast 5 games:")
    for game in stats[-5:]:
        print(f"{game['date']} - {game['guesses']} guesses, {game['time']}s")
    print(35*"==" + "\n")
    
def main():
    """Main game loop with menu."""
    print("Hi there!\n" + 35*"--")
    print("Welcome to Bulls and Cows game!")
    print(35*"--" + "\n")
    while True:
        print("Menu: 1. Play game | 2. View statistics | 3. Exit")
        choice = input("Choose (1-3): ").strip()
        if choice == "1": play_game()
        elif choice == "2": display_statistics()
        elif choice == "3":
            print("Thanks for playing! Goodbye! 👋")
            break
        else: print("Invalid choice\n")

def play_game():
    """Play one round of Bulls and Cows."""
    secret = get_secret_number()
    score = 0
    start_time = time.time()
    while True:
        guess = get_guess_number()
        if not guess_number_validation(guess): continue
        score += 1
        bulls, cows = get_bulls_and_cows(secret, guess)
        if bulls == DIGIT:
            elapsed = round(time.time() - start_time, 2)
            print(f"\nCorrect! You win 🎉\nGuesses: {score} | Time: {elapsed}s ⏱️")
            add_game_result(score, elapsed)
            print("Result saved!\n")
            break
        bulls_text = format_count(bulls, "bull", "bulls")
        cows_text = format_count(cows, "cow", "cows")
        output = [bulls_text, cows_text]
        print(", ".join(filter(None, output)) or "No bulls, no cows")
    

if __name__ == "__main__":
    main()
