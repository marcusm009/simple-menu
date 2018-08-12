import json
import curses

#TODO: Re-write description
#TODO: Add menu switching and function handling
#TODO: Perhaps switch import template to template in object.json

class Menu:
    def __init__(self, blueprint, parent=None):
        self.parent = parent
        self.menu_options = []

        # Initialize default attributes for menu
        self.label = ""
        self.header = "\n\tChoose what you would like to do:"
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

        # Initialize curses attributes
        attributes = {}
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        attributes['normal'] = curses.color_pair(1)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
        attributes['highlighted'] = curses.color_pair(2)

        # Loop until an option is selected
        while not selection:

            # Clear the screen and add the header
            stdscr.erase()
            stdscr.addstr(self.header + '\n', curses.A_UNDERLINE)

            for idx in range(len(self.menu_options)):
                if idx == option:
                    attr = attributes['highlighted']
                else:
                    attr = attributes['normal']

                # Check if the menu has a parent and add an option to go back
                # if self.parent:
                #     stdscr.addstr("Go back\n", attr)

                stdscr.addstr(self.menu_options[idx].label + '\n', attr)

            # Gets the last character typed for input
            c = stdscr.getch()
            if c == curses.KEY_UP and option > 0:
                option -= 1
            elif c == curses.KEY_DOWN and option < len(self.menu_options) - 1:
                option += 1
            elif c == 10:
                selection = self.menu_options[option]

        function = getattr(self, "function")
        if function is not None:
            function()

        selection.show()


    def show(self):
        # Check to make sure there are menu options
        if not self.menu_options:
            print("No menu options!")
            return

        curses.wrapper(self.__show__)

        # # Check if the menu has a parent and print "go back" if it does
        # if self.parent is not None:
        #     print("0. Go back")
        #
        # if inp == "0" and self.parent is not None:
        #     self.parent.show()


def func():
    print("hello world!")

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

# {
#     "1": {
#         "1": {
#             "label": "Hello"
#         },
#         "2": {
#             "label": "Hello",
#             "function": "foo"
#         },
#         "label": "Create new Neural Network"
#     },
#     "2": {
#         "1": {
#             "label": "Hello"
#         },
#         "2": {
#             "label": "Hello"
#         },
#         "label": "Load Neural Network"
#     }
# }
