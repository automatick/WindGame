from engine import get_levels, calculate_level_difficulty, parse_lrc
import curses as cr
from config import GAME_NAME, GAME_ROOT


def menu(stdscr: cr.window):
    """Displays the game menu and allows the user to select a level and speed mode."""
    cr.curs_set(0)  # Disable the cursor
    height, width = stdscr.getmaxyx()
    levels_path = f"{GAME_ROOT}/levels"

    # Speed modes and their corresponding values
    selected_mode = 1  # Default to normal mode (1.0x speed)
    speed_modes = ["Normal", "Nightcore", "Daycore"]
    speed_values = [1.0, 1.5, 0.75]

    # Initialize color pairs
    cr.start_color()
    cr.init_pair(1, cr.COLOR_CYAN, cr.COLOR_BLACK)  # Header and footer
    cr.init_pair(2, cr.COLOR_GREEN, cr.COLOR_BLACK)  # Selected level
    cr.init_pair(3, cr.COLOR_WHITE, cr.COLOR_BLACK)  # Regular level
    cr.init_pair(4, cr.COLOR_YELLOW, cr.COLOR_BLACK)  # Mode
    cr.init_pair(5, cr.COLOR_MAGENTA, cr.COLOR_BLACK)  # Difficulty and duration

    def draw_header():
        """Draws the header with the game name."""
        centered_game_name = GAME_NAME.center(width - 1, " ")
        stdscr.addstr(0, 0, centered_game_name[:width - 1], cr.color_pair(1) | cr.A_BOLD)

    def draw_levels(levels, selected):
        """Displays the list of levels with difficulty and duration."""
        for i, level in enumerate(levels):
            difficulty, duration = calculate_level_difficulty(parse_lrc(f"{levels_path}/{level}.lrc"))
            level_info = f"{i + 1}: {level} \t\t  [Difficulty: {difficulty} | Duration: {str(duration)[:-1]}s]"

            if i == selected:
                stdscr.addstr(i + 2, 2, level_info, cr.color_pair(2) | cr.A_BOLD | cr.A_REVERSE)
            else:
                stdscr.addstr(i + 2, 2, level_info, cr.color_pair(3))

    def draw_footer():
        """Displays the footer with navigation instructions and the current mode."""
        footer_text = "Arrows: Navigate | 'e': Change Mode | Enter: Start"
        mode_text = f"Mode: {speed_modes[selected_mode]}"
        stdscr.addstr(height - 2, 0, footer_text.center(width - 1), cr.color_pair(1) | cr.A_BOLD)
        stdscr.addstr(height - 1, 0, mode_text.center(width - 1), cr.color_pair(4) | cr.A_BOLD)

    # Get available levels and initialize the selection
    levels = get_levels()
    selected = 0

    while True:
        stdscr.clear()
        draw_header()
        draw_levels(levels, selected)
        draw_footer()
        stdscr.refresh()

        # Handle user input
        key = stdscr.getch()
        if key == ord('\n'):  # Enter key to confirm
            break
        elif key == cr.KEY_UP and selected > 0:  # Navigate up
            selected -= 1
        elif key == cr.KEY_DOWN and selected < len(levels) - 1:  # Navigate down
            selected += 1
        elif key == ord('e'):  # Change speed mode
            selected_mode = (selected_mode + 1) % len(speed_modes)

    # Clear the screen before starting the game
    stdscr.clear()
    stdscr.refresh()
    return levels[selected], speed_values[selected_mode]
