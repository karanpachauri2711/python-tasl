import random

def give_feedback(secret, guess):
    feedback = []
    for i in range(3):
        if guess[i] == secret[i]:
            feedback.append("✅ Correct")
        elif guess[i] in secret:
            feedback.append("🔁 Right digit, wrong place")
        else:
            feedback.append("❌ Not in code")
    return feedback

def treasure_code_breaker():
    print("🧭 Welcome to Treasure Code Breaker!")
    print("🔐 A 3-digit code locks the treasure chest.")
    print("💡 Guess the code! You have 6 tries.\n")

    digits = [str(random.randint(0, 9)) for _ in range(3)]
    attempts = 6

    for attempt in range(1, attempts + 1):
        guess = input(f"🔢 Attempt {attempt}/6 - Enter a 3-digit code: ")
        if len(guess) != 3 or not guess.isdigit():
            print("❌ Invalid input! Enter exactly 3 digits.")
            continue

        if list(guess) == digits:
            print("🎉 You cracked the code! The treasure is yours! 🏆")
            return
        else:
            fb = give_feedback(digits, list(guess))
            for i, f in enumerate(fb):
                print(f"Digit {i+1}: {f}")
            print("-" * 30)

    print(f"\n💀 You failed to break the code. It was {''.join(digits)}.")

treasure_code_breaker()