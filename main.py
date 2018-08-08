import json

#TODO: Re-write description
#TODO: Finish making menu class

# The idea here is to make a simple menu system where you pass in a dictionary
# using tuples as keys (zeros act as the header)

# Example:
# blueprint = {
# (0) : "Select something: "
# (1) : "Start"
#     (1.0) : "Select something else: "
#     (1.1) : "Singleplayer"
#         (1.1.0) : "Select a difficulty: "
#         (1.1.1) : "Easy"
#         (1.1.2): "Hard"
#     (1.2) : "Multiplayer"
#         (1.1.0) : "Select a difficulty: "
#         (1.1.1) : "Easy"
#         (1.1.2): "Hard"
#     (1.3) : "Options"
# (2) : "Quit"
#
# menu = Menu(blueprint)

class Menu:
    def __init__(self, blueprint, parent=None):
        self.parent = parent
        self.children = []

        # Initialize default attributes for menu
        self.header = "\nChoose what you would like to do:"
        self.selection_message = "\nSelection > "
        self.error_message = "Invalid selection! Please type number from list!"

        # Initialize attributes
        caption = blueprint.get("caption")
        header = blueprint.get("head")
        selection_message = blueprint.get("selection_message")
        error_message = blueprint.get("error_message")

        # Try to add new attributes to menu
        if caption is not None:
            self.caption = caption
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
            child_blueprint = blueprint.get(str(key))

            # Adds menu option or break out of loop
            if child_blueprint is not None:
                self.children.append(Menu(child_blueprint, self))
                key += 1
            else:
                break

def main():
    dict = {
        "1": {
            "1": {
                "caption": "Hello"
            },
            "2": {
                "caption": "Hello",
                "function": "foo"
            },
            "caption": "Create new Neural Network"
        },
        "2": {
            "1": {
                "caption": "Hello"
            },
            "2": {
                "caption": "Hello"
            },
            "caption": "Load Neural Network"
        }
    }

    with open("menu.json", "w") as write_file:
        json.dump(dict, write_file, indent=4, sort_keys=True)

    with open("menu.json", "r") as read_file:
        blueprint = json.load(read_file)

    menu = Menu(blueprint)

    with open("object.json", "w") as write_file:
        json.dump(menu, write_file, indent=4, sort_keys=True, default=lambda x: x.__dict__())



main()
