from engine import get_levels, calculate_level_difficulty, parse_lrc
import curses as cr
from config import GAME_NAME, GAME_ROOT
import time


def menu(stdscr: cr.window):
    """Displays the game menu and allows the user to select a level and speed mode."""
    cr.curs_set(0)  # Disable the cursor
    height, width = stdscr.getmaxyx()
    levels_path = f"{GAME_ROOT}/levels"

    # Speed modes and their corresponding values
    selected_mode = 1  # Default to normal mode (1.0x speed)
    speed_modes = ["Normal", "Nightcore", "Daycore"]
    speed_values = [1.0, 1.5, 0.75]
    speed_icons = ["*", "+", "-"]

    # Initialize color pairs
    cr.start_color()
    cr.init_pair(1, cr.COLOR_CYAN, cr.COLOR_BLACK)     # Header and footer
    cr.init_pair(2, cr.COLOR_GREEN, cr.COLOR_BLACK)    # Selected level
    cr.init_pair(3, cr.COLOR_WHITE, cr.COLOR_BLACK)    # Regular level
    cr.init_pair(4, cr.COLOR_YELLOW, cr.COLOR_BLACK)   # Mode
    cr.init_pair(5, cr.COLOR_MAGENTA, cr.COLOR_BLACK)  # Difficulty and duration
    cr.init_pair(6, cr.COLOR_BLUE, cr.COLOR_BLACK)     # Border

    def draw_border():
        """Draws a decorative border around the menu."""
        # Draw top and bottom borders
        for x in range(width - 1):
            stdscr.addch(0, x, '-')
            stdscr.addch(height - 2, x, '-')
        
        # Draw side borders
        for y in range(height - 1):
            if y > 0 and y < height - 2:
                stdscr.addch(y, 0, '|')
                stdscr.addch(y, width - 2, '|')
        
        # Draw corners
        stdscr.addch(0, 0, '+')
        stdscr.addch(0, width - 2, '+')
        stdscr.addch(height - 2, 0, '+')
        stdscr.addch(height - 2, width - 2, '+')

    def draw_header():
        """Draws the header with the game name."""
        title = f"* {GAME_NAME} *"
        centered_title = title.center(width - 4)
        stdscr.addstr(1, 2, centered_title, cr.color_pair(1) | cr.A_BOLD)
        # Decorative line under title
        separator = "-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-"
        centered_separator = separator.center(width - 4)
        stdscr.addstr(2, 2, centered_separator, cr.color_pair(1))

    def draw_levels(levels, selected, animation_frame):
        """Displays the list of levels with difficulty and duration."""
        for i, level in enumerate(levels):
            difficulty, duration = calculate_level_difficulty(parse_lrc(f"{levels_path}/{level}.lrc"))
            
            # Create animated selector
            selector = "> " if i == selected and animation_frame else "  "
            
            # Format level info with better spacing
            level_name = f"{f'<{level}>':<20}"
            difficulty_str = f"Difficulty: {min(difficulty, 999)}"
            duration_str = f"Duration: {str(duration)[:-1]}s"
            
            level_info = f"{selector}{level_name}\t\t [{difficulty_str} | {duration_str}]"
            
            y_pos = i + 4  # Start levels list after header
            if i == selected:
                stdscr.addstr(y_pos, 2, level_info, cr.color_pair(2) | cr.A_BOLD)
            else:
                stdscr.addstr(y_pos, 2, level_info, cr.color_pair(3))

    def draw_speed_modes(selected_mode):
        """Displays available speed modes in a stylish way."""
        mode_y = height - 4
        mode_text = "Speed Mode: "
        stdscr.addstr(mode_y, 2, mode_text, cr.color_pair(4))
        
        for i, (mode, icon) in enumerate(zip(speed_modes, speed_icons)):
            x_pos = len(mode_text) + 2 + i * 20
            if i == selected_mode:
                mode_str = f"{icon} {mode} {icon}"
                stdscr.addstr(mode_y, x_pos, mode_str, cr.color_pair(4) | cr.A_BOLD | cr.A_REVERSE)
            else:
                mode_str = f"{icon} {mode}"
                stdscr.addstr(mode_y, x_pos, mode_str, cr.color_pair(4))

    def draw_footer():
        """Displays the footer with navigation instructions."""
        controls = "UP/DOWN: Navigate | E: Change Mode | Enter: Start"
        stdscr.addstr(height-3, 2, controls.center(width-4), cr.color_pair(1) | cr.A_BOLD)

    # Get available levels and initialize the selection
    levels = get_levels()
    selected = 0
    animation_frame = True
    last_frame_time = time.time()
    animation_interval = 0.5  # seconds

    while True:
        current_time = time.time()
        if current_time - last_frame_time >= animation_interval:
            animation_frame = not animation_frame
            last_frame_time = current_time

        stdscr.clear()
        draw_border()
        draw_header()
        draw_levels(levels, selected, animation_frame)
        draw_speed_modes(selected_mode)
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
        elif key in [ord('e'), ord('E')]:  # Change speed mode
            selected_mode = (selected_mode + 1) % len(speed_modes)

    # Clear the screen before starting the game
    stdscr.clear()
    stdscr.refresh()
    return levels[selected], speed_values[selected_mode]
