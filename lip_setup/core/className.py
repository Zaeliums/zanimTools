import re

class className:
    def __init__(self, side_l_name="L", side_r_name="R", side_c_name="C",
                 pos_top_name="Top", pos_bot_name="Bot", pos_corner_name="Corner", 
                 pos_mid_name="Mid", pos_front_name="Front", pos_back_name="Back", 
                 type_jnt="JNT", type_ctrl="CTL"):
        # Initialize the naming conventions with defaults or provided values
        self.side_l_name = side_l_name
        self.side_r_name = side_r_name
        self.side_c_name = side_c_name
        
        self.pos_top_name = pos_top_name
        self.pos_bot_name = pos_bot_name
        self.pos_corner_name = pos_corner_name
        self.pos_mid_name = pos_mid_name
        self.pos_front_name = pos_front_name
        self.pos_back_name = pos_back_name
        
        self.type_jnt = type_jnt
        self.type_ctrl = type_ctrl

    @classmethod
    def get_mirrored_name(cls, controller_name):
        # Logic to get mirrored name
        if cls.side_l_name in controller_name:
            return controller_name.replace(cls.side_l_name, cls.side_r_name)
        elif cls.side_r_name in controller_name:
            return controller_name.replace(cls.side_r_name, cls.side_l_name)
        else:
            return controller_name  # Return as-is if no match
    
    def update_naming_convention(self, side_l, side_r, side_c, pos_top, pos_bot, 
                                 pos_corner, pos_mid, pos_front, pos_back, 
                                 type_jnt, type_ctrl):
        # Update the naming convention values based on UI input
        self.side_l_name = side_l
        self.side_r_name = side_r
        self.side_c_name = side_c
        self.pos_top_name = pos_top
        self.pos_bot_name = pos_bot
        self.pos_corner_name = pos_corner
        self.pos_mid_name = pos_mid
        self.pos_front_name = pos_front
        self.pos_back_name = pos_back
        self.type_jnt = type_jnt
        self.type_ctrl = type_ctrl

    def resolve(self, base_name, pos_name, side_name, number=None, type=None):
        """
        Generate a full name based on current naming convention values.
        """
        components = []
        if side_name == 'L':
            components.append(self.side_l_name)
        elif side_name == 'R':
            components.append(self.side_r_name)
        elif side_name == 'C':
            components.append(self.side_c_name)
        
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
                components.append(self.type_jnt)
            elif type == 'CTL':
                components.append(self.type_ctrl)

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
        side_name = words[0] if len(words) > 0 and words[0] in [cls.side_l_name, cls.side_r_name, cls.side_c_name] else None

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
