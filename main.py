import threading
from engine import *
import curses as cr
import time
from mainmenu import *
from config import GAME_ROOT

def run_game(stdscr: cr.window, audio_file: str, lrc_file: str, speed: float):
    """Runs the main game loop."""
    cr.curs_set(0)  # Disable the cursor
    cr.init_pair(1, cr.COLOR_GREEN, cr.COLOR_BLACK)  # Correct input
    cr.init_pair(2, cr.COLOR_RED, cr.COLOR_BLACK)    # Incorrect input
    cr.init_pair(3, cr.COLOR_WHITE, cr.COLOR_BLACK)  # Default text
    cr.init_pair(4, cr.COLOR_YELLOW, cr.COLOR_BLACK) # Highlight next line

    lyrics = parse_lrc(lrc_file)  # Parse the lyrics file
    audio_thread = threading.Thread(target=play_audio, args=(audio_file, speed), daemon=True)
    audio_thread.start()

    height, width = stdscr.getmaxyx()
    errors = 0
    start_time = time.time()

    for i, (timestamp, line) in enumerate(lyrics):
        elapsed_time = time.time() - start_time
        if timestamp / speed > elapsed_time:
            time.sleep(timestamp / speed - elapsed_time)

        # Determine the next line and its timing
        if i + 1 < len(lyrics):
            next_timestamp = lyrics[i + 1][0]
            next_line = lyrics[i + 1][1]
        else:
            next_timestamp = timestamp + 5  # Default delay for the last line
            next_line = ""

        # Calculate the time limit for the current line
        time_limit = (next_timestamp - timestamp) / speed

        # Display the next line with a fade effect
        stdscr.addstr(
            height // 2 + 6,
            width // 2 - len(f"Next: {next_line[:width-6]}") // 2,
            f"Next: {next_line[:width-6]}",
            cr.color_pair(4) | cr.A_BOLD
        )

        # Process the current line and update error count
        errors += get_string(stdscr, height, width, line, time_limit)

        # Clear the screen for the next iteration
        stdscr.clear()

    return errors

def main(stdscr: cr.window):
    """Main entry point of the game."""
    level, speed = menu(stdscr)  # Get level and speed from the menu
    errors = run_game(
        stdscr,
        f"{GAME_ROOT}/levels/{level}.mp3",
        f"{GAME_ROOT}/levels/{level}.lrc",
        speed
    )
    stdscr.clear()
    stdscr.addstr(10, 10, f"Game Over! Errors: {errors}", cr.color_pair(2) | cr.A_BOLD)
    stdscr.refresh()
    time.sleep(3)

if __name__ == "__main__":
    cr.wrapper(main)
