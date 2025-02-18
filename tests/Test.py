import maya.cmds as cmds

class NamingConvention:
    settings_node = "rigSetupSettings"
    
    # Default values
    _defaults = {
        "separator": "_",
        "side_l": "L",
        "side_r": "R",
        "side_c": "C",
        "side_index": 0,
        "pos_top_name": "Top",
        "pos_bot_name": "Bot",
        "pos_corner_name": "Corner",
        "pos_mid_name": "Mid",
        "pos_front_name": "Front",
        "pos_back_name": "Back",
        "pos_index": 1,
        "type_joint": "JNT",
        "type_control": "CTL",
        "type_group": "GRP",
        "type_locator": "LOC",
        "type_follicle": "FOL",
        "type_index": 2,
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

        scene_data = self.naming_convention.fetch_scene_data()
        for ui_element, ui_value in scene_data.items():
            if isinstance(ui_value, bool):
                self.create_checkbox(ui_element, ui_value)
            elif isinstance(ui_value, str):
                self.create_textbox(ui_element, ui_value)
            elif isinstance(ui_value, int):
                self.create_numerical_box(ui_element, ui_value, int)
            elif isinstance(ui_value, float):
                self.create_numerical_box(ui_element, ui_value, float)

        self.save_button = cmds.button(label="Save Data", command=self.save_data)
        self.build_rig = cmds.button(label="Build Rig", command=lambda *_: create_rig(self.naming_convention))


        cmds.showWindow(self.window)

    def create_checkbox(self, name, value):
        checkbox = cmds.checkBox(label=name, value=value)
        self.ui_elements[name] = checkbox

    def create_textbox(self, name, value):
        cmds.text(label=f"{name}:")
        textbox = cmds.textField(text=value)
        self.ui_elements[name] = textbox

    def create_numerical_box(self, name, value, value_type):
        cmds.text(label=f"{name}:")
        if value_type == int:
            numerical_box = cmds.intField(value=value)
        else:
            numerical_box = cmds.floatField(value=value)
        self.ui_elements[name] = numerical_box

    def save_data(self, *args):
        self.naming_convention.save_data(self.ui_elements)
        self.naming_convention = NamingConvention()  # Reload updated values
        cmds.confirmDialog(title="Data Saved", message="Data has been saved to the scene node.", button=["OK"])

def create_rig(naming_convention):
    print(naming_convention.fetch_scene_data())

# Example usage
naming_convention = NamingConvention()
MainMenu(naming_convention)