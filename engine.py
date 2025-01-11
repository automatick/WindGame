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
    stdscr.nodelay(True)
    start_time = time.time()
    target_line = line.lower()

    while len(user_input) < len(target_line):
        elapsed_time = time.time() - start_time
        remaining_time = time_limit - elapsed_time
        if remaining_time <= 0:
            break

        # Display the target line with color effects
        for idx, char in enumerate(line):
            color = cr.color_pair(1) if idx < len(user_input) and user_input[idx] == char.lower() else cr.color_pair(3)
            style = cr.A_BOLD if idx < len(user_input) else cr.A_DIM
            stdscr.addstr(height // 2, width // 2 - len(line) // 2 + idx, char, color | style)

        # Highlight the current character being typed
        if len(user_input) < len(target_line):
            stdscr.addstr(height // 2, width // 2 - len(line) // 2 + len(user_input), line[len(user_input)], cr.A_REVERSE)

        # Display remaining time
        time_bar_length = max(0, int((remaining_time / time_limit) * (width - 20)))
        stdscr.addstr(height // 2 + 2, 5, "Time left: [" + "=" * time_bar_length + " " * (width - 20 - time_bar_length) + "]", cr.color_pair(4))

        stdscr.refresh()

        # Handle user input
        try:
            key = stdscr.get_wch()
            if isinstance(key, str):
                if key in ("\b", "\x7f"):  # Handle backspace
                    if user_input:
                        user_input = user_input[:-1]
                        color_pairs.pop()
                else:
                    user_input += key.lower()
                    if user_input[-1] == target_line[len(user_input) - 1]:
                        color_pairs.append(1)  # Correct input
                    else:
                        color_pairs.append(2)  # Incorrect input
                        errors += 1
            elif key == cr.KEY_BACKSPACE:  # Alternative handling for backspace
                if user_input:
                    user_input = user_input[:-1]
                    color_pairs.pop()
        except cr.error:
            pass

    # Count remaining untyped characters as errors
    return errors + len(target_line) - len(user_input)



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
