import json

#TODO: Re-write description
#TODO: Add menu switching and function handling
#TODO: Perhaps switch import template to template in object.json

class Menu:
    def __init__(self, blueprint, parent=None):
        self.parent = parent
        self.menu_options = {}

        # Initialize default attributes for menu
        self.label = ""
        self.header = "\n\tChoose what you would like to do:"
        self.separator = 50 * "="
        self.selection_message = "\nSelection > "
        self.error_message = "Invalid selection! Please type number from list!"

        # Initialize attributes
        label = blueprint.get("label")
        header = blueprint.get("head")
        selection_message = blueprint.get("selection_message")
        error_message = blueprint.get("error_message")

        # Try to add new attributes to menu
        if label is not None:
            self.label = label
        if header is not None:
            self.header = header
        if selection_message is not None:
            self.selection_message = selection_message
        if error_message is not None:
            self.error_message = error_message

        # Initialize key to 1
        key = 1

        # Loop through blueprint with various keys to add menu options
        while True:
            # Assign menu_option to the specified key
            menu_option = blueprint.get(str(key))

            # If the menu option exists
            if menu_option:
                # Append a new menu to the menu option
                self.menu_options[str(key)] = Menu(menu_option, self)
                key += 1
            else:
                break

    def as_dict(self):
        return to_dict(self)

    def show(self):
        # Declare user input
        inp = 0
        selection = None

        # Check to make sure there are menu options
        if not self.menu_options:
            return

        # Print header and separators
        print(self.separator)
        print(self.header)
        print()
        print(self.separator)

        # Check if the menu has a parent and print "go back" if it does
        if self.parent is not None:
            print("0. Go back")

        # Loop through options and print them
        key = 1
        while True:
            cur_option = self.menu_options.get(str(key))
            if cur_option is None:
                break
            print(str(key) + ". ", end='')
            print(cur_option.label)
            key += 1

        # Get user input and validate it using the key from the menu option
        #   dictionary
        while True:
            print(self.separator, end='')
            inp = input(self.selection_message)
            selection = self.menu_options.get(inp)
            if selection is not None or inp == "0":
                break
            else:
                print()
                print(self.error_message)

        if inp == "0" and self.parent is not None:
            self.parent.show()

        if type(selection) is Menu:
            selection.show()


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
