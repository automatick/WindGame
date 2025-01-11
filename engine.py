import re
import string
import curses as cr
import time
import os
import threading
from pydub import AudioSegment
from pydub.playback import play


def change_audio_speed(audio: AudioSegment, speed: float) -> AudioSegment:
    """Adjusts the playback speed of an audio file."""
    new_frame_rate = int(audio.frame_rate * speed)
    return audio._spawn(audio.raw_data, overrides={"frame_rate": new_frame_rate}).set_frame_rate(audio.frame_rate)


def play_audio(file_path: str, speed: float = 1.0):
    """Plays an audio file with optional speed adjustment."""
    audio = AudioSegment.from_file(file_path)
    if speed != 1.0:
        audio = change_audio_speed(audio, speed)
    play(audio)


def parse_lrc(file_path: str) -> list[tuple[float, str]]:
    """Parses a .lrc file and returns a list of timestamped lyrics."""
    pattern = re.compile(r"\[(\d+):(\d+\.\d+)\](.*)")
    lyrics = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            match = pattern.match(line.strip())
            if match:
                minutes = int(match.group(1))
                seconds = float(match.group(2))
                timestamp = minutes * 60 + seconds
                text = match.group(3)
                text = text.translate(str.maketrans("", "", string.punctuation)).strip()
                lyrics.append((timestamp, text))
    return lyrics


def get_string(stdscr: cr.window, height: int, width: int, line: str, time_limit: float) -> int:
    """Handles user input for typing a given line with visual effects."""
    user_input = ""
    color_pairs = []
    errors = 0
    score = 0
    combo = 0
    stdscr.nodelay(True)
    start_time = time.time()
    target_line = line.lower()

    # Initialize more color pairs for visual effects
    cr.init_pair(5, cr.COLOR_CYAN, cr.COLOR_BLACK)    # Combo indicator
    cr.init_pair(6, cr.COLOR_MAGENTA, cr.COLOR_BLACK) # Score
    cr.init_pair(7, cr.COLOR_BLUE, cr.COLOR_BLACK)    # Time critical

    while len(user_input) < len(target_line):
        elapsed_time = time.time() - start_time
        remaining_time = time_limit - elapsed_time
        if remaining_time <= 0:
            break

        # Display the target line with enhanced color effects
        for idx, char in enumerate(line):
            if idx < len(user_input):
                if user_input[idx] == char.lower():
                    color = cr.color_pair(1)
                    style = cr.A_BOLD
                else:
                    color = cr.color_pair(2)
                    style = cr.A_BOLD
            else:
                color = cr.color_pair(3)
                style = cr.A_DIM
            stdscr.addstr(height // 2, width // 2 - len(line) // 2 + idx, char, color | style)

        # Enhanced cursor highlight with pulsing effect
        if len(user_input) < len(target_line):
            pulse = int((time.time() * 4) % 2)  # Creates a pulsing effect
            cursor_style = cr.A_REVERSE if pulse else cr.A_BOLD
            stdscr.addstr(height // 2, width // 2 - len(line) // 2 + len(user_input),
                         line[len(user_input)], cursor_style | cr.color_pair(5))

        # Improved time bar with color gradient
        time_percentage = remaining_time / time_limit
        bar_length = width - 20
        filled_length = max(0, int(time_percentage * bar_length))
        time_color = cr.color_pair(1) if time_percentage > 0.5 else \
                    cr.color_pair(7) if time_percentage > 0.25 else cr.color_pair(2)
        
        time_bar = "█" * filled_length + "░" * (bar_length - filled_length)
        stdscr.addstr(height // 2 + 2, 5, "Time: [", cr.color_pair(3))
        stdscr.addstr(time_bar, time_color | cr.A_BOLD)
        stdscr.addstr("]", cr.color_pair(3))

        # Display score and combo
        score_text = f"Score: {score}"
        combo_text = f"Combo: x{combo}" if combo > 1 else ""
        stdscr.addstr(height // 2 - 2, width // 2 - len(score_text) // 2,
                     score_text, cr.color_pair(6) | cr.A_BOLD)
        if combo > 1:
            stdscr.addstr(height // 2 - 3, width // 2 - len(combo_text) // 2,
                         combo_text, cr.color_pair(5) | cr.A_BOLD)

        stdscr.refresh()

        try:
            key = stdscr.get_wch()
            if isinstance(key, str):
                if key in ("\b", "\x7f"):  # Handle backspace
                    if user_input:
                        user_input = user_input[:-1]
                        color_pairs.pop()
                        combo = 0
                else:
                    user_input += key.lower()
                    if len(user_input) <= len(target_line) and user_input[-1] == target_line[len(user_input) - 1]:
                        color_pairs.append(1)
                        combo += 1
                        score += 10 * combo
                    else:
                        color_pairs.append(2)
                        errors += 1
                        combo = 0
            elif key == cr.KEY_BACKSPACE:
                if user_input:
                    user_input = user_input[:-1]
                    color_pairs.pop()
                    combo = 0
        except cr.error:
            pass

    return errors


def get_levels() -> list[str]:
    """Retrieves a list of available levels based on existing .lrc and .mp3 files."""
    levels = []
    for file in os.listdir("levels"):
        if file.endswith(".lrc") and os.path.isfile(f"levels/{file[:-4]}.mp3"):
            levels.append(file[:-4])
    return levels


def calculate_level_difficulty(lyrics: list[tuple[float, str]]) -> tuple[int, int]:
    """Calculates the difficulty of a level based on lyrics timing and length."""
    total_time = sum([lyric[0] for lyric in lyrics])
    speed = 0
    previous_time = 0

    for lyric in lyrics:
        delay = lyric[0] - previous_time
        length = len(lyric[1])
        if delay > 0:
            speed += length / delay
        previous_time = lyric[0]

    return int(speed), int(total_time)
