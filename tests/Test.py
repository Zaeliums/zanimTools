import maya.cmds as cmds
from collections import namedtuple

RigSetting = namedtuple('RigSetting', ['label', 'value'])

class NamingConvention:
    settings_node = "rigSetupSettings"
    
    _defaults = {
        "separator": RigSetting("Separator", "_"),
        "side_l": RigSetting("Side Left Prefix", "L"),
        "side_r": RigSetting("Side Right Prefix", "R"),
        "side_c": RigSetting("Side Center Prefix", "C"),
        "side_index": RigSetting("Side Index", 0),
        "pos_top_name": RigSetting("Top Position Name", "Top"),
        "pos_bot_name": RigSetting("Bottom Position Name", "Bot"),
        "pos_corner_name": RigSetting("Corner Position Name", "Corner"),
        "pos_mid_name": RigSetting("Middle Position Name", "Mid"),
        "pos_front_name": RigSetting("Front Position Name", "Front"),
        "pos_back_name": RigSetting("Back Position Name", "Back"),
        "pos_index": RigSetting("Position Index", 1),
        "type_joint": RigSetting("Joint Type", "JNT"),
        "type_control": RigSetting("Control Type", "CTL"),
        "type_group": RigSetting("Group Type", "GRP"),
        "type_locator": RigSetting("Locator Type", "LOC"),
        "type_follicle": RigSetting("Follicle Type", "FOL"),
        "type_index": RigSetting("Type Index", 2),
        "jaw_joint_reference": RigSetting("Jaw Joint Reference", "C_jawA01_JNT"),
        "jaw_control": RigSetting("Jaw Control", "C_jawOpen_CTL"),
        "jaw01_jnt": RigSetting("Jaw01 Joint", "C_jawA01_JNT"),
        "mirror_behavior": RigSetting("Mirror Behavior", False)
    }

    def __init__(self):
        for attr_name, default in self._defaults.items():
            setattr(self, attr_name, self.get_attr(attr_name, default.value))

    def get_attr(self, attr_name, attr_value):
        if cmds.objExists(self.settings_node) and cmds.attributeQuery(attr_name, node=self.settings_node, exists=True):
            return cmds.getAttr(f"{self.settings_node}.{attr_name}")
        return attr_value

    def fetch_rig_settings(self):
        return {attr: getattr(self, attr) for attr in self._defaults}

    def save_settings(self, ui_elements):
        rig_settings = self.fetch_rig_settings()

        for ui_element, ui_value in rig_settings.items():
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

            attr_type = type(rig_settings[ui_element])
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

        

class MainMenu:
    def __init__(self, naming_convention):
        self.window = "dataInputWindow"
        self.title = "Data Input UI"
        self.size = (300, 800)
        self.naming_convention = naming_convention
        self.ui_elements = {}

        self.create_ui()

    def create_ui(self):
        if cmds.window(self.window, exists=True):
            cmds.deleteUI(self.window, window=True)

        self.window = cmds.window(self.window, title=self.title, widthHeight=self.size)
        self.layout = cmds.columnLayout(adjustableColumn=True)

        rig_settings = self.naming_convention.fetch_rig_settings()
        for ui_element, ui_value in rig_settings.items():
            # Access the label and default value from the named tuple
            label = self.naming_convention._defaults[ui_element].label
            if isinstance(ui_value, bool):
                self.create_checkbox(ui_element, ui_value, label)
            elif isinstance(ui_value, str):
                self.create_textbox(ui_element, ui_value, label)
            elif isinstance(ui_value, int):
                self.create_numerical_box(ui_element, ui_value, label, int)
            elif isinstance(ui_value, float):
                self.create_numerical_box(ui_element, ui_value, label, float)

        self.save_button = cmds.button(label="Save Settings", command=self.save_settings)
        self.build_rig = cmds.button(label="Build Rig", command=lambda *_: create_rig(self.naming_convention))


        cmds.showWindow(self.window)

    def create_checkbox(self, name, value, label):
        checkbox = cmds.checkBox(label=label, value=value)
        self.ui_elements[name] = checkbox

    def create_textbox(self, name, value, label):
        cmds.text(label=f"{label}:")
        textbox = cmds.textField(text=value)
        self.ui_elements[name] = textbox

    def create_numerical_box(self, name, value, label, value_type):
        cmds.text(label=f"{label}:")
        if value_type == int:
            numerical_box = cmds.intField(value=value)
        else:
            numerical_box = cmds.floatField(value=value)
        self.ui_elements[name] = numerical_box

    def save_settings(self, *args):
        self.naming_convention.save_settings(self.ui_elements)
        self.naming_convention = NamingConvention()  # Reload updated values
        cmds.confirmDialog(title="Settings Saved", message="Settings has been saved to the scene node.", button=["OK"])

def create_rig(naming_convention):
    print(naming_convention.fetch_rig_settings())

def stripped_names(naming_convention, is_mirror_behavior=True):
    control_list = cmds.ls(sl=True)  # Get selected controls in Maya
    if is_mirror_behavior:
        # Replace the 'side_l' and 'side_r' in the control names
        stripped_names = [
            ctrl.replace(naming_convention.side_l, "").replace(naming_convention.side_r, "")
            for ctrl in control_list
        ]
        print(stripped_names)  # Print the stripped names (or use them as needed)

# Example usage
naming_convention = NamingConvention()
MainMenu(naming_convention)