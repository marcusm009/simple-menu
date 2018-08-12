import json
import curses

#TODO: Re-write description
#TODO: Perhaps switch import template to template in object.json

class Menu:
    def __init__(self, blueprint, parent=None):
        self.parent = parent
        self.menu_options = []

        # Initialize default attributes for menu
        self.label = ""
        self.header = "\nChoose what you would like to do:"
        self.separator = 50 * "="
        self.selection_message = "\nSelection > "
        self.function = None

        # Initialize attributes
        label = blueprint.get("label")
        header = blueprint.get("head")
        selection_message = blueprint.get("selection_message")
        function = blueprint.get("function")

        # Try to add new attributes to menu
        if label is not None:
            self.label = label
        if header is not None:
            self.header = header
        if function is not None:
            self.function = function
        if selection_message is not None:
            self.selection_message = selection_message

        menu_options = blueprint.get("menu_options")

        for menu_option in menu_options:
            self.menu_options.append(Menu(menu_option, self))


    def as_dict(self):
        return to_dict(self)

    def __show__(self, stdscr):
        # Initialize option and selection
        option = 0
        selection = None

        # Causes curses to use the default color scheme
        curses.use_default_colors()

        # Loop until an option is selected
        while not selection:
            # Clear the screen and add the header
            stdscr.erase()

            # Add the header
            stdscr.addstr(self.header + '\n', curses.A_UNDERLINE)

            # Loop through all menu options, check if the option is highlighted
            #   and draw accordingly
            for idx in range(len(self.menu_options)):
                if idx == option:
                    stdscr.addstr(self.menu_options[idx].label + '\n', curses.A_REVERSE)
                else:
                    stdscr.addstr(self.menu_options[idx].label + '\n')

            # Gets the last character typed for input
            c = stdscr.getch()
            # Up and down changes which menu option to highlight, while right
            #   and left selects and goes back accordingly
            if c == curses.KEY_UP and option > 0:
                option -= 1
            elif c == curses.KEY_DOWN and option < len(self.menu_options) - 1:
                option += 1
            elif c == curses.KEY_RIGHT or c == 10:
                selection = self.menu_options[option]
            elif c == curses.KEY_LEFT:
                selection = self.parent

        # TODO: Fix function functionality
        function = getattr(self, "function")
        if function is not None:
            function()

        # Shows the next menu option
        selection.show()

        # Restores default color scheme
        curses.use_default_colors()

    def show(self):
        # Check to make sure there are menu options
        if not self.menu_options:
            print("No menu options!")
            return

        curses.wrapper(self.__show__)

def func():
    print("hello world!")

# TODO: Fix to_dict not displaying nested menus
def to_dict(menu):
    loop_attributes = ["label", "function", "header", "selection_message",
        "error_message"]
    dict = {}

    # Loop through different attributes and add them to the dictionary
    for attribute in loop_attributes:
        if hasattr(menu, attribute):
            dict[attribute] = getattr(menu, attribute)

    # Check to see if the menu contains any menu_options and recursively
    #   call to_dict to add them as a nested dictionary
    if hasattr(menu, "menu_options"):
        key = 1
        menu_options = {}
        while True:
            try:
                menu_options[str(key)] = to_dict(menu.menu_options[str(key)])
                key += 1
            except:
                break
        dict["menu_options"] = menu_options

    return dict

def main():
    # with open("menu.json", "w") as write_file:
    #     json.dump(dict, write_file, indent=4, sort_keys=True)

    with open("menu.json", "r") as read_file:
        blueprint = json.load(read_file)

    menu = Menu(blueprint)
    menu.show()

    with open("object.json", "w") as write_file:
        json.dump(menu.as_dict(), write_file, indent=4, sort_keys=True)



main()
