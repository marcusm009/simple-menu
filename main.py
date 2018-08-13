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
        self.header = "\nChoose what you would like to do:\n"
        self.separator = 50 * "="
        self.footer = "\nSelection: \"Enter\" or \"->\" | Go back: \"<-\""
        self.function = None

        # Initialize attributes
        label = blueprint.get("label")
        header = blueprint.get("head")
        footer = blueprint.get("footer")
        function = blueprint.get("function")

        # Try to add new attributes to menu
        if label is not None:
            self.label = label
        if header is not None:
            self.header = header
        if function is not None:
            self.function = function
        if footer is not None:
            self.footer = footer

        menu_options = blueprint.get("menu_options")

        for menu_option in menu_options:
            self.menu_options.append(Menu(menu_option, self))

    def __show__(self, stdscr):
        # Initialize option and selection
        option = 0
        selection = None
        function = None

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

            # Add the footer
            stdscr.addstr(self.footer)


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
                if self.parent:
                    selection = self.parent
                else:
                    return

        # Shows the next menu option
        function = selection.show()

        # Restores default color scheme
        curses.use_default_colors()

        return function

    def show(self):
        # Check to make sure there are menu options. If not, it breaks out
        #   recursion by returning the current function
        if not self.menu_options:
            print("No menu options!")
            return self.function

        function = curses.wrapper(self.__show__)
        return function

def call_with_label(label):
    possibles = globals().copy()
    possibles.update(locals())
    method = possibles.get(label)
    if not method:
         raise NotImplementedError("Method %s not implemented" % label)
    method()

def func():
    print("hello")

def main():
    # with open("menu.json", "w") as write_file:
    #     json.dump(dict, write_file, indent=4, sort_keys=True)

    with open("menu.json", "r") as read_file:
        blueprint = json.load(read_file)

    menu = Menu(blueprint)
    function = menu.show()
    call_with_label(function)


main()
