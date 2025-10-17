from ascii_art import ASCII_ART
import curses

#? Starts counting from bellow the ascii art.
FIRST_ROW = ASCII_ART.count('\n') + 2

class Screen:
    def __init__(self):
        """
        Initializes the screen for terminal-based UI using curses.

        - Initializes the curses standard screen.
        - Enables keypad mode to capture special keys.
        - Retrieves and stores the current terminal's height and width.
        """
        self.stdscr = curses.initscr()
        self.stdscr.keypad(True)
        #? Get the current terminal size.
        self.height, self.width = self.stdscr.getmaxyx()
    
    def display_ascii_menu(self):
        """
        Displays the ASCII art menu on the screen using bold formatting.

        This method writes the ASCII_ART string to the top-left corner of the curses window
        with bold attribute and refreshes the screen to show the changes.
        """
        self.stdscr.addstr(0, 0, ASCII_ART, curses.A_BOLD)
        self.stdscr.refresh()
    
    def display_str(self, str, x, y):
        """
        Displays a string at the specified (x, y) coordinates on the screen using bold formatting.

        Args:
            str (str): The string to display.
            x (int): The x-coordinate (column) where the string will be displayed.
            y (int): The y-coordinate (row) where the string will be displayed.

        Returns:
            None
        """
        self.stdscr.addstr(y, x, str, curses.A_BOLD)
        self.stdscr.refresh()
    
    def close(self):
        """
        Waits for a key press from the user and then properly terminates the curses application.

        This method pauses execution until the user presses a key, ensuring that any final output
        can be viewed before the curses window is closed. After a key is pressed, it calls
        `curses.endwin()` to restore the terminal to its normal operating mode.
        """
        self.stdscr.refresh()
        curses.endwin()

    def is_key_up(self, key, row, max_columns):
        """
        Checks if the given key corresponds to the 'up' arrow key and if moving up is possible within the grid.

        Args:
            key (int): The key code to check.
            row (int): The current row index.
            max_columns (int): The number of columns in the grid.

        Returns:
            bool: True if the key is 'up' and moving up is within bounds, False otherwise.
        """
        return key == curses.KEY_UP and row - max_columns >= 0
    
    def is_key_down(self, key, row, max_columns, list):
        """
        Checks if the given key corresponds to the 'down' arrow key and if moving down is possible within the grid.

        Args:
            key (int): The key code to check.
            row (int): The current row index.
            max_columns (int): The number of columns in the grid.

        Returns:
            bool: True if the key is 'down' and moving down is within bounds, False otherwise.
        """
        return key == curses.KEY_DOWN and row + max_columns < len(list)
    
    def is_key_left(self, key, row, max_columns):
        """
        Checks if the given key corresponds to the 'left' arrow key and if moving left is possible within the grid.

        Args:
            key (int): The key code to check.
            row (int): The current row index.
            max_columns (int): The number of columns in the grid.

        Returns:
            bool: True if the key is 'left' and moving left is within bounds, False otherwise.
        """
        return key == curses.KEY_LEFT and row % max_columns > 0

    def is_key_right(self, key, row, max_columns, list):
        """
        Checks if the given key corresponds to the 'right' arrow key and if moving right is possible within the grid.

        Args:
            key (int): The key code to check.
            row (int): The current row index.
            max_columns (int): The number of columns in the grid.

        Returns:
            bool: True if the key is 'right' and moving right is within bounds, False otherwise.
        """
        key == curses.KEY_RIGHT and (row % max_columns) < (max_columns - 1) and (row + 1) < len(list)

    def is_key_toggle_select(self, key):
        """
        Check if the given key corresponds to a selection action.

        Args:
            key (int): The key code to check.

        Returns:
            bool: True if the key is Space, False otherwise.
        """
        return key == 32
    
    def is_key_select(self, key):
        """
        Checks if the provided key corresponds to the 'finish' action.

        Args:
            key (int): The key code to check.

        Returns:
            bool: True if the key is Enter, False otherwise.
        """
        return key in (curses.KEY_ENTER, 10, 13)

    def display_menu(self, packages, instructions, max_columns=1):

        current_row = 0
        selected = [False] * len(packages)
        finished = False

        while not finished:
            self.stdscr.clear()
            self.display_ascii_menu()
            for idx, line in enumerate(instructions):
                self.display_str(line, 0, FIRST_ROW + idx)

            #? Display selection options. ('Name' field of the dictionary)
            for idx, env in enumerate(packages):
                col = idx % max_columns
                row = idx // max_columns + FIRST_ROW + len(instructions) + 1
                if row >= self.height - 3:
                    break
                checkbox = "[x]" if selected[idx] else "[ ]"
                name = env.get("Name", str(env))
                attr = curses.A_REVERSE if idx == current_row else curses.A_NORMAL
                try:
                    self.stdscr.addstr(row, col * (self.width // max_columns), f"{checkbox} {name}", attr)
                except curses.error:
                    pass

            #? Display selected packages summary
            selected_list = [env.get("Name", str(env)) for idx, env in enumerate(packages) if selected[idx]]
            summary_str = "Selected Packages: " + (", ".join(selected_list) if selected_list else "None")
            try:
                self.stdscr.addstr(self.height - 2, 0, summary_str[:self.width])
            except curses.error:
                pass

            self.stdscr.refresh()

            key = self.stdscr.getch()

            if self.is_key_up(key, current_row, max_columns):
                current_row -= max_columns
            elif self.is_key_down(key, current_row, max_columns, packages):
                current_row += max_columns
            elif self.is_key_left(key, current_row, max_columns):
                current_row -= 1
            elif self.is_key_right(key, current_row, max_columns, packages):
                current_row += 1
            elif self.is_key_toggle_select(key):
                selected[current_row] = not selected[current_row]
            elif self.is_key_select(key):
                finished = True

            self.stdscr.clear()

        self.close()

        return selected_list
    
    def display_categories(self, items, title="Select a category to proceed", max_columns=1):
        """
        Displays a list of items as togglable checkbox options in the terminal UI.

        Args:
            items (list): List of strings to display as checkbox items.
            title (str): Title to display above the list.
            max_columns (int): Number of columns for the checkbox grid.

        Returns:
            list: List of selected item strings.
        """
        current_row = 0
        selected = [False] * len(items)
        finished = False

        while not finished:
            self.stdscr.clear()
            self.display_ascii_menu()
            self.display_str(title, 0, FIRST_ROW)

            #? Display checkbox items
            for idx, item in enumerate(items):
                col = idx % max_columns
                row = idx // max_columns + FIRST_ROW + 2
                if row >= self.height - 3:
                    break
                checkbox = "[x]" if selected[idx] else "[ ]"
                attr = curses.A_REVERSE if idx == current_row else curses.A_NORMAL
                try:
                    self.stdscr.addstr(row, col * (self.width // max_columns), f"{checkbox} {item}", attr)
                except curses.error:
                    pass

            #? Display selected summary
            selected_list = [item for idx, item in enumerate(items) if selected[idx]]
            summary_str = "Selected: " + (", ".join(selected_list) if selected_list else "None")
            try:
                self.stdscr.addstr(self.height - 2, 0, summary_str[:self.width])
            except curses.error:
                pass

            self.stdscr.refresh()
            key = self.stdscr.getch()

            if self.is_key_up(key, current_row, max_columns):
                current_row -= max_columns
            elif self.is_key_down(key, current_row, max_columns, items):
                current_row += max_columns
            elif self.is_key_left(key, current_row, max_columns):
                current_row -= 1
            elif self.is_key_right(key, current_row, max_columns, items):
                current_row += 1
            elif self.is_key_toggle_select(key):
                selected[current_row] = not selected[current_row]
            elif self.is_key_select(key):
                finished = True

            self.stdscr.clear()

        self.close()
        return selected_list