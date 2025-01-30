import re
import maya.cmds as cmds


class NamingConvention:
    # TODO: Make this updated by inputs in Maya; ask Alex, he seemed to know what he was talking about
    def __init__(self, settings_node="rigSetupSettings"):
        self.settings_node = settings_node

        # Load settings dynamically
        self.load_naming_convention()

    def load_naming_convention(self):
        """Load naming convention from Maya scene settings node."""
        self.side_l = self.get_attr("side_l", "L")
        self.side_r = self.get_attr("side_r", "R")
        self.side_c = self.get_attr("side_c", "C")

        self.pos_top_name = self.get_attr("pos_top_name", "Top")
        self.pos_bot_name = self.get_attr("pos_bot_name", "Bot")
        self.pos_corner_name = self.get_attr("pos_corner_name", "Corner")
        self.pos_mid_name = self.get_attr("pos_mid_name", "Mid")
        self.pos_front_name = self.get_attr("pos_front_name", "Front")
        self.pos_back_name = self.get_attr("pos_back_name", "Back")

        self.jaw_joint = self.get_attr("jaw_joint", "JNT")
        self.jaw_control = self.get_attr("jaw_control", "CTL")

    def get_attr(self, attr_name, default):
        """Helper to get attribute from settings node."""
        if cmds.attributeQuery(attr_name, node=self.settings_node, exists=True):
            return cmds.getAttr(f"{self.settings_node}.{attr_name}")
        return default

    def set_attr(self, attr_name, value):
        """Helper to set attribute on settings node."""
        if not cmds.attributeQuery(attr_name, node=self.settings_node, exists=True):
            cmds.addAttr(self.settings_node, longName=attr_name, dataType="string")
        cmds.setAttr(f"{self.settings_node}.{attr_name}", value, type="string")

    def update_naming_convention(self):
        """Update naming convention dynamically from settings."""
        self.load_naming_convention()

    @classmethod
    def get_mirrored_name(cls, controller_name):
        # Logic to get mirrored name
        if cls.side_l in controller_name:
            return controller_name.replace(cls.side_l, cls.side_r)
        elif cls.side_r in controller_name:
            return controller_name.replace(cls.side_r, cls.side_l)
        else:
            return controller_name  # Return as-is if no match

    def resolve(self, base_name, pos_name, side_name, number=None, type=None):
        """
        Generate a full name based on current naming convention values.
        """
        components = []
        if side_name == 'L':
            components.append(self.side_l)
        elif side_name == 'R':
            components.append(self.side_r)
        elif side_name == 'C':
            components.append(self.side_c)

        if base_name:
            components.append(base_name)

        if pos_name == 'Top':
            components.append(self.pos_top_name)
        elif pos_name == 'Bot':
            components.append(self.pos_bot_name)
        elif pos_name == 'Corner':
            components.append(self.pos_corner_name)
        elif pos_name == 'Mid':
            components.append(self.pos_mid_name)
        elif pos_name == 'Front':
            components.append(self.pos_front_name)
        elif pos_name == 'Back':
            components.append(self.pos_back_name)

        if number:
            components.append(number)

        if type:
            if type == 'JNT':
                components.append(self.jaw_joint)
            elif type == 'CTL':
                components.append(self.jaw_control)

        return "_".join(components)

    """
    @classmethod
    def from_base_name(cls, base_name, separator="_"):

        # Parse an existing name string into components based on the naming convention and camel case.
        # Example Input: "C_eyeTop02_JNT"

        # Step 1: Split the name based on camel case
        words = re.findall(r'[a-zA-Z][^A-Z]*', base_name)  # Extract words based on camel case

        # Step 2: Find the position name in the words list
        pos_name = None
        for word in words:
            if word in [cls.pos_top_name, cls.pos_bot_name, cls.pos_corner_name,
                        cls.pos_mid_name, cls.pos_front_name, cls.pos_back_name]:
                pos_name = word
                words.remove(word)
                break  # Exit the loop once a match is found

        # Step 3: The last word before the number is likely the base name
        base_name = words[-1] if len(words) > 0 else None

        # Step 4: Extract the number from the end of the base name if possible
        match = re.match(r'(\D+)(\d+)', base_name or "")
        number = match.group(2) if match else None

        # Step 5: Get the side from the prefix (first character)
        side_name = words[0] if len(words) > 0 and words[0] in [cls.side_l, cls.side_r, cls.side_c] else None

        # Return an instance of NameHelper with the extracted values
        return cls(
            side_name=side_name,
            base_name=base_name,
            pos_name=pos_name,
            number=number,
            type=None,  # Type is not parsed yet
            separator=separator,
        )

        """