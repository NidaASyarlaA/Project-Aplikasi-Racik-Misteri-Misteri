import random
import time
import sys
import platform

if platform.system() == "Windows":
    try:
        import winsound
        WINSOUND_AVAILABLE = True
    except Exception:
        WINSOUND_AVAILABLE = False
else:
    WINSOUND_AVAILABLE = False
 
# ====== Utility: safe print with flush ======
def sprint(text=""):
    print(text, flush=True)

# ====== Effect: ketik (typewriter) with optional beep ======
def ketik(teks, delay=0.02, suara=True):
    if not teks:
        print()
        return
    for char in teks:
        sys.stdout.write(char)
        sys.stdout.flush()
        if suara and char.strip() and WINSOUND_AVAILABLE:
            # safe freqs
            freq = random.randint(400, 1200)
            dur = random.randint(12, 35)
            try:
                winsound.Beep(freq, dur)
            except Exception:
                pass
        time.sleep(delay)
    print()

# ====== ANSI Colors (may not work in all terminals) ======
RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
MAGENTA = "\033[35m"
RED = "\033[31m"

# ====== ASCII art: cup + steam ======
CUP_ART = [
r"      (  )   (   )  )",
r"       ) (   )  (  (",
r"       ( )  (    ) )",
r"       _____________",
r"       _____________",
r"      |  ~  ~  ~  ~ |/ _ \ ",
r"      |  ~  ~  ~  ~ | / | |",
r"      |             | | | |",
r"      |             | |_| |",
r"      |_____________|",
]

def show_cup_animation(frames=6, delay=0.25):
    steam_frames = ["  ( )  ", " (   ) ", "(     )", " (   ) "]
    for i in range(frames):
        # clear small area by printing newlines (simple)
        print("\n"*1)
        print(CYAN + steam_frames[i % len(steam_frames)] + RESET)
        for line in CUP_ART:
            print(GREEN + line + RESET)
        time.sleep(delay)

# ====== Progress bar for 'cooking' jamu ======
def progress_bar(steps=5, delay=0.35, prefix="  "):
    frames = ["[■□□□□]", "[■■□□□]", "[■■■□□]", "[■■■■□]", "[■■■■■]"]
    for f in frames[:steps]:
        sys.stdout.write(f"\r{prefix}{f} Lagi nggarap... ")
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write("\r" + " " * 40 + "\r")
    sys.stdout.flush()
