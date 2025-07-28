import random
import time
import os

words = ["python", "code", "game", "data", "ai", "logic", "debug", "chat", "cloud", "loop"]
score = 0

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def snake_word_game():
    global score
    print("🐍 Welcome to Snake Word Hunt!")
    print("Type the word before it reaches the bottom. Press Enter to start...")
    input()

    for i in range(1, 11):
        word = random.choice(words)
        clear()
        print(f"\nRound {i}")
        print(f"\nThe word is falling... type: '{word}'")
        
        for j in range(3, 0, -1):
            print(f"⏳ {j}...")
            time.sleep(1)

        typed = input("✍ Your input: ").strip()
        if typed.lower() == word:
            score += 1
            print("✅ Correct! +1 point.")
        else:
            print(f"❌ Missed! The word was: {word}")
        time.sleep(1)

    print(f"\n🏁 Game Over! Your final score: {score}/10")

snake_word_game()