import re

import maya.cmds as cmds


class NamingConvention:
    # TODO: Make this updated by inputs in Maya; ask Alex, he seemed to know what he was talking about
    def __init__(self, settings_node="rigSetupSettings"):
        self.settings_node = settings_node

        # Ensure settings node exists
        if not cmds.objExists(self.settings_node):
            cmds.createNode("transform", name=self.settings_node)

        """
        nomenclature works like this:
        name is made from 3 tokens
        side token
        body token
        type token
        separators "_"
        They are usually structured like "side_body_type" or "type_body_side"
        They can be queried and worked with regardless of position, using their name structure index
        0 means it's the first token, 1 the second token and 2 the third. All tokens are separated by a separator "_"
        
        A token can contain multiple values combined:
            for example: L_lipTop01_CTL
                        L = side, index 0
                        lipTop01 = body, index 1
                                    The body here contains "name + pos + number", but can still
                        CTL = type, index 2
        So to find if this lip is Top or Bot, you'd need to look for the specific word in the index 1
        
        If values need to be exposed in the UI to be changed by the user, add them both here and in main_menu.py in the 
        class __init__ UI layout.
        """
        # Load initial values from Maya attributes (or use defaults)
        self.separator = self.get_attr("separator", "_")  # Should probably never be changed

        self.side_l = self.get_attr("side_l", "L")
        self.side_r = self.get_attr("side_r", "R")
        self.side_c = self.get_attr("side_c", "C")
        self.side_index = self.get_attr("side_index", 0)  # What token contains side indicator

        self.pos_top_name = self.get_attr("pos_top_name", "Top")
        self.pos_bot_name = self.get_attr("pos_bot_name", "Bot")
        self.pos_corner_name = self.get_attr("pos_corner_name", "Corner")
        self.pos_mid_name = self.get_attr("pos_mid_name", "Mid")
        self.pos_front_name = self.get_attr("pos_front_name", "Front")
        self.pos_back_name = self.get_attr("pos_back_name", "Back")
        self.pos_index = self.get_attr("pos_index", 1)  # What token contains position indicator

        self.type_joint = self.get_attr("type_joint", "JNT")
        self.type_control = self.get_attr("type_joint", "CTL")
        self.type_group = self.get_attr("type_group", "GRP")
        self.type_locator = self.get_attr("type_locator", "LOC")
        self.type_follicle = self.get_attr("type_follicle", "FOL")
        self.type_index = self.get_attr("type_index", 2)  # What token contains type indicator

        self.jaw_joint_reference = self.get_attr("jaw_joint_reference", "C_jawA01_JNT")  # Specific full names
        self.jaw_control = self.get_attr("jaw_control", "C_jawOpen_CTL")  # Specific full names

        self.jaw01_jnt = self.get_attr("jaw01_jnt", "C_jawA01_JNT")

        self.mirror_behavior = self.get_attr("mirror_behavior", "False")


    def get_attr(self, attr_name, default):
        """Retrieve an attribute value from Maya or return a default."""
        if cmds.attributeQuery(attr_name, node=self.settings_node, exists=True):
            return cmds.getAttr(f"{self.settings_node}.{attr_name}")
        return default

    def set_attr(self, attr_name, value):
        """Store an attribute value in Maya."""
        if not cmds.attributeQuery(attr_name, node=self.settings_node, exists=True):
            cmds.addAttr(self.settings_node, longName=attr_name, dataType="string")
        cmds.setAttr(f"{self.settings_node}.{attr_name}", value, type="string")

    def update_naming_convention(self, **kwargs):
        """Update values dynamically and save them to the settings node."""
        for key, value in kwargs.items():
            setattr(self, key, value)  # Update the attribute in Python
            self.set_attr(key, value)  # Store the value in Maya

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
                components.append(self.jaw_joint_reference)
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
