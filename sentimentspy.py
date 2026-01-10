from colorama import Fore, Style, init
from textblob import TextBlob
from datetime import datetime

init(autoreset=True)

print(f"{Fore.BLUE} {Style.BRIGHT} SENTIMENT SPY")
name = input(f"{Fore.MAGENTA}Enter your name: ").strip() or "Agent"
print(f"{Fore.CYAN}Welcome, {name}")
print(f"{Fore.CYAN}Commands: :help :stats :reset :exit\n")

history = []

def analyze(text):
    polarity = round(TextBlob(text).sentiment.polarity, 3)
    confidence = round(abs(polarity) * 100, 2)

    if polarity >= 0.3:
        return "Positive", polarity, confidence, Fore.GREEN
    if polarity <= -0.3:
        return "Negative", polarity, confidence, Fore.RED
    return "Neutral", polarity, confidence, Fore.YELLOW

def show_help():
    print(f"""{Fore.CYAN}
    :help     Show commands
    :stats    Session summary
    :reset    Clear data
    :exit     Exit
    """)


def show_stats():
    if not history:
        print(f"{Fore.RED}No data available")
        return
    avg = round(sum(h["polarity"] for h in history) / len(history), 3)
    pos = sum(1 for h in history if h["polarity"] > 0)
    neg = sum(1 for h in history if h["polarity"] < 0)
    neu = len(history) - pos - neg

    print(f"""{Fore.CYAN}
    Total Inputs : {len(history)}
    Positive     : {pos}
    Negative     : {neg}
    Neutral      : {neu}
    Avg Polarity : {avg}
    """)

while True:
    user_input = input(f"{Fore.GREEN}>> ").strip()

    if not user_input:
        print(f"{Fore.RED}Input required")
        continue

    if user_input.startswith(":"):
        if user_input == ":exit":
            print(f"{Fore.BLUE}Session closed")
            break
        if user_input == ":help":
            show_help()
        elif user_input == ":stats":
            show_stats()
        elif user_input == ":reset":
            history.clear()
            print(f"{Fore.YELLOW}Session reset")
        else:
            print(f"{Fore.RED}Invalid command")
        continue

    sentiment, polarity, confidence, color = analyze(user_input)
    timestamp = datetime.now().strftime("%H:%M:%S")

    history.append({
        "sentiment": sentiment,
        "polarity": polarity,
        "confidence": confidence,
        "time": timestamp
    })

    print(f"{color}Sentiment  : {sentiment}")
    print(f"{color}Polarity   : {polarity}")
    print(f"{color}Confidence : {confidence}%\n")
