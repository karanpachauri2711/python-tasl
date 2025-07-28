import random

def number_hunt():
    secret = random.randint(1, 50)
    arrows = 5  # shots
    print("🌲 Welcome to the Number Hunt!")
    print("🎯 A secret number is hiding in the jungle (1-50).")
    print("🏹 You have 5 arrows to find it!\n")

    while arrows > 0:
        try:
            guess = int(input(f"Shot {6 - arrows}/5 - Take aim (1-50): "))
        except ValueError:
            print("❌ Invalid input! Enter a number.")
            continue

        if guess == secret:
            print("🔥 Bullseye! You hunted the target!")
            break
        elif guess < secret:
            print("📈 Too low! The prey ran further.")
        else:
            print("📉 Too high! You overshot the target.")

        arrows -= 1

    if arrows == 0 and guess != secret:
        print(f"\n💀 Out of arrows! The secret number was {secret}.")

    print("🏁 Hunt over. Thanks for playing!")

number_hunt()