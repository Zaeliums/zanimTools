import maya.cmds as cmds

class NamingConvention:
    settings_node = "rigSetupSettings"

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
    
    _defaults = {
        "separator": "_",  # Should probably never be changed
        "side_l": "L",
        "side_r": "R",
        "side_c": "C",
        "side_index": 0,  # What token contains side indicator
        "pos_top_name": "Top",
        "pos_bot_name": "Bot",
        "pos_corner_name": "Corner",
        "pos_mid_name": "Mid",
        "pos_front_name": "Front",
        "pos_back_name": "Back",
        "pos_index": 1,  # What token contains position indicator
        "type_joint": "JNT",
        "type_control": "CTL",
        "type_group": "GRP",
        "type_locator": "LOC",
        "type_follicle": "FOL",
        "type_index": 2,  # What token contains type indicator
        "jaw_joint_reference": "C_jawA01_JNT",
        "jaw_control": "C_jawOpen_CTL",
        "jaw01_jnt": "C_jawA01_JNT",
        "mirror_behavior": False
    }
    def __init__(self):
        for attr_name, default_value in self._defaults.items():
            setattr(self, attr_name, self.get_attr(attr_name, default_value))


    def get_attr(self, attr_name, default):
        if cmds.objExists(self.settings_node) and cmds.attributeQuery(attr_name, node=self.settings_node, exists=True):
            return cmds.getAttr(f"{self.settings_node}.{attr_name}")
        return default

    def fetch_scene_data(self):
        return {attr: getattr(self, attr) for attr in self._defaults}

    def save_data(self, ui_elements):
        scene_data = self.fetch_scene_data()

        for ui_element, ui_value in scene_data.items():
            if isinstance(ui_value, bool):
                value = cmds.checkBox(ui_elements[ui_element], query=True, value=True)
            elif isinstance(ui_value, str):
                value = cmds.textField(ui_elements[ui_element], query=True, text=True)
            elif isinstance(ui_value, int):
                value = cmds.intField(ui_elements[ui_element], query=True, value=True)
            elif isinstance(ui_value, float):
                value = cmds.floatField(ui_elements[ui_element], query=True, value=True)

            if not cmds.objExists(self.settings_node):
                cmds.createNode("transform", name=self.settings_node)

            attr_type = type(scene_data[ui_element])
            if attr_type == bool:
                atype = "bool"
            elif attr_type == str:
                atype = "string"
            elif attr_type == int:
                atype = "long"
            elif attr_type == float:
                atype = "float"

            if not cmds.attributeQuery(ui_element, node=self.settings_node, exists=True):
                if atype == "string":
                    cmds.addAttr(self.settings_node, longName=ui_element, dataType=atype)
                else:
                    cmds.addAttr(self.settings_node, longName=ui_element, attributeType=atype)

            if atype == "string":
                cmds.setAttr(f"{self.settings_node}.{ui_element}", value, type=atype)
            else:
                cmds.setAttr(f"{self.settings_node}.{ui_element}", value)


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
