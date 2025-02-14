import maya.cmds as cmds

class NamingConvention:
    def __init__(self, settings_node="rigSetupSettings"):
        self.settings_node = settings_node
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
        self.type_control = self.get_attr("type_control", "CTL")
        self.type_group = self.get_attr("type_group", "GRP")
        self.type_locator = self.get_attr("type_locator", "LOC")
        self.type_follicle = self.get_attr("type_follicle", "FOL")
        self.type_index = self.get_attr("type_index", 2)  # What token contains type indicator

        self.jaw_joint_reference = self.get_attr("jaw_joint_reference", "C_jawA01_JNT")  # Specific full names
        self.jaw_control = self.get_attr("jaw_control", "C_jawOpen_CTL")  # Specific full names

        self.jaw01_jnt = self.get_attr("jaw01_jnt", "C_jawA01_JNT")

        self.mirror_behavior = self.get_attr("mirror_behavior", False)

    def get_attr(self, name, default):
        if cmds.objExists(self.settings_node) and cmds.attributeQuery(name, node=self.settings_node, exists=True):
            return cmds.getAttr(f"{self.settings_node}.{name}")
        return default

    def get_attributes(self):
        return {attr: getattr(self, attr) for attr in dir(self) if
                not attr.startswith('__') and not callable(getattr(self, attr))}

    def save_data(self, attribute_values):
        attributes = self.get_attributes()

        for attr_name, attr_value in attributes.items():
            if isinstance(attr_value, bool):
                value = cmds.checkBox(attribute_values[attr_name], query=True, value=True)
            elif isinstance(attr_value, str):
                value = cmds.textField(attribute_values[attr_name], query=True, text=True)
            elif isinstance(attr_value, int):
                value = cmds.intField(attribute_values[attr_name], query=True, value=True)
            elif isinstance(attr_value, float):
                value = cmds.floatField(attribute_values[attr_name], query=True, value=True)

            if not cmds.objExists(self.settings_node):
                cmds.createNode("transform", name=self.settings_node)

            attr_type = type(attributes[attr_name])
            if attr_type == bool:
                atype = "bool"
            elif attr_type == str:
                atype = "string"
            elif attr_type == int:
                atype = "long"
            elif attr_type == float:
                atype = "float"

            if not cmds.attributeQuery(attr_name, node=self.settings_node, exists=True):
                if atype == "string":
                    cmds.addAttr(self.settings_node, longName=attr_name, dataType=atype)
                else:
                    cmds.addAttr(self.settings_node, longName=attr_name, attributeType=atype)

            if atype == "string":
                cmds.setAttr(f"{self.settings_node}.{attr_name}", value, type=atype)
            else:
                cmds.setAttr(f"{self.settings_node}.{attr_name}", value)

        cmds.confirmDialog(title="Data Saved", message="Data has been saved to the scene node.", button=["OK"])

class MayaDataInputUI:
    def __init__(self, naming_convention):
        self.window = "dataInputWindow"
        self.title = "Data Input UI"
        self.size = (300, 800)
        self.naming_convention = naming_convention
        self.attribute_values = {}

        self.create_ui()

    def create_ui(self):
        if cmds.window(self.window, exists=True):
            cmds.deleteUI(self.window, window=True)

        self.window = cmds.window(self.window, title=self.title, widthHeight=self.size)
        self.layout = cmds.columnLayout(adjustableColumn=True)

        attributes = self.naming_convention.get_attributes()
        for attr_name, attr_value in attributes.items():
            if isinstance(attr_value, bool):
                self.create_checkbox(attr_name, attr_value)
            elif isinstance(attr_value, str):
                self.create_textbox(attr_name, attr_value)
            elif isinstance(attr_value, int):
                self.create_numerical_box(attr_name, attr_value, int)
            elif isinstance(attr_value, float):
                self.create_numerical_box(attr_name, attr_value, float)

        self.save_button = cmds.button(label="Save Data", command=self.save_data)

        cmds.showWindow(self.window)

    def create_checkbox(self, name, value):
        checkbox = cmds.checkBox(label=name, value=value)
        self.attribute_values[name] = checkbox

    def create_textbox(self, name, value):
        cmds.text(label=f"{name}:")
        textbox = cmds.textField(text=value)
        self.attribute_values[name] = textbox

    def create_numerical_box(self, name, value, value_type):
        cmds.text(label=f"{name}:")
        if value_type == int:
            numerical_box = cmds.intField(value=value)
        else:
            numerical_box = cmds.floatField(value=value)
        self.attribute_values[name] = numerical_box

    def save_data(self, *args):
        self.naming_convention.save_data(self.attribute_values)

# Example usage
naming_convention = NamingConvention()
MayaDataInputUI(naming_convention)